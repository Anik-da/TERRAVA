from huggingface_hub import InferenceClient
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
        }
        self.default_model = "facebook/mms-tts-eng"

    def _get_client(self):
        token = settings.hf_token
        if token:
            return InferenceClient(provider="hf-inference", api_key=token)
        return None

    async def synthesize(self, text: str, lang: str = "eng") -> bytes:
        target_model = self.model_map.get(lang.lower(), self.default_model)
        client = self._get_client()

        if client:
            try:
                # text_to_speech returns audio bytes directly
                audio_bytes = client.text_to_speech(
                    text=text,
                    model=target_model
                )
                if audio_bytes and len(audio_bytes) > 0:
                    return audio_bytes
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
