from fastapi import APIRouter, UploadFile, File, HTTPException, Form

from app.intelligence.voice_pipeline import process_customer_voice


router = APIRouter(
    prefix="/api/v1/voice",
    tags=["Voice-to-Voice Pipeline"]
)


@router.post("/process")
async def process_voice(
    file: UploadFile = File(...),
    language: str = Form("te-IN")
):
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Audio filename is required."
        )

    audio_bytes = await file.read()

    if not audio_bytes:
        raise HTTPException(
            status_code=400,
            detail="Uploaded audio file is empty."
        )

    if len(audio_bytes) > 20 * 1024 * 1024:
        raise HTTPException(
            status_code=413,
            detail="Audio file must be smaller than 20 MB."
        )

    try:
        result = await process_customer_voice(
            audio_bytes=audio_bytes,
            language=language
        )

        if not result.get("success"):
            raise HTTPException(
                status_code=422,
                detail=result.get("message", "Voice processing failed.")
            )

        return result

    except HTTPException:
        raise

    except Exception as error:
        print("VOICE PIPELINE ERROR:", repr(error))

        raise HTTPException(
            status_code=502,
            detail="Voice-to-voice processing failed. Check backend terminal."
        )