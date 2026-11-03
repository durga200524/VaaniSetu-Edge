from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel, Field

from app.services.gnani_timbre import generate_speech


router = APIRouter(
    prefix="/api/v1/tts",
    tags=["Text to Speech"]
)


class TTSRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=2000)
    language: str = "en-IN"
    voice: str | None = None


@router.post("/generate")
async def text_to_speech(request: TTSRequest):
    try:
        result = await generate_speech(
            text=request.text,
            language=request.language,
            voice=request.voice
        )

        return Response(
            content=result["audio"],
            media_type="audio/wav",
            headers={
                "Content-Disposition": 'attachment; filename="vaanisetu_response.wav"',
                "X-TTS-Model": result["model"],
                "X-TTS-Voice": result["voice"],
                "X-TTS-Language": result["language"]
            }
        )

    except Exception as error:
        print("GNANI TTS ERROR:", repr(error))

        raise HTTPException(
            status_code=502,
            detail="Text-to-speech generation failed. Check backend terminal."
        )