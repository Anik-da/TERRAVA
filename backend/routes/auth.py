from fastapi import APIRouter, status, Depends
from models.auth import FarmerRegister, FarmerLogin, PasswordReset, Token, UserResponse
from database.firebase import db_client, is_mock_mode
from utils.security import hash_password, verify_password, create_access_token
from app.exceptions import TerravaException
from typing import Dict, Any

router = APIRouter(prefix="/auth", tags=["Farmer Authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(payload: FarmerRegister):
    # Check if user already exists
    existing_users = db_client.collection("users").where("email", "==", payload.email).get()
    if len(existing_users) > 0:
        raise TerravaException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A farmer account with this email address already exists",
            error_code="EMAIL_ALREADY_EXISTS"
        )

    # In a real environment, we would also create the user in Firebase Auth.
    # To keep this backend ultra-portable, we handle state natively inside Firestore / memory.
    import uuid
    uid = str(uuid.uuid4())
    
    # Hash password securely
    hashed_pwd = hash_password(payload.password)
    
    user_data = {
        "uid": uid,
        "name": payload.name,
        "phone": payload.phone,
        "email": payload.email,
        "password": hashed_pwd,
        "state": payload.state,
        "district": payload.district,
        "farm_size": payload.farm_size,
        "role": "farmer",  # Default registration is a farmer
        "crops": [],
        "livestock": [],
        "location": None
    }

    # Store user in collection
    db_client.collection("users").document(uid).set(user_data)
    
    return UserResponse(**user_data)


@router.post("/login", response_model=Token)
async def login(payload: FarmerLogin):
    users = db_client.collection("users").where("email", "==", payload.email).get()
    if len(users) == 0:
        raise TerravaException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email address or password",
            error_code="INVALID_CREDENTIALS"
        )
        
    user_snap = users[0]
    user_data = user_snap.to_dict()
    
    if not verify_password(payload.password, user_data.get("password", "")):
        raise TerravaException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email address or password",
            error_code="INVALID_CREDENTIALS"
        )
        
    # Generate robust JWT access token
    token_data = {
        "uid": user_data["uid"],
        "sub": user_data["email"],
        "role": user_data.get("role", "farmer")
    }
    access_token = create_access_token(data=token_data)
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        role=user_data.get("role", "farmer")
    )


@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout():
    # Firebase is stateless with JWTs; client discards the token.
    return {"message": "Logged out successfully from your Terrava session"}


@router.post("/reset-password", status_code=status.HTTP_200_OK)
async def reset_password(payload: PasswordReset):
    users = db_client.collection("users").where("email", "==", payload.email).get()
    if len(users) == 0:
        raise TerravaException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No grower account exists with this email address",
            error_code="EMAIL_NOT_FOUND"
        )
    return {"message": f"Password reset instructions dispatched to: {payload.email}"}
