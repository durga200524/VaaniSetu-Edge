import json
import uuid
from datetime import datetime, timezone
from pathlib import Path


# Resolution Passport storage directory
BASE_DIR = Path(__file__).resolve().parents[2]

PASSPORT_DIR = BASE_DIR / "data" / "resolution_passports"

PASSPORT_DIR.mkdir(parents=True, exist_ok=True)


def create_resolution_passport(
    transcript: str,
    language: str,
    intent_analysis: dict,
    ai_response: dict,
    speech_output: dict,
    audio_analysis: dict,
    processing_time_seconds: float
):
    """
    Create and permanently save a Resolution Passport
    for a customer voice interaction.
    """

    passport_id = str(uuid.uuid4())

    timestamp = datetime.now(
        timezone.utc
    ).isoformat()

    passport = {
        "passport_id": passport_id,

        "timestamp": timestamp,

        "customer_interaction": {
            "transcript": transcript,
            "language": language,
            "audio_analysis": audio_analysis
        },

        "intent_analysis": intent_analysis,

        "ai_resolution": {
            "response": ai_response.get("text"),
            "model": ai_response.get("model"),
            "knowledge_sources": ai_response.get(
                "sources", []
            )
        },

        "speech_output": {
            "model": speech_output.get("model"),
            "voice": speech_output.get("voice"),
            "language": speech_output.get("language"),
            "audio_format": speech_output.get("audio_format")
        },

        "processing": {
            "status": "COMPLETED",
            "processing_time_seconds": round(
                processing_time_seconds, 2
            )
        }
    }

    # Save passport as JSON
    file_path = PASSPORT_DIR / f"{passport_id}.json"

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(
            passport,
            file,
            ensure_ascii=False,
            indent=4
        )

    return passport