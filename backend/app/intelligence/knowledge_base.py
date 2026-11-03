import uuid
from pathlib import Path

import chromadb
from pypdf import PdfReader


# Persistent database location
BASE_DIR = Path(__file__).resolve().parents[2]
CHROMA_DIR = BASE_DIR / "data" / "chroma_db"

# Create persistent ChromaDB client
client = chromadb.PersistentClient(
    path=str(CHROMA_DIR)
)

# Create or access knowledge collection
collection = client.get_or_create_collection(
    name="vaanisetu_business_knowledge",
    metadata={"description": "Business customer support knowledge"}
)


def extract_pdf_text(pdf_path: str):
    """Extract text from a PDF document."""

    reader = PdfReader(pdf_path)

    extracted_pages = []

    for page_number, page in enumerate(reader.pages, start=1):

        text = page.extract_text()

        if text and text.strip():

            extracted_pages.append({
                "page": page_number,
                "text": text.strip()
            })

    if not extracted_pages:
        raise ValueError(
            "No readable text found in the PDF."
        )

    return extracted_pages


def split_text(
    text: str,
    chunk_size: int = 700,
    overlap: int = 100
):
    """Split text into overlapping chunks."""

    words = text.split()

    chunks = []

    start = 0

    while start < len(words):

        end = start + chunk_size

        chunk = " ".join(words[start:end])

        if chunk.strip():
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def add_pdf_to_knowledge_base(pdf_path: str):
    """Extract, split and store PDF content."""

    pdf_path = Path(pdf_path)

    if not pdf_path.exists():
        raise FileNotFoundError(
            "PDF file does not exist."
        )

    if pdf_path.suffix.lower() != ".pdf":
        raise ValueError(
            "Only PDF documents are supported."
        )

    pages = extract_pdf_text(str(pdf_path))

    documents = []
    metadatas = []
    ids = []

    for page in pages:

        chunks = split_text(page["text"])

        for chunk in chunks:

            documents.append(chunk)

            metadatas.append({
                "source": pdf_path.name,
                "page": page["page"]
            })

            ids.append(str(uuid.uuid4()))

    if not documents:
        raise ValueError(
            "No text chunks were generated."
        )

    # Store documents in ChromaDB
    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )

    return {
        "success": True,
        "filename": pdf_path.name,
        "pages_processed": len(pages),
        "chunks_stored": len(documents),
        "message": "PDF added to knowledge base successfully."
    }


def search_knowledge_base(
    query: str,
    top_k: int = 3
):
    """Retrieve relevant business information."""

    if not query or not query.strip():
        raise ValueError(
            "Search query cannot be empty."
        )

    if collection.count() == 0:
        return []

    results = collection.query(
        query_texts=[query],
        n_results=min(top_k, collection.count())
    )

    retrieved_documents = []

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    for document, metadata, distance in zip(
        documents,
        metadatas,
        distances
    ):

        retrieved_documents.append({
            "text": document,
            "source": metadata.get("source"),
            "page": metadata.get("page"),
            "distance": round(float(distance), 4)
        })

    return retrieved_documents