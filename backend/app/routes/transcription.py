import io
import subprocess

import soundfile as sf
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from imageio_ffmpeg import get_ffmpeg_exe

from app.services.gnani_prisma import transcribe_audio


router = APIRouter(
    prefix="/api/v1/transcription",
    tags=["Speech Recognition"]
)


@router.post("/transcribe")
async def transcribe(
    audio: UploadFile = File(...),
    language: str = Form("te-IN")
):
    allowed_types = [
        "audio/wav",
        "audio/x-wav",
        "audio/mpeg",
        "audio/mp3",
        "audio/mp4",
        "video/mp4",
        "application/octet-stream"
    ]

    if audio.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file format. Upload WAV, MP3 or MP4."
        )

    audio_bytes = await audio.read()

    if not audio_bytes:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty."
        )

    if len(audio_bytes) > 25 * 1024 * 1024:
        raise HTTPException(
            status_code=413,
            detail="File must be smaller than 25 MB."
        )

    try:
        # Convert uploaded file to WAV
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

        # Read audio duration
        with sf.SoundFile(io.BytesIO(wav_bytes)) as wav:
            duration = len(wav) / wav.samplerate

        if duration <= 0:
            raise HTTPException(
                status_code=400,
                detail="No audio detected in the uploaded file."
            )

        if duration > 30:
            raise HTTPException(
                status_code=400,
                detail="Audio duration must not exceed 30 seconds."
            )

        # Send audio to Gnani Prisma
        result = await transcribe_audio(
            audio_bytes=wav_bytes,
            filename="converted_audio.wav",
            language=language
        )

        return {
            "success": True,
            "model": result.get("model", "Prisma v2.5"),
            "language": language,
            "duration_seconds": round(duration, 2),
            "transcript": result.get("transcript", ""),
            "request_id": result.get("request_id")
        }

    except HTTPException:
        raise

    except subprocess.CalledProcessError as error:
        print("AUDIO CONVERSION ERROR:", error.stderr.decode(
            "utf-8", errors="replace"
        ))

        raise HTTPException(
            status_code=400,
            detail="Audio conversion failed. Check the uploaded file."
        )

    except Exception as error:
        print("ACTUAL TRANSCRIPTION ERROR:", repr(error))

        raise HTTPException(
            status_code=502,
            detail="Speech recognition failed. Check the backend terminal."
        )