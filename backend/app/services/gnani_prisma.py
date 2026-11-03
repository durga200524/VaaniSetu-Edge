import httpx

from app.config import settings


GNANI_STT_URL = "https://api.vachana.ai/stt/v3"


async def transcribe_audio(
    audio_bytes: bytes,
    filename: str,
    language: str
):
    if not settings.GNANI_API_KEY:
        raise ValueError("Gnani API key is not configured.")

    headers = {
        "X-API-Key-ID": settings.GNANI_API_KEY
    }

    files = {
        "audio_file": (
            filename,
            audio_bytes,
            "audio/wav"
        )
    }

    data = {
        "language_code": language,
        "format": "transcribe",
        "itn_native_numerals": "true"
    }

    async with httpx.AsyncClient(timeout=60.0) as client:

        response = await client.post(
            GNANI_STT_URL,
            headers=headers,
            files=files,
            data=data
        )

        response.raise_for_status()

        result = response.json()

        if not result.get("success"):
            raise ValueError(
                result.get("message", "Gnani transcription failed.")
            )

        return result