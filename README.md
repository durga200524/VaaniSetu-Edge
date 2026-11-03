VaaniSetu Edge

Noise-Resilient Multilingual Voice Intelligence and Edge-Assisted Resolution Platform for Indian Small Businesses

VaaniSetu Edge is a multilingual AI-powered voice intelligence platform designed to help Indian small businesses handle customer queries through voice.

The platform accepts customer audio, converts speech into text, identifies customer intent, retrieves relevant business information, generates an AI-powered response, and converts the response into speech.

It integrates Gnani AI's Prisma v2.5 Speech-to-Text (STT) and Timbre v2.5 Text-to-Speech (TTS) services with a local Qwen2.5 language model and a ChromaDB-based knowledge retrieval system.

The project also includes noise-resilient audio analysis, Resolution Passports for tracking interactions, and a software-based edge constraint simulator.

1. Problem Statement

Many small businesses in India receive customer queries in different Indian languages and through voice communication.

Some common challenges include:

Language barriers between customers and businesses.

Difficulty understanding customer voice queries.

Background noise affecting speech recognition.

Difficulty retrieving accurate business information quickly.

Limited access to affordable AI-powered customer support.

Resource limitations when deploying AI applications on edge devices.

VaaniSetu Edge aims to address these challenges through a multilingual voice intelligence and AI-assisted resolution platform.

2. Project Objectives

The main objectives are:

Develop a multilingual voice-based customer support platform.

Convert customer speech into text using AI-based speech recognition.

Analyze audio quality and reduce background noise.

Identify customer intent from transcribed speech.

Retrieve relevant information from business documents.

Generate contextual responses using a local language model.

Convert AI-generated responses into speech.

Maintain a record of completed customer interactions.

Simulate edge-device resource constraints.

3. Key Features

3.1 Multilingual Speech Recognition

Uses Gnani Prisma v2.5.

Converts customer audio into text.

Provides English, Hindi, and Telugu language selections.

Accepts common audio formats, including MP3, WAV, MP4, M4A, OGG, and WEBM.

3.2 Noise-Resilient Audio Intelligence

Analyzes uploaded audio quality.

Measures RMS volume, peak amplitude, clipping, silence, and duration.

Performs background noise reduction.

Generates cleaned audio for playback and download.

Compares original and processed audio metrics.

Compares original and processed speech recognition results.

3.3 Customer Intent Recognition

Identifies the purpose of a customer's query.

Supported intent categories include:

ORDER_TRACKING

PRODUCT_RETURN

PAYMENT_ISSUE

PRODUCT_INFORMATION

ACCOUNT_SUPPORT

CUSTOMER_SUPPORT

UNKNOWN

The current intent engine uses keyword-based matching.

3.4 Knowledge Base and RAG

The platform uses Retrieval-Augmented Generation (RAG) to provide answers based on business documents.

Technologies:

ChromaDB for vector storage and retrieval.

PDF ingestion for business knowledge.

Qwen2.5 local LLM for answer generation.

Workflow:

Upload a business PDF.

Extract text from the document.

Divide the content into smaller chunks.

Store the chunks in ChromaDB.

Retrieve relevant information when a customer asks a question.

Generate an answer using the retrieved context.

The system is designed to avoid inventing business information that is not available in its knowledge base.

3.5 Multilingual Speech Generation

Uses Gnani Timbre v2.5.

Converts AI-generated text into speech.

Uses configured English, Hindi, and Telugu voices.

Returns generated audio for playback.

3.6 Complete Voice Processing Pipeline

The main voice processing pipeline combines multiple AI components.

Processing Workflow:

Customer Audio → Audio Conversion and Analysis → Speech Recognition → Intent Detection → Knowledge Retrieval → AI Answer Generation → Speech Generation → Resolution Passport

The pipeline returns the transcription, detected intent, generated answer, speech output, and interaction record.

3.7 Resolution Passport

Each processed customer interaction can generate a Resolution Passport.

It records information such as:

Unique passport ID.

Interaction timestamp.

Customer transcript.

Selected language.

Detected customer intent.

AI-generated response.

Knowledge sources.

Speech generation details.

Processing status.

Processing time.

Resolution Passports help maintain a history of customer interactions and their outcomes.

3.8 Edge Constraint Simulator

The platform includes a software-based edge resource simulator.

It allows users to configure:

Available RAM.

CPU cores.

Network latency.

Network bandwidth.

Internet connectivity.

It evaluates the configured conditions and provides resource assessments and recommendations.

Important: This is a software simulation. Physical edge hardware deployment and actual hardware resource measurement have not been implemented.

5. Application Screenshots

4.1 Main Dashboard

4.2 Voice Assistant

4.3 Complete Voice Processing Pipeline

4.4 Resolution History

4.5 Edge Constraint Simulator

4.6 Audio Quality Analysis

4.7 Noise-Reduced Audio

4.8 Noise Reduction Comparison

6. System Architecture

The platform follows a frontend-backend architecture.

                    CUSTOMER
                       |
                       |
                 FRONTEND UI
              React + TypeScript
                       |
                       |
                FASTAPI BACKEND
                       |
             -----------------------
             |          |          |
             |          |          |
          AUDIO       SPEECH    INTELLIGENCE
        PROCESSING   SERVICES     MODULES
             |          |          |
          Noise       Gnani       Intent
         Reduction    Prisma    Recognition
         Analysis      STT         |
                                  RAG
                                   |
                                ChromaDB
                                   |
                                Qwen2.5
                                   |
                            Answer Generation
             -----------------------
                       |
                 Gnani Timbre
                     TTS
                       |
                GENERATED SPEECH
                       |
                RESOLUTION PASSPORT
                       |
                 DASHBOARD HISTORY

6. Technology Stack

Component

Technology

Frontend

React.js

Programming Language

TypeScript

Frontend Build Tool

Vite

Styling

CSS3

API Communication

Axios

Backend

Python, FastAPI

Speech Recognition

Gnani Prisma v2.5

Speech Generation

Gnani Timbre v2.5

Local Language Model

Qwen2.5

Vector Database

ChromaDB

PDF Processing

PyPDF

Audio Processing

FFmpeg, NumPy, SoundFile

Data Storage

JSON-based Resolution Passport files

Development Tools

VS Code, Git

7. Project Structure

VaaniSetu-Edge/
│
├── backend/
│ │
│ ├── app/
│ │ ├── routes/
│ │ │ ├── transcription.py
│ │ │ ├── audio_analysis.py
│ │ │ ├── intent.py
│ │ │ ├── knowledge.py
│ │ │ ├── tts.py
│ │ │ ├── voice.py
│ │ │ ├── resolution.py
│ │ │ └── edge.py
│ │ │
│ │ ├── services/
│ │ │ ├── gnani_prisma.py
│ │ │ ├── transcription_comparison.py
│ │ │ └── gnani_timbre.py
│ │ │
│ │ ├── audio/
│ │ │ ├── audio_analysis.py
│ │ │ ├── noise_reduction.py
│ │ │ └── audio_metrics.py
│ │ │
│ │ ├── intelligence/
│ │ │ ├── intent_engine.py
│ │ │ ├── voice_pipeline.py
│ │ │ ├── knowledge_base.py
│ │ │ ├── answer_generation.py
│ │ │ ├── resolution_passport.py
│ │ │ └── edge_simulator.py
│ │ │
│ │ ├── database/
│ │ ├── config.py
│ │ └── main.py
│ │
│ ├── data/
│ │ ├── chroma_db/
│ │ └── resolution_passports/
│ │
│ └── .env # Local secret; do not commit
│
├── docs/
│ ├── architecture.md
│ └── screenshots/
│ ├── dashboard.png
│ ├── voice-assistant.png
│ ├── voice-processing-result.png
│ ├── resolution-history.png
│ ├── edge-simulator.png
│ ├── audio-quality-analysis.png
│ ├── noise-reduced-audio.png
│ └── noise-reduction-comparison.png
│
├── frontend/
│ │
│ ├── public/
│ ├── src/
│ │ ├── api/
│ │ ├── components/
│ │ ├── App.tsx
│ │ ├── App.css
│ │ ├── index.css
│ │ └── main.tsx
│ │
│ ├── package.json
│ └── README.md
│
├── .gitignore
└── README.md

The structure above is an overview. Local environment files, virtual environments, and generated database files should not be committed to the repository.

---

## 8. Installation and Setup

### Prerequisites

Install the following:

- Python 3.12
- Node.js
- npm
- Visual Studio Code
- Git
- Ollama
- Qwen2.5 model
- Gnani AI API access

### Step 1: Clone the Repository

```bash
git clone https://github.com/durga200524/VaaniSetu-Edge.git

Navigate to the project:

cd VaaniSetu-Edge

Step 2: Backend Setup

Navigate to the backend folder:

cd backend

Create a virtual environment if one does not already exist:

python -m venv venv

Activate the virtual environment in Windows PowerShell:

.\venv\Scripts\Activate.ps1

Install the backend packages used by the project. A backend dependency file is not currently included in this repository, so a reproducible one-command installation is a future documentation improvement.

Step 3: Configure Environment Variables

Create a .env file inside the backend directory.

Add your Gnani API key:

GNANI_API_KEY=your_gnani_api_key

Use your own valid API key.

Security: Never upload .env files, API keys, or other credentials to GitHub.

Step 4: Start the Backend

From the backend directory, run:

uvicorn app.main:app --reload

Backend URL:

http://127.0.0.1:8000

API documentation:

http://127.0.0.1:8000/docs

Health check:

http://127.0.0.1:8000/health

Step 5: Start the Local LLM

Make sure Ollama is installed and running.

Download the Qwen2.5 model used by the application:

ollama pull qwen2.5:3b

The local model must be available for AI answer generation.

Step 6: Frontend Setup

Open another terminal and navigate to the frontend directory:

cd frontend

Install dependencies:

npm install

Start the frontend:

npm run dev

Frontend URL:

http://localhost:5173/

9. Backend API Endpoints

Feature

Method

Endpoint

Health Check

GET

/health

Speech Transcription

POST

/api/v1/transcription/transcribe

Audio Analysis

POST

/api/v1/audio/analyze

Noise Reduction

POST

/api/v1/audio/reduce-noise

Audio Comparison

POST

/api/v1/audio/compare

Transcription Comparison

POST

/api/v1/audio/compare-transcriptions

Intent Detection

POST

/api/v1/intelligence/intent

Voice Intent Detection

POST

/api/v1/intelligence/voice-intent

Knowledge Upload

POST

/api/v1/knowledge/upload

Knowledge Search

GET

/api/v1/knowledge/search

Knowledge-based Answer

POST

/api/v1/knowledge/ask

Speech Generation

POST

/api/v1/tts/generate

Complete Voice Pipeline

POST

/api/v1/voice/process

Resolution History

GET

/api/v1/resolution/all

Individual Resolution

GET

/api/v1/resolution/{passport_id}

Edge Simulation

POST

/api/v1/edge/simulate

10. Supported Languages

The application provides language selections for:

Language

Language Code

English

en-IN

Hindi

hi-IN

Telugu

te-IN

Full end-to-end language quality and accuracy require further evaluation across different speakers, accents, and audio conditions.

11. Testing and Validation

The following integrations and features have been tested during development:

Backend health check.

Gnani Prisma v2.5 speech recognition.

Audio quality analysis.

Background noise reduction.

Original and processed audio comparison.

Speech transcription comparison.

Customer intent detection.

PDF upload and knowledge retrieval.

Qwen2.5 answer generation.

Gnani Timbre v2.5 speech generation.

Complete voice processing pipeline.

Resolution Passport creation and retrieval.

Frontend and backend integration.

Dashboard statistics and interaction history.

Edge constraint simulation under different resource conditions.

12. Current Limitations

Physical edge hardware deployment has not been implemented.

The edge simulator is software-based.

Noise reduction requires more evaluation using real-world noisy recordings.

Transcription accuracy requires testing against independently verified reference transcripts.

Telugu answer generation quality from the local LLM needs improvement.

Complete offline voice processing has not been established.

Intent recognition currently uses keyword-based matching.

Additional testing is required across different Indian languages and regional accents.

13. Future Enhancements

Real-time microphone-based voice interaction.

Improved multilingual intent recognition.

Better background noise suppression.

Improved local LLM response quality.

Optimized inference for resource-constrained devices.

Physical deployment on Raspberry Pi or other edge hardware.

Offline speech and knowledge processing.

Support for additional Indian languages.

More extensive performance and accuracy benchmarking.

Integration with business customer support systems.

14. Project Information

Category

Details

Project Name

VaaniSetu Edge

Project Domain

Artificial Intelligence and Generative AI

Project Category

Voice AI and Edge Computing

Frontend

React.js, TypeScript, Vite

Backend

Python, FastAPI

STT

Gnani Prisma v2.5

TTS

Gnani Timbre v2.5

Local LLM

Qwen2.5

Vector Database

ChromaDB

Audio Processing

FFmpeg, NumPy, SoundFile

Languages

English, Hindi, Telugu

Application Type

Software-based AI platform

14. Project Objective – Final Summary

VaaniSetu Edge aims to make AI-powered customer communication more accessible to Indian small businesses.

By combining multilingual speech recognition, noise-resilient audio processing, customer intent detection, document-based knowledge retrieval, local language model inference, and speech generation, the platform provides an integrated voice-based customer support workflow.

The project explores how voice intelligence and edge-assisted software design can help businesses improve customer communication while considering limited computing and network resources.
```
