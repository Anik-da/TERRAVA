import requests
from app.config import settings
from utils.logger import logger


class TextToSpeech:
    """
    Text-to-Speech using Facebook's MMS-TTS multilingual models:
    - facebook/mms-tts-eng (English)
    - facebook/mms-tts-hin (Hindi)
    - facebook/mms-tts-kan (Kannada)
    via HuggingFace Inference API.
    """

    def __init__(self):
        self.model_map = {
            "eng": "facebook/mms-tts-eng",
            "hin": "facebook/mms-tts-hin",
            "kan": "facebook/mms-tts-kan",
            "tel": "facebook/mms-tts-tel",
            "tam": "facebook/mms-tts-tam",
            "mar": "facebook/mms-tts-mar",
            "ben": "facebook/mms-tts-ben",
        }
        self.default_model = "facebook/mms-tts-eng"

    def _get_headers(self):
        token = settings.hf_token
        if token:
            return {"Authorization": f"Bearer {token}"}
        return None

    async def synthesize(self, text: str, lang: str = "eng") -> bytes:
        target_model = self.model_map.get(lang.lower(), self.default_model)
        api_url = f"https://router.huggingface.co/hf-inference/models/{target_model}"
        headers = self._get_headers()

        if headers:
            try:
                response = requests.post(
                    api_url,
                    headers={**headers, "Content-Type": "application/json"},
                    json={"inputs": text},
                    timeout=30
                )
                if response.status_code == 200 and len(response.content) > 0:
                    return response.content
                else:
                    logger.warning(f"MMS-TTS API returned {response.status_code}: {response.text[:200]}")
            except Exception as e:
                logger.warning(f"MMS-TTS remote inference failed: {e}. Generating mock audio.")

        # Local mock WAV audio header + small noise block to prevent playback crashes
        mock_wav_header = (
            b"RIFF\x24\x08\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00\x40\x1f\x00\x00"
            b"\x40\x1f\x00\x00\x01\x00\x08\x00data\x00\x08\x00\x00"
        )
        mock_sound_data = b"\x80" * 2048
        return mock_wav_header + mock_sound_data


text_to_speech = TextToSpeech()
