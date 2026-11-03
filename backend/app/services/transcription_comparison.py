import re
from difflib import SequenceMatcher

from app.services.gnani_prisma import transcribe_audio


def normalize_text(text: str) -> str:
    """Normalize text before comparing transcripts."""

    text = text.lower().strip()
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"\s+", " ", text)

    return text


def compare_texts(original_text: str, processed_text: str):
    """Compare two transcripts using text similarity."""

    original_normalized = normalize_text(original_text)
    processed_normalized = normalize_text(processed_text)

    similarity = SequenceMatcher(
        None,
        original_normalized.split(),
        processed_normalized.split()
    ).ratio() * 100

    original_words = original_normalized.split()
    processed_words = processed_normalized.split()

    return {
        "similarity_percentage": round(similarity, 2),
        "original_word_count": len(original_words),
        "processed_word_count": len(processed_words),
        "transcripts_match": (
            original_normalized == processed_normalized
        )
    }


async def compare_transcriptions(
    original_audio_bytes: bytes,
    processed_audio_bytes: bytes,
    language: str = "te-IN"
):
    """Transcribe both audio versions using Gnani Prisma."""

    # Transcribe original audio
    original_result = await transcribe_audio(
        audio_bytes=original_audio_bytes,
        filename="original_audio.wav",
        language=language
    )

    # Transcribe noise-reduced audio
    processed_result = await transcribe_audio(
        audio_bytes=processed_audio_bytes,
        filename="processed_audio.wav",
        language=language
    )

    original_transcript = original_result.get(
        "transcript", ""
    )

    processed_transcript = processed_result.get(
        "transcript", ""
    )

    if not original_transcript or not processed_transcript:
        raise ValueError(
            "Gnani Prisma returned an empty transcript."
        )

    comparison = compare_texts(
        original_transcript,
        processed_transcript
    )

    return {
        "success": True,
        "model": "Gnani Prisma v2.5",
        "language": language,

        "original_transcription": {
            "transcript": original_transcript,
            "request_id": original_result.get("request_id")
        },

        "processed_transcription": {
            "transcript": processed_transcript,
            "request_id": processed_result.get("request_id")
        },

        "comparison": comparison,

        "evaluation_note": (
            "Transcript similarity measures agreement between "
            "the two outputs. Ground-truth transcription is "
            "required to determine which version is more accurate."
        )
    }