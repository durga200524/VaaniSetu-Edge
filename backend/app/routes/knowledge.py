from pathlib import Path
import tempfile

from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel, Field

from app.intelligence.knowledge_base import (
    add_pdf_to_knowledge_base,
    search_knowledge_base
)

from app.intelligence.answer_generation import generate_answer


router = APIRouter(
    prefix="/api/v1/knowledge",
    tags=["Knowledge Base"]
)


class QuestionRequest(BaseModel):

    question: str = Field(
        ...,
        min_length=1,
        max_length=2000
    )


@router.post("/upload")
async def upload_knowledge_pdf(
    file: UploadFile = File(...)
):

    if Path(file.filename or "").suffix.lower() != ".pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported."
        )

    pdf_bytes = await file.read()

    if not pdf_bytes:
        raise HTTPException(
            status_code=400,
            detail="Uploaded PDF is empty."
        )

    if len(pdf_bytes) > 10 * 1024 * 1024:
        raise HTTPException(
            status_code=413,
            detail="PDF must be smaller than 10 MB."
        )

    try:
        with tempfile.NamedTemporaryFile(
            suffix=".pdf",
            delete=False
        ) as temporary_file:

            temporary_file.write(pdf_bytes)
            temporary_path = temporary_file.name

        try:
            result = add_pdf_to_knowledge_base(
                temporary_path
            )
        finally:
            Path(temporary_path).unlink(missing_ok=True)

        return result

    except Exception as error:
        print("KNOWLEDGE UPLOAD ERROR:", repr(error))

        raise HTTPException(
            status_code=500,
            detail="Unable to process PDF."
        )


@router.get("/search")
async def search_business_knowledge(
    query: str,
    top_k: int = 3
):

    if not query.strip():
        raise HTTPException(
            status_code=400,
            detail="Search query cannot be empty."
        )

    if top_k < 1 or top_k > 10:
        raise HTTPException(
            status_code=400,
            detail="top_k must be between 1 and 10."
        )

    try:
        results = search_knowledge_base(
            query=query,
            top_k=top_k
        )

        return {
            "success": True,
            "query": query,
            "results_count": len(results),
            "results": results
        }

    except Exception as error:
        print("KNOWLEDGE SEARCH ERROR:", repr(error))

        raise HTTPException(
            status_code=500,
            detail="Knowledge search failed."
        )


@router.post("/ask")
async def ask_business_question(
    request: QuestionRequest
):

    try:
        result = await generate_answer(
            request.question
        )

        return result

    except Exception as error:
        print("ANSWER GENERATION ERROR:", repr(error))

        raise HTTPException(
            status_code=502,
            detail="AI answer generation failed. Check backend terminal."
        )