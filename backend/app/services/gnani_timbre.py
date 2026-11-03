import httpx

from app.config import settings


GNANI_TTS_URL = "https://api.vachana.ai/api/v1/tts/inference"

TTS_MODEL = "timbre-v2.5"


# Preferred voices for supported languages
LANGUAGE_VOICES = {
    "te-IN": "Suhana",
    "hi-IN": "Nalini",
    "en-IN": "Kaveri",
    "ta-IN": "Asmita",
    "kn-IN": "Kaveri",
    "ml-IN": "Kaveri",
    "mr-IN": "Kaveri",
    "bn-IN": "Kaveri",
    "gu-IN": "Kaveri",
    "pa-IN": "Kaveri",
}


async def generate_speech(
    text: str,
    language: str = "en-IN",
    voice: str = None
):
    if not text or not text.strip():
        raise ValueError("Text cannot be empty.")

    if not settings.GNANI_API_KEY:
        raise ValueError("Gnani API key is not configured.")

    selected_voice = voice or LANGUAGE_VOICES.get(language)

    if not selected_voice:
        raise ValueError("Unsupported language or voice.")

    headers = {
        "X-API-Key-ID": settings.GNANI_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "text": text.strip(),
        "model": TTS_MODEL,
        "voice": selected_voice,
        "language": language,
        "speed": 1.0,
        "audio_config": {
            "sample_rate": 48000,
            "num_channels": 1,
            "sample_width": 2,
            "encoding": "linear_pcm",
            "container": "wav"
        }
    }

    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(
            GNANI_TTS_URL,
            headers=headers,
            json=payload
        )

        response.raise_for_status()

    if not response.content:
        raise ValueError("Gnani TTS returned empty audio.")

    return {
        "audio": response.content,
        "voice": selected_voice,
        "language": language,
        "model": TTS_MODEL,
        "content_type": "audio/wav"
    }