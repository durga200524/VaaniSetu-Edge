# VaaniSetu Edge – Frontend

### Noise-Resilient Multilingual Voice Intelligence and Edge-Assisted Resolution Platform

VaaniSetu Edge is a multilingual AI-powered voice intelligence platform designed to help Indian small businesses understand customer voice queries, identify customer intent, retrieve relevant business information, and generate spoken responses.

This folder contains the frontend application built using React, TypeScript, and Vite.

---

## 1. Technology Stack

| Technology   | Purpose                           |
| ------------ | --------------------------------- |
| React.js     | Frontend UI development           |
| TypeScript   | Type-safe JavaScript              |
| Vite         | Development server and build tool |
| CSS3         | Styling and responsive design     |
| Axios        | Backend API communication         |
| Lucide React | Icons                             |
| Recharts     | Data visualization                |

---

## 2. Main Features

### Dashboard

- Displays total customer voice interactions.
- Shows supported languages.
- Displays completed resolutions.
- Shows backend connection status.
- Provides an overview of the AI processing pipeline.
- Displays the five most recent customer interactions.

### Voice Assistant

- Upload customer audio files.
- Supports MP3, WAV, MP4, M4A, OGG, and WEBM formats.
- Supports English, Hindi, and Telugu.
- Sends audio to the backend for processing.
- Displays speech transcription.
- Displays detected customer intent.
- Shows AI-generated answers.
- Plays generated speech.
- Displays the Resolution Passport.

### Noise-Resilient Audio Intelligence

- Analyzes audio quality.
- Displays audio metrics such as duration, sample rate, RMS volume, peak amplitude, clipping, and silence.
- Reduces background noise.
- Allows users to play and download cleaned audio.
- Compares original and processed audio.
- Compares speech recognition results.

### Resolution History

- Displays previously processed customer interactions.
- Shows Resolution Passport IDs.
- Displays customer transcripts and detected intents.
- Shows AI-generated responses.
- Displays processing status and timestamps.

### Edge Constraint Simulator

- Simulates different device resource conditions.
- Allows users to configure available RAM.
- Allows users to configure CPU cores.
- Allows users to configure network latency.
- Allows users to configure network bandwidth.
- Simulates online and offline conditions.
- Displays resource assessments, limitations, and recommendations.

**Note:** The Edge Simulator is software-based. It simulates resource constraints and does not physically modify or measure actual hardware resources.

---

## 3. Project Structure

```text
frontend/
│
├── public/
│
├── src/
│   │
│   ├── api/
│   │   ├── client.ts
│   │   ├── health.ts
│   │   ├── voice.ts
│   │   ├── resolution.ts
│   │   └── edge.ts
│   │
│   ├── components/
│   │   ├── VoiceAssistant.tsx
│   │   ├── VoiceAssistant.css
│   │   ├── ResolutionHistory.tsx
│   │   ├── ResolutionHistory.css
│   │   ├── EdgeSimulator.tsx
│   │   └── EdgeSimulator.css
│   │
│   ├── App.tsx
│   ├── App.css
│   ├── index.css
│   └── main.tsx
│
├── index.html
├── package.json
├── package-lock.json
├── tsconfig.json
├── vite.config.ts
└── README.md
```

---

## 4. Requirements

Install the following before running the frontend:

- Node.js
- npm
- Visual Studio Code (recommended)
- Running VaaniSetu Edge backend

---

## 5. Installation

Open a terminal inside the frontend directory:

```bash
cd frontend
```

Install the required dependencies:

```bash
npm install
```

---

## 6. Run the Frontend

Start the Vite development server:

```bash
npm run dev
```

Open the application in your browser:

**Frontend URL:** http://localhost:5173/

---

## 7. Backend Connection

The frontend communicates with the FastAPI backend using Axios.

**Backend base URL:**

```text
http://127.0.0.1:8000
```

The Axios client is configured in:

```text
src/api/client.ts
```

Before using the frontend, make sure the backend is running.

Start the backend from the backend directory:

```bash
uvicorn app.main:app --reload
```

**Backend API documentation:**

http://127.0.0.1:8000/docs

**Backend health check:**

http://127.0.0.1:8000/health

---

## 8. API Integration

The frontend communicates with the following backend endpoints:

| Feature                     | API Endpoint                              |
| --------------------------- | ----------------------------------------- |
| Backend Health              | GET /health                               |
| Voice Processing            | POST /api/v1/voice/process                |
| Retrieve Resolution History | GET /api/v1/resolution/all                |
| Edge Simulation             | POST /api/v1/edge/simulate                |
| Audio Quality Analysis      | POST /api/v1/audio/analyze                |
| Noise Reduction             | POST /api/v1/audio/reduce-noise           |
| Audio Comparison            | POST /api/v1/audio/compare                |
| Transcription Comparison    | POST /api/v1/audio/compare-transcriptions |

---

## 9. Supported Languages

The platform currently supports:

- English (en-IN)
- Hindi (hi-IN)
- Telugu (te-IN)

---

## 10. Build for Production

To create an optimized production build:

```bash
npm run build
```

To preview the production build locally:

```bash
npm run preview
```

---

## 11. Testing

The following frontend integrations have been tested:

- Backend health monitoring.
- Audio file upload.
- Multilingual voice processing.
- Speech transcription display.
- Customer intent display.
- AI-generated answer display.
- Generated speech playback.
- Resolution Passport display.
- Audio quality analysis.
- Noise reduction and cleaned audio playback.
- Audio comparison.
- Transcription comparison.
- Resolution History retrieval.
- Dashboard statistics.
- Edge constraint simulation.

---

## 12. Current Limitations

- The Edge Simulator is software-based; physical hardware deployment has not been implemented.
- Noise reduction requires further evaluation across different real-world noise environments.
- Transcription accuracy needs additional evaluation using independently verified reference transcripts.
- Telugu answer generation quality from the local LLM requires further improvement.
- Complete offline voice processing has not yet been established.

---

## 13. Future Enhancements

- Real-time microphone-based voice interaction.
- Improved multilingual intent recognition.
- Better noise suppression for challenging environments.
- Optimized local inference.
- Deployment on Raspberry Pi or other edge hardware.
- Offline knowledge retrieval and response capabilities.
- Expanded support for Indian languages.
- Performance benchmarking on resource-constrained devices.

---

## 14. Project Information

| Category             | Details                                        |
| -------------------- | ---------------------------------------------- |
| Project Name         | VaaniSetu Edge                                 |
| Project Category     | AI / Generative AI / Voice AI / Edge Computing |
| Frontend             | React.js, TypeScript, Vite                     |
| Backend              | Python, FastAPI                                |
| Speech Recognition   | Gnani Prisma v2.5                              |
| Speech Generation    | Gnani Timbre v2.5                              |
| Knowledge Retrieval  | ChromaDB                                       |
| AI Answer Generation | Qwen2.5 Local LLM                              |
| Audio Processing     | FFmpeg, NumPy, SoundFile                       |
| Project Type         | Software-based AI platform                     |

---

## Project Objective

The objective of VaaniSetu Edge is to provide an accessible multilingual voice intelligence solution for Indian small businesses.

The frontend provides an interface for audio upload, speech processing, customer intent detection, AI-generated responses, speech output, resolution tracking, noise analysis, and software-based edge constraint simulation.

---

**VaaniSetu Edge – Making multilingual customer communication smarter and more accessible.**
