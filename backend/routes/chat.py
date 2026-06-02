import base64
from fastapi import APIRouter, Form, UploadFile, File, Depends, status
from typing import Dict, Any, Optional
from ai.farm_doctor import ai_farm_doctor
from ai.speech_to_text import speech_to_text
from ai.text_to_speech import text_to_speech
from app.dependencies import get_current_user
from app.exceptions import TerravaException

router = APIRouter(prefix="/chat", tags=["AI Farm Doctor"])


@router.post("")
async def chat_with_farm_doctor(
    message: Optional[str] = Form(None, description="Text message for the chatbot"),
    audio_file: Optional[UploadFile] = File(None, description="Optional audio recording of your question (WAV/MP3)"),
    lang: str = Form("en", description="Language code (e.g. en, hi, kn)"),
    session_id: Optional[str] = Form(None, description="Optional chat history session identifier"),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    uid = current_user["uid"]
    active_session = session_id or f"session_{uid}"

    # Verify input presence
    if not message and not audio_file:
        raise TerravaException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Provide either a textual message or an uploaded voice file",
            error_code="MISSING_INPUT"
        )

    try:
        user_query = message
        
        # Phase 1: Transcribe voice audio if provided (Speech To Text)
        if audio_file:
            audio_bytes = await audio_file.read()
            user_query = await speech_to_text.transcribe(audio_bytes)

        # Phase 2: Compute AI response from Phi-4 Mini (agricultural expert context)
        doctor_reply = await ai_farm_doctor.chat(
            session_id=active_session,
            message=user_query,
            lang=lang
        )

        # Phase 3: Synthesize reply back to speech (Text To Speech)
        # Convert language ISO standard if needed (e.g., en -> eng, hi -> hin, kn -> kan)
        tts_lang = "eng"
        if lang.lower() in ["hi", "hindi"]:
            tts_lang = "hin"
        elif lang.lower() in ["kn", "kannada"]:
            tts_lang = "kan"
            
        speech_bytes = await text_to_speech.synthesize(doctor_reply["response"], lang=tts_lang)
        base64_audio = base64.b64encode(speech_bytes).decode("utf-8")

        return {
            "session_id": active_session,
            "user_query": user_query,
            "response": doctor_reply["response"],
            "language": lang,
            "engine": doctor_reply["engine"],
            "audio_response_b64": base64_audio,
            "audio_format": "audio/wav"
        }
    except Exception as e:
        raise TerravaException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI Farm Doctor chatbot failure: {str(e)}",
            error_code="CHATBOT_FAILURE"
        )
