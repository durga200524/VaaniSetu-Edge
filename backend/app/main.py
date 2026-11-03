from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.transcription import router as transcription_router
from app.routes.audio_analysis import router as audio_analysis_router
from app.routes.intent import router as intent_router
from app.routes.knowledge import router as knowledge_router
from app.routes.tts import router as tts_router
from app.routes.voice import router as voice_router
from app.routes.resolution import router as resolution_router
from app.routes.edge import router as edge_router


app = FastAPI(
    title="VaaniSetu Edge API",
    description=(
        "Noise-Resilient Multilingual Voice Intelligence "
        "and Edge-Assisted Resolution Platform"
    ),
    version="1.0.0"
)


# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Register API Routers
app.include_router(transcription_router)
app.include_router(audio_analysis_router)
app.include_router(intent_router)
app.include_router(knowledge_router)
app.include_router(tts_router)
app.include_router(voice_router)
app.include_router(resolution_router)
app.include_router(edge_router)


# Root Endpoint
@app.get("/")
async def root():
    return {
        "message": "Welcome to VaaniSetu Edge!",
        "project": "Noise-Resilient Multilingual Voice Intelligence Platform",
        "status": "running",
        "version": "1.0.0"
    }


# Health Check Endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "backend": "FastAPI",
        "project": "VaaniSetu Edge"
    }