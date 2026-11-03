import io
import subprocess
import base64
import time

import soundfile as sf
from imageio_ffmpeg import get_ffmpeg_exe

from app.services.gnani_prisma import transcribe_audio
from app.intelligence.intent_engine import detect_intent
from app.intelligence.answer_generation import generate_answer
from app.services.gnani_timbre import generate_speech
from app.intelligence.resolution_passport import (
    create_resolution_passport
)


async def process_customer_voice(
    audio_bytes: bytes,
    language: str = "te-IN"
):
    """
    Complete VaaniSetu Edge voice-to-voice pipeline
    with Resolution Passport generation.
    """

    start_time = time.perf_counter()

    if not audio_bytes:
        raise ValueError("Audio file is empty.")

    # STEP 1: Convert uploaded audio into WAV
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

    # STEP 2: Check audio duration
    with sf.SoundFile(io.BytesIO(wav_bytes)) as wav:
        duration = len(wav) / wav.samplerate

    if duration <= 0:
        raise ValueError("No audio detected.")

    if duration > 30:
        raise ValueError("Audio duration must not exceed 30 seconds.")

    audio_analysis = {
        "duration_seconds": round(duration, 2),
        "sample_rate": 16000,
        "channels": 1,
        "format": "WAV"
    }

    # STEP 3: Speech-to-Text
    transcription_result = await transcribe_audio(
        audio_bytes=wav_bytes,
        filename="converted_audio.wav",
        language=language
    )

    transcript = transcription_result.get("transcript", "")

    if not transcript or not transcript.strip():
        raise ValueError("No speech detected in the audio.")

    # STEP 4: Intent detection
    intent_result = detect_intent(transcript)

    # STEP 5: RAG + Qwen answer generation
    answer_result = await generate_answer(transcript)

    answer = answer_result.get("answer", "")

    if not answer:
        raise ValueError("Unable to generate an answer.")

    ai_response = {
        "text": answer,
        "model": answer_result.get(
            "model", "qwen2.5:3b"
        ),
        "sources": answer_result.get("sources", [])
    }

    # STEP 6: Text-to-Speech
    speech_result = await generate_speech(
        text=answer,
        language=language
    )

    generated_audio = speech_result["audio"]

    speech_output = {
        "model": speech_result["model"],
        "voice": speech_result["voice"],
        "language": speech_result["language"],
        "audio_format": "wav"
    }

    # STEP 7: Generate Resolution Passport
    processing_time = time.perf_counter() - start_time

    passport = create_resolution_passport(
        transcript=transcript,
        language=language,
        intent_analysis=intent_result,
        ai_response=ai_response,
        speech_output=speech_output,
        audio_analysis=audio_analysis,
        processing_time_seconds=processing_time
    )

    # STEP 8: Encode generated audio
    audio_base64 = base64.b64encode(
        generated_audio
    ).decode("utf-8")

    # STEP 9: Return complete result
    return {
        "success": True,
        "pipeline": "VaaniSetu Edge Voice-to-Voice",

        "audio_analysis": audio_analysis,

        "transcription": {
            "text": transcript,
            "language": language,
            "model": "Gnani Prisma v2.5",
            "request_id": transcription_result.get("request_id")
        },

        "intent_analysis": intent_result,

        "ai_response": ai_response,

        "speech_output": {
            **speech_output,
            "audio_base64": audio_base64
        },

        "resolution_passport": {
            "passport_id": passport["passport_id"],
            "timestamp": passport["timestamp"],
            "status": passport["processing"]["status"]
        },

        "message": "Voice processing and Resolution Passport generation completed successfully."
    }