import os
from typing import Dict, Any, Optional
import firebase_admin
from firebase_admin import credentials, firestore, storage, auth
from app.config import settings
from utils.logger import logger

# Global clients
db_client = None
storage_bucket = None
firebase_app = None
is_mock_mode = False

# Mock in-memory database fallback to prevent startup failures
class MockFirestoreCollection:
    def __init__(self, name: str, db_ref: "MockFirestoreDb"):
        self.name = name
        self.db_ref = db_ref

    def document(self, doc_id: str):
        return MockFirestoreDocument(self.name, doc_id, self.db_ref)

    def add(self, data: Dict[str, Any], document_id: Optional[str] = None):
        import uuid
        doc_id = document_id or str(uuid.uuid4())
        self.db_ref.store[self.name][doc_id] = data
        return MockFirestoreDocument(self.name, doc_id, self.db_ref), MockFirestoreDocumentReference(doc_id)

    def get(self):
        docs = []
        collection_data = self.db_ref.store.get(self.name, {})
        for doc_id, content in collection_data.items():
            docs.append(MockFirestoreDocumentSnapshot(doc_id, content))
        return docs

    def stream(self):
        return self.get()

    def where(self, field: str, op: str, value: Any):
        # Extremely basic query filter mock
        docs = []
        collection_data = self.db_ref.store.get(self.name, {})
        for doc_id, content in collection_data.items():
            if field in content:
                match = False
                val = content[field]
                if op == "==" and val == value:
                    match = True
                elif op == "in" and value in val:
                    match = True
                elif op == "array_contains" and value in val:
                    match = True
                if match:
                    docs.append(MockFirestoreDocumentSnapshot(doc_id, content))
        return MockFirestoreQuery(docs)


class MockFirestoreQuery:
    def __init__(self, docs):
        self.docs = docs
    
    def get(self):
        return self.docs
    
    def stream(self):
        return self.docs


class MockFirestoreDocument:
    def __init__(self, collection: str, doc_id: str, db_ref: "MockFirestoreDb"):
        self.collection = collection
        self.id = doc_id
        self.db_ref = db_ref

    def get(self):
        data = self.db_ref.store.get(self.collection, {}).get(self.id)
        return MockFirestoreDocumentSnapshot(self.id, data)

    def set(self, data: Dict[str, Any], merge: bool = False):
        if self.collection not in self.db_ref.store:
            self.db_ref.store[self.collection] = {}
        if merge and self.id in self.db_ref.store[self.collection]:
            self.db_ref.store[self.collection][self.id].update(data)
        else:
            self.db_ref.store[self.collection][self.id] = data
        return self

    def update(self, data: Dict[str, Any]):
        return self.set(data, merge=True)

    def delete(self):
        if self.collection in self.db_ref.store and self.id in self.db_ref.store[self.collection]:
            del self.db_ref.store[self.collection][self.id]


class MockFirestoreDocumentReference:
    def __init__(self, doc_id: str):
        self.id = doc_id


class MockFirestoreDocumentSnapshot:
    def __init__(self, doc_id: str, data: Optional[Dict[str, Any]]):
        self.id = doc_id
        self._data = data
        self.exists = data is not None

    def to_dict(self) -> Optional[Dict[str, Any]]:
        return self._data


class MockFirestoreDb:
    def __init__(self):
        self.store: Dict[str, Dict[str, Any]] = {
            "users": {},
            "farms": {},
            "crops": {},
            "livestock": {},
            "disease_reports": {},
            "market_data": {
                "rice": {"name": "Rice", "price": 3420, "trend": "up", "forecast": 3600},
                "wheat": {"name": "Wheat", "price": 2400, "trend": "stable", "forecast": 2450},
                "tomato": {"name": "Tomato", "price": 1240, "trend": "down", "forecast": 1150}
            },
            "weather_data": {},
            "community_posts": {},
            "notifications": {},
            "sos_requests": {},
            "government_schemes": {
                "pm_kisan": {
                    "id": "pm_kisan",
                    "title": "PM Kisan Samman Nidhi",
                    "state": "All",
                    "crop": "All",
                    "min_farm_size": 0,
                    "max_farm_size": 100,
                    "benefits": "₹6,000 yearly income support"
                },
                "karnataka_subsidy": {
                    "id": "karnataka_subsidy",
                    "title": "Karnataka Free Seeds Scheme",
                    "state": "Karnataka",
                    "crop": "Sustainable Coffee",
                    "min_farm_size": 0,
                    "max_farm_size": 5,
                    "benefits": "Free organic crop seed distribution"
                }
            }
        }

    def collection(self, name: str) -> MockFirestoreCollection:
        if name not in self.store:
            self.store[name] = {}
        return MockFirestoreCollection(name, self)


class MockStorageBucket:
    def blob(self, path: str):
        return MockStorageBlob(path)


class MockStorageBlob:
    def __init__(self, path: str):
        self.path = path

    def upload_from_string(self, data: bytes, content_type: str):
        logger.info(f"[MockStorage] Uploaded {len(data)} bytes to {self.path} ({content_type})")

    def upload_from_file(self, file_obj, content_type: str):
        logger.info(f"[MockStorage] Uploaded file to {self.path} ({content_type})")

    def generate_signed_url(self, **kwargs) -> str:
        return f"https://mock-storage.googleapis.com/{settings.FIREBASE_STORAGE_BUCKET}/{self.path}"


def initialize_firebase():
    global db_client, storage_bucket, firebase_app, is_mock_mode
    
    # Check if Firebase has already been initialized
    if firebase_admin._apps:
        firebase_app = firebase_admin.get_app()
        db_client = firestore.client()
        storage_bucket = storage.bucket(name=settings.FIREBASE_STORAGE_BUCKET)
        logger.info("Connected to existing Firebase App successfully.")
        return

    try:
        # Check credentials file configuration
        creds_path = settings.FIREBASE_CREDENTIALS_PATH
        fallback_paths = [
            "service-account.json",
            "firebase-credentials.json",
            "backend/service-account.json",
            "backend/firebase-credentials.json",
            os.path.join(os.path.dirname(__file__), "..", "service-account.json"),
            os.path.join(os.path.dirname(__file__), "..", "firebase-credentials.json"),
            os.path.join(os.path.dirname(__file__), "service-account.json"),
            os.path.join(os.path.dirname(__file__), "firebase-credentials.json")
        ]
        
        for path in fallback_paths:
            if not creds_path and os.path.exists(path):
                creds_path = path
                logger.info(f"Auto-discovered Firebase service account credentials at: {path}")
                break

        if creds_path and os.path.exists(creds_path):
            cred = credentials.Certificate(creds_path)
            firebase_app = firebase_admin.initialize_app(cred, {
                "storageBucket": settings.FIREBASE_STORAGE_BUCKET,
                "databaseURL": settings.FIREBASE_DATABASE_URL
            })
            logger.info(f"Initialized Firebase with service account key: {creds_path}")
        else:
            # Fallback to default credentials or environment defaults
            firebase_app = firebase_admin.initialize_app(options={
                "storageBucket": settings.FIREBASE_STORAGE_BUCKET,
                "databaseURL": settings.FIREBASE_DATABASE_URL
            })
            logger.info("Initialized Firebase with default environment credential settings.")
            
        db_client = firestore.client()
        storage_bucket = storage.bucket(name=settings.FIREBASE_STORAGE_BUCKET)
    except Exception as e:
        logger.warning(
            f"Firebase SDK initialization failed: {e}. Switching to high-fidelity Mock Database sandbox."
        )
        db_client = MockFirestoreDb()
        storage_bucket = MockStorageBucket()
        is_mock_mode = True


initialize_firebase()
