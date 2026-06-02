from huggingface_hub import InferenceClient
from app.config import settings
from utils.logger import logger


class SpeechToText:
    """
    Speech-to-Text using openai/whisper-large-v3-turbo
    via HuggingFace Inference API (automatic_speech_recognition task).
    """

    def __init__(self):
        self.model_id = "openai/whisper-large-v3-turbo"

    def _get_client(self):
        token = settings.hf_token
        if token:
            return InferenceClient(provider="hf-inference", api_key=token)
        return None

    async def transcribe(self, audio_bytes: bytes) -> str:
        client = self._get_client()

        if client:
            try:
                result = client.automatic_speech_recognition(
                    audio=audio_bytes,
                    model=self.model_id
                )
                # Result can be a string or an object with .text attribute
                if hasattr(result, 'text'):
                    return result.text
                elif isinstance(result, dict):
                    return result.get("text", "")
                elif isinstance(result, str):
                    return result
            except Exception as e:
                logger.warning(f"Whisper STT remote inference failed: {e}. Falling back to default.")

        # Local mock fallback
        return "How do I control tomato early blight on my farm?"


speech_to_text = SpeechToText()
