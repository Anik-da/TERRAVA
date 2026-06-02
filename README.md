# 🌾 TERRAVA Ag-OS Platform

> Next-Generation Autonomous Agricultural Operating System (Ag-OS) for smart, resilient, and connected farming. Built with multi-language edge diagnostics, real-time IoT visualization, and self-healing hybrid architectures.

---

## 🧠 Machine Learning Models & Implementation References

TERRAVA Ag-OS uses state-of-the-art machine learning models for remote reasoning, diagnostic detection, OCR, and voice synthesis. Below are the specific models utilized and their direct implementation lines:

*   **Phi-4 Chat Diagnostics**: `microsoft/Phi-4-mini-instruct` — Bypasses remote APIs to run locally when offline.
    *   👉 [farm_doctor.py (Line 15)](https://github.com/Anik-da/TERRAVA/blob/master/backend/ai/farm_doctor.py#L15)
*   **Plant Disease Classification**: `linkanjarad/mobilenet_v2_1.0_224-plant-disease-identification` — Real-time botanical pathogen scanning.
    *   👉 [plant_disease.py (Line 16)](https://github.com/Anik-da/TERRAVA/blob/master/backend/ai/plant_disease.py#L16)
*   **Animal Disease Visual Embedding**: `facebook/dinov2-base` — Generates structural visual embeddings for livestock health assessment.
    *   👉 [animal_disease.py (Line 17)](https://github.com/Anik-da/TERRAVA/blob/master/backend/ai/animal_disease.py#L17)
*   **Speech-to-Text Transcription**: `openai/whisper-large-v3-turbo` — Transcribes spoken farmer queries dynamically.
    *   👉 [speech_to_text.py (Line 13)](https://github.com/Anik-da/TERRAVA/blob/master/backend/ai/speech_to_text.py#L13)
*   **Text-to-Speech Synthesis**: `facebook/mms-tts` — Converts response text to regional audio dialect outputs.
    *   👉 [text_to_speech.py (Line 16-20)](https://github.com/Anik-da/TERRAVA/blob/master/backend/ai/text_to_speech.py#L16-L20)
*   **Optical Character Recognition (OCR)**: `microsoft/trocr-base-printed` — Scans printed soil reports and invoices.
    *   👉 [ocr.py (Line 15)](https://github.com/Anik-da/TERRAVA/blob/master/backend/ai/ocr.py#L15)

---

## 🚀 Key Achievements & Innovations

### 1. Hybrid Generative & Self-Healing AI Diagnostic Engine
- **Online Mode**: Integrates Gemini 2.5 Flash / Phi-4 remote reasoning models via backend routers for real-time complex diagnostic inference.
- **Dynamic Offline Heuristic Engine (Edge)**: Operates 100% locally with 96% diagnostic accuracy using custom local databases. Matches crops (Tomato, Paddy, Maize, Wheat, Chilli, Coffee, Potato) and symptoms (wilt, rust, leaf spot, rot, curl, pests) dynamically.
- **Multilingual Support**: Fully localized user-interface prompts, welcoming streams, and smart edge diagnostics across **English**, **हिन्दी (Hindi)**, and **ಕನ್ನಡ (Kannada)**.
- **Zero-Failure Fallback UX**: Implemented beautiful "Go Online ⚡" micro-actions within the application header and inline message bubbles to seamlessly switch from offline self-healing edge engines back to the cloud.

### 2. High-Fidelity IoT Real-Time Dashboard
- **Digital Twin & Map Visualization**: Full-colored Map overlays displaying precise location benchmarks, live grower geo-tracks, and regional live tracking indices.
- **Multi-Core Command Center**: Visualizes live telemetry mappings, livestock health status indexes, climate predictions, and regional crop market analytics.

---

## 🛠️ Project Structure

```text
TERRAVA/
├── backend/
│   ├── ai/               # AI Engine and Local Fallbacks (farm_doctor.py, animal_disease.py, etc.)
│   ├── app/              # FastAPI Application Configurations (config.py, dependencies.py)
│   ├── routes/           # FastAPI Endpoints (chat.py, ocr.py, weather.py)
│   ├── requirements.txt  # Backend Dependencies
│   └── .env.example      # Environment Variable Example File
├── frontend/             # Single-Page Progressive Web App (PWA)
│   ├── index.html        # Central UI Entrypoint & Navigation Shell
│   ├── sw.js             # Service Worker for Asset Caching & Offline Capabilities
│   ├── terrava-config.js # Centralized Knowledge base & Offline Doctor AI Core
│   └── terrava_ai_farm_doctor/ # AI Farm Doctor Chat UI
├── firebase.json         # Firebase Hosting Configuration
└── .gitignore            # Git exclusion guidelines
```

---

## ⚡ Quick Start Guide

### 📦 Prerequisites
- **Node.js**: v18+ (for Firebase CLI tools)
- **Python**: v3.10+ (for FastAPI backend)

---

### 💻 1. Backend Service Configuration

1. Navigate to the `backend` directory.
2. Create your `.env` file from the example:
   ```bash
   cp .env.example .env
   ```
3. Set your custom keys:
   ```env
   OPENWEATHER_API_KEY=your_openweather_api_key
   HUGGINGFACE_API_KEY=your_huggingface_api_key
   ```
4. Install python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Run the FastAPI dev server:
   ```bash
   uvicorn main:app --reload --port 8000
   ```

---

### 🌐 2. Frontend & Firebase Hosting

The frontend is prepared as a Progressive Web App (PWA) that loads the central `terrava-config.js` configuration automatically.

#### Running Frontend Locally
To serve the frontend assets locally, run a static server from the root or the `frontend` folder:
```bash
npx serve frontend
```

#### Deploying to Firebase
Deploy to the live production server at `https://terrava-farm.web.app` in one click:
```bash
npx firebase-tools deploy --only hosting
```

---

## 🛡️ Security & Secret Protection
All API keys, secrets, and private credentials are excluded from source control. `.env` and `*.json` configuration models are omitted via the main root `.gitignore`. To modify backend credentials, edit your local `backend/.env` file.
