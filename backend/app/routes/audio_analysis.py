import io
import subprocess

import soundfile as sf

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    HTTPException,
    Form
)
from fastapi.responses import Response
from imageio_ffmpeg import get_ffmpeg_exe

from app.audio.audio_analysis import analyze_audio
from app.audio.noise_reduction import reduce_noise
from app.audio.audio_metrics import compare_audio
from app.services.transcription_comparison import compare_transcriptions


router = APIRouter(
    prefix="/api/v1/audio",
    tags=["Audio Intelligence"]
)


def convert_to_wav(audio_bytes: bytes):

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

    return process.stdout


def validate_audio(wav_bytes: bytes):

    with sf.SoundFile(io.BytesIO(wav_bytes)) as wav:
        duration = len(wav) / wav.samplerate

    if duration <= 0 or duration > 30:
        raise ValueError(
            "Audio duration must be between 0 and 30 seconds."
        )

    return duration


@router.post("/analyze")
async def analyze_uploaded_audio(
    audio: UploadFile = File(...)
):

    audio_bytes = await audio.read()

    if not audio_bytes:
        raise HTTPException(400, "Audio file is empty.")

    if len(audio_bytes) > 25 * 1024 * 1024:
        raise HTTPException(413, "File must be smaller than 25 MB.")

    try:
        wav_bytes = convert_to_wav(audio_bytes)
        validate_audio(wav_bytes)

        result = analyze_audio(wav_bytes)

        return {
            "success": True,
            "message": "Audio analysis completed successfully.",
            "analysis": result
        }

    except Exception as error:
        print("AUDIO ANALYSIS ERROR:", repr(error))
        raise HTTPException(400, "Audio analysis failed.")


@router.post("/reduce-noise")
async def reduce_uploaded_audio_noise(
    audio: UploadFile = File(...)
):

    audio_bytes = await audio.read()

    if not audio_bytes:
        raise HTTPException(400, "Audio file is empty.")

    if len(audio_bytes) > 25 * 1024 * 1024:
        raise HTTPException(413, "File must be smaller than 25 MB.")

    try:
        wav_bytes = convert_to_wav(audio_bytes)
        validate_audio(wav_bytes)

        result = reduce_noise(wav_bytes)

        return Response(
            content=result["processed_audio"],
            media_type="audio/wav",
            headers={
                "Content-Disposition":
                    'attachment; filename="cleaned_audio.wav"',
                "X-Audio-Duration":
                    str(result["duration_seconds"]),
                "X-Processing-Status":
                    "Noise reduction completed"
            }
        )

    except Exception as error:
        print("NOISE REDUCTION ERROR:", repr(error))
        raise HTTPException(400, "Noise reduction failed.")


@router.post("/compare")
async def compare_original_and_cleaned_audio(
    audio: UploadFile = File(...)
):

    audio_bytes = await audio.read()

    if not audio_bytes:
        raise HTTPException(400, "Audio file is empty.")

    if len(audio_bytes) > 25 * 1024 * 1024:
        raise HTTPException(413, "File must be smaller than 25 MB.")

    try:
        wav_bytes = convert_to_wav(audio_bytes)
        duration = validate_audio(wav_bytes)

        result = reduce_noise(wav_bytes)

        comparison = compare_audio(
            original_audio_bytes=wav_bytes,
            processed_audio_bytes=result["processed_audio"]
        )

        return {
            "success": True,
            "message": "Audio comparison completed successfully.",
            "duration_seconds": duration,
            "comparison": comparison
        }

    except Exception as error:
        print("AUDIO COMPARISON ERROR:", repr(error))
        raise HTTPException(400, "Audio comparison failed.")


@router.post("/compare-transcriptions")
async def compare_original_and_processed_transcriptions(
    audio: UploadFile = File(...),
    language: str = Form("te-IN")
):

    audio_bytes = await audio.read()

    if not audio_bytes:
        raise HTTPException(400, "Audio file is empty.")

    if len(audio_bytes) > 25 * 1024 * 1024:
        raise HTTPException(413, "File must be smaller than 25 MB.")

    try:
        # Convert uploaded audio into WAV
        wav_bytes = convert_to_wav(audio_bytes)

        duration = validate_audio(wav_bytes)

        # Apply noise reduction
        noise_result = reduce_noise(wav_bytes)

        # Compare both Prisma transcriptions
        result = await compare_transcriptions(
            original_audio_bytes=wav_bytes,
            processed_audio_bytes=noise_result["processed_audio"],
            language=language
        )

        return {
            "success": True,
            "message": "Prisma transcription comparison completed.",
            "duration_seconds": duration,
            "noise_reduction": "Applied",
            "transcription_comparison": result
        }

    except Exception as error:
        print("TRANSCRIPTION COMPARISON ERROR:", repr(error))
        raise HTTPException(
            status_code=502,
            detail="Transcription comparison failed. Check backend terminal."
        )