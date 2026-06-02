import math
from huggingface_hub import InferenceClient
from typing import List, Dict, Any
from app.config import settings
from utils.logger import logger


class SchemeSearchEngine:
    """
    Semantic search engine for government agricultural schemes using
    BAAI/bge-small-en-v1.5 embeddings via HuggingFace Inference API (feature_extraction task).
    """

    def __init__(self):
        self.model_id = "BAAI/bge-small-en-v1.5"

    def _get_client(self):
        token = settings.hf_token
        if token:
            return InferenceClient(provider="hf-inference", api_key=token)
        return None

    async def search(self, query: str, schemes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        client = self._get_client()

        if client:
            try:
                # Build corpus: query + all scheme descriptions
                texts = [query] + [s.get("title", "") + " " + s.get("benefits", "") for s in schemes]

                # Get embeddings for all texts
                embeddings = client.feature_extraction(
                    text=texts,
                    model=self.model_id
                )

                if embeddings and len(embeddings) == len(texts):
                    query_emb = embeddings[0]
                    scored_schemes = []
                    for idx, scheme in enumerate(schemes):
                        scheme_emb = embeddings[idx + 1]
                        sim = self._cosine_similarity(query_emb, scheme_emb)
                        s_copy = scheme.copy()
                        s_copy["similarity_score"] = round(float(sim), 4)
                        scored_schemes.append(s_copy)
                    return sorted(scored_schemes, key=lambda x: x["similarity_score"], reverse=True)
            except Exception as e:
                logger.warning(f"BGE Small remote search failed: {e}. Falling back to word-overlap matching.")

        # Local High-Fidelity Jaccard/Word-Overlap Semantic Matcher (Offline Fallback)
        scored_schemes = []
        query_words = set(query.lower().split())

        for scheme in schemes:
            combined_text = (scheme.get("title", "") + " " + scheme.get("benefits", "") + " " + scheme.get("crop", "")).lower()
            scheme_words = set(combined_text.split())

            intersection = query_words.intersection(scheme_words)
            union = query_words.union(scheme_words)
            jaccard_score = len(intersection) / len(union) if union else 0.0

            sim_score = 0.5 + (jaccard_score * 0.5)

            s_copy = scheme.copy()
            s_copy["similarity_score"] = round(sim_score, 2)
            scored_schemes.append(s_copy)

        return sorted(scored_schemes, key=lambda x: x["similarity_score"], reverse=True)

    def _cosine_similarity(self, v1, v2) -> float:
        """Compute cosine similarity, handling nested list structures."""
        # Flatten if needed (some models return [[...]])
        if isinstance(v1, list) and len(v1) > 0 and isinstance(v1[0], list):
            v1 = v1[0]
        if isinstance(v2, list) and len(v2) > 0 and isinstance(v2[0], list):
            v2 = v2[0]

        dot_product = sum(x * y for x, y in zip(v1, v2))
        magnitude_v1 = math.sqrt(sum(x * x for x in v1))
        magnitude_v2 = math.sqrt(sum(x * x for x in v2))
        if not magnitude_v1 or not magnitude_v2:
            return 0.0
        return dot_product / (magnitude_v1 * magnitude_v2)


scheme_search_engine = SchemeSearchEngine()
