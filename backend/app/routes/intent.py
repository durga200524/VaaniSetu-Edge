import io
import subprocess

import soundfile as sf

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from pydantic import BaseModel, Field
from imageio_ffmpeg import get_ffmpeg_exe

from app.intelligence.intent_engine import detect_intent
from app.intelligence.voice_pipeline import process_customer_voice


router = APIRouter(
    prefix="/api/v1/intelligence",
    tags=["AI Intelligence"]
)


class IntentRequest(BaseModel):

    text: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="Customer message or speech transcript"
    )


@router.post("/intent")
async def identify_customer_intent(
    request: IntentRequest
):

    result = detect_intent(request.text)

    return {
        "success": True,
        "original_text": request.text,
        "intent_analysis": result
    }


@router.post("/voice-intent")
async def identify_intent_from_voice(
    audio: UploadFile = File(...),
    language: str = Form("te-IN")
):

    audio_bytes = await audio.read()

    if not audio_bytes:
        raise HTTPException(
            status_code=400,
            detail="Uploaded audio file is empty."
        )

    if len(audio_bytes) > 25 * 1024 * 1024:
        raise HTTPException(
            status_code=413,
            detail="File must be smaller than 25 MB."
        )

    try:
        # Convert uploaded audio to WAV
        process = subprocess.run(
            [
                get_ffmpeg_exe(),
                "-i", "pipe:0",
                "-vn",
                "-ac", "1",
                "-ar", "16000",
                "-f", "wav",
                "pipe:1"
            ],
            input=audio_bytes,
            capture_output=True,
            check=True
        )

        wav_bytes = process.stdout

        # Validate audio duration
        with sf.SoundFile(io.BytesIO(wav_bytes)) as wav:
            duration = len(wav) / wav.samplerate

        if duration <= 0 or duration > 30:
            raise HTTPException(
                status_code=400,
                detail="Audio duration must be between 0 and 30 seconds."
            )

        # Run Prisma transcription and intent recognition
        result = await process_customer_voice(
            audio_bytes=wav_bytes,
            language=language
        )

        return {
            "success": result["success"],
            "duration_seconds": round(duration, 2),
            "voice_pipeline": result
        }

    except HTTPException:
        raise

    except subprocess.CalledProcessError as error:
        print(
            "AUDIO CONVERSION ERROR:",
            error.stderr.decode("utf-8", errors="replace")
        )

        raise HTTPException(
            status_code=400,
            detail="Unable to convert the uploaded audio."
        )

    except Exception as error:
        print("VOICE PIPELINE ERROR:", repr(error))

        raise HTTPException(
            status_code=502,
            detail="Voice processing failed. Check the backend terminal."
        )