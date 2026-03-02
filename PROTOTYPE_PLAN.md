# RepCon Voice Agent - Detailed Prototyping Plan

## Version: 3.0 (Comprehensive)
## Updated: 2026-03-02

---

# TABLE OF CONTENTS

1. [Executive Summary](#executive-summary)
2. [Constraints & Requirements](#constraints--requirements)
3. [Research: Open Source Solutions](#research--open-source-solutions)
4. [Recommended Tech Stack](#recommended-tech-stack)
5. [Architecture](#architecture)
6. [Detailed Implementation Plan](#detailed-implementation-plan)
7. [Code Structure](#code-structure)
8. [Database Schema](#database-schema)
9. [Voice Pipeline Flow](#voice-pipeline-flow)
10. [Multi-Language Support](#multi-language-support)
11. [Phone Number & Telephony](#phone-number--telephony)
12. [Google Sheets Integration](#google-sheets-integration)
13. [Admin Dashboard](#admin-dashboard)
14. [Security & Compliance](#security--compliance)
15. [Monitoring & Logging](#monitoring--logging)
16. [Testing Checklist](#testing-checklist)
17. [CI/CD Pipeline](#cicd-pipeline)
18. [Cost Analysis](#cost-analysis)
19. [Risk Analysis](#risk-analysis)
20. [Success Metrics](#success-metrics)
21. [Next Steps](#next-steps)

---

## 1. Executive Summary

**RepCon (Representation Consultant)** is an AI-powered voice agent system designed for small-scale educational institutes in India. It automates inbound inquiries, operates 24/7/365, and replaces manual telecallers.

### Key Value Propositions

| Feature | Before (Manual) | After (RepCon) |
|---------|-----------------|----------------|
| **Availability** | 8 hours/day | 24/7/365 |
| **Concurrent Calls** | 1-2 | Unlimited |
| **Response Time** | Minutes | <2 seconds |
| **Cost/Month** | ₹15,000-30,000 | ₹2,000-3,000 |
| **Lead Capture** | Manual entry | Automatic |
| **Follow-up** | Missed often | Instant |

### Target Market

- **Primary:** Small-scale coaching centers in India
- **Secondary:** Tuition centers, vocational training institutes
- **Tertiary:** Online course providers

---

## 2. Constraints & Requirements

| Constraint | Value |
|------------|-------|
| **Target Institutes** | Small-scale educational institutes in India |
| **Budget/Institute** | 30-50k INR/month (~$350-600) |
| **Availability** | 24/7/365 (replaces 8hr manual telecallers) |
| **Approach** | Single institute prototype → Scale to 100 |
| **Tech Preference** | Open source maximum for STT/TTS/LLM |
| **Languages** | English, Hindi, Telugu, Urdu, Tamil, Kannada |
| **Data Storage** | India (data localization) |
| **Uptime Target** | 99.9% |

### Load Volume Requirements (CRITICAL)

| Metric | Value | Notes |
|--------|-------|-------|
| **Calls per Institute/Day** | 150 calls | Expected inbound volume |
| **Avg Call Duration** | 5 minutes | Per call |
| **Total Minutes/Day** | 750 minutes | 150 × 5 |
| **Peak Concurrent Calls** | 15-20 | During peak hours (9AM-12PM, 5PM-8PM) |
| **Calls per Month** | ~4,500 calls | 150 × 30 days |
| **Minutes per Month** | ~22,500 minutes | 750 × 30 days |

### Capacity Planning

| Load Level | GPU Requirements | Concurrent Streams |
|------------|------------------|-------------------|
| **Single Institute** | 1x NVIDIA T4 (16GB) | 10-15 parallel |
| **10 Institutes** | 1x NVIDIA A100 (40GB) | 100-150 parallel |
| **100 Institutes** | 3x NVIDIA A100 (40GB) | 1000+ parallel |

### Functional Requirements

1. **Inbound Call Handling**
   - Answer calls automatically
   - Greet caller with institute-specific message
   - Understand caller intent

2. **Course Information**
   - Provide course details (duration, fee, syllabus)
   - Answer FAQs about job opportunities
   - Share eligibility criteria

3. **Lead Capture**
   - Collect: Name, Phone, Email
   - Record: Course interest, source
   - Store in database

4. **Multi-language Support**
   - Auto-detect caller language
   - Respond in same language
   - Support 6 Indian languages

5. **Admin Dashboard**
   - View leads in real-time
   - Filter by date, course, status
   - Export reports

6. **Call Logging**
   - Record call duration
   - Store transcripts (optional)
   - Track outcomes

---

## 3. Research: Open Source Solutions

### 1. Axiom Voice Agent ⭐ (RECOMMENDED)

| Attribute | Details |
|-----------|---------|
| **Repository** | https://github.com/pheonix-delta/axiom-voice-agent |
| **STT** | Sherpa-ONNX Parakeet (200MB, <100ms) |
| **TTS** | Kokoro TTS (Sherpa-ONNX) |
| **VAD** | Silero VAD |
| **LLM** | Ollama (local) or fallback to templates |
| **Latency** | <400ms |
| **VRAM** | 4GB (GTX 1650 compatible) |
| **License** | Apache 2.0 |
| **Cost** | FREE (self-hosted) |

### 2. BentoVoice Agent

| Attribute | Details |
|-----------|---------|
| **Repository** | https://github.com/bentoml/BentoVoiceAgent |
| **STT** | Whisper |
| **TTS** | XTTS |
| **LLM** | Llama 3.1 |
| **Cost** | FREE (self-hosted) |

### 3. STIMM - Open Source Voice Agent Platform

| Attribute | Details |
|-----------|---------|
| **Repository** | https://github.com/stimm-ai/stimm |
| **Built on** | LiveKit Agents |
| **License** | MIT |

---

## 4. Recommended Tech Stack

### For Single Institute Prototype

| Component | Technology | Version | Cost | Notes |
|-----------|------------|---------|------|-------|
| **STT** | faster-whisper | latest | FREE | Use large-v3 for Indic languages |
| **TTS** | Kokoro TTS | latest | FREE | Indian language voices |
| **VAD** | Silero VAD | latest | FREE | Best open source VAD |
| **LLM** | Ollama + Llama 3.2 | 0.5+ | FREE | Run locally on GPU |
| **Phone** | Twilio | - | $1-5/mo | VoIP DID number |
| **Server** | Single GPU VPS | - | $20-30/mo | NVIDIA T4/P40 |
| **Database** | PostgreSQL | 15+ | $5-10/mo | or SQLite for prototype |
| **Cache** | Redis | 7+ | FREE | For session management |
| **API** | FastAPI | 0.100+ | FREE | Python web framework |
| **Frontend** | React + Vite | 5+ | FREE | Admin dashboard |

### Technology Rationale

#### Why faster-whisper?
- **Open source:** ✅
- **GPU-accelerated:** ✅
- **Multi-language:** ✅ (100+ languages including all 6 Indian)
- **Models:** small (75MB), base (140MB), large-v3 (3GB)
- **Latency:** 300-500ms

#### Why Kokoro TTS?
- **Open source:** ✅
- **Indian voices:** ✅ (Hindi, Tamil, Telugu, etc.)
- **Low latency:** <200ms
- **Natural quality:** ⭐⭐⭐⭐
- **License:** Apache 2.0

#### Why Ollama + Llama 3.2?
- **Open source:** ✅
- **Local inference:** ✅ (data privacy)
- **VRAM efficient:** 1B (2GB), 3B (6GB)
- **Multilingual:** ✅
- **Fast inference:** ✅

#### Why Twilio?
- **Reliability:** Industry-leading
- **India DID numbers:** ✅
- **Webhook support:** ✅
- **Python SDK:** ✅
- **Recording:** Optional

---

## 5. Architecture

### 5.1 Single Institute Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        TWILIO / VoIP.ms                          │
│                     (Inbound Phone Calls)                         │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      FASTAPI BACKEND                             │
│                        (Port 8000)                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│  │   Webhooks   │───▶│   Voice      │───▶│    LLM       │      │
│  │  (Twilio)    │    │   Pipeline   │    │   Handler    │      │
│  └──────────────┘    └──────┬───────┘    └──────────────┘      │
│                             │                                     │
│         ┌───────────────────┼───────────────────┐               │
│         ▼                   ▼                   ▼               │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐       │
│  │     STT      │    │     TTS     │    │     VAD      │       │
│  │  (Whisper)   │    │   (Kokoro)  │    │   (Silero)   │       │
│  └──────────────┘    └──────────────┘    └──────────────┘       │
│                                                                  │
└────────────────────────────┬────────────────────────────────────┘
                             │
         ┌───────────────────┼───────────────────┐
         ▼                   ▼                   ▼
  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
  │  PostgreSQL  │    │    Redis     │    │     GCS      │
  │  (Database)  │    │    (Cache)   │    │   (Sheets)   │
  └──────────────┘    └──────────────┘    └──────────────┘
```

### 5.2 Multi-Tenant Architecture (100 Institutes)

```
┌─────────────────────────────────────────────────────────────┐
│                     LOAD BALANCER                            │
│                    (Nginx / Traefik)                        │
│                     1 IP, Port 443                          │
└─────────────────────────┬───────────────────────────────────┘
                          │
         ┌────────────────┼────────────────┐
         ▼                ▼                ▼
    ┌─────────┐      ┌─────────┐      ┌─────────┐
    │  API    │      │  API    │      │  API    │
    │ Gateway │      │ Gateway │      │ Gateway │
    │ (10 inst)     │(10 inst)      │(10 inst)     │
    └────┬────┘      └────┬────┘      └────┬────┘
         │                │                │
    ┌────┴────┐      ┌────┴────┐      ┌────┴────┐
    │ GPU 1   │      │ GPU 2   │      │ GPU 3   │
    │ A100 40G│      │ A100 40G│      │ A100 40G│
    └─────────┘      └─────────┘      └─────────┘
         │                │                │
         └────────────────┼────────────────┘
                          │
                    ┌─────▼─────┐
                    │ PostgreSQL│
                    │  Primary  │
                    └───────────┘
```

### 5.3 Voice Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      CALL START                                  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                  SILERO VAD                                      │
│            (Voice Activity Detection)                            │
│  - Detects speech vs silence                                    │
│  - Segments audio chunks                                        │
│  - 50ms chunks                                                 │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                  LANGUAGE DETECTION                              │
│            (fasttext / langdetect)                               │
│  - Detects: en, hi, te, ur, ta, kn                             │
│  - Returns language code                                        │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                  WHISPER STT                                     │
│            (faster-whisper large-v3)                             │
│  - Transcribes audio to text                                   │
│  - Uses detected language                                      │
│  - Returns: text, confidence                                    │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                  INTENT CLASSIFICATION                           │
│            (Rule-based + LLM)                                    │
│  - Course inquiry                                              │
│  - Fee inquiry                                                 │
│  - Admission inquiry                                           │
│  - Complaint/Other                                             │
│  - Lead capture                                                │
└────────────────────────────┬────────────────────────────────────┘
                             │
         ┌───────────────────┼───────────────────┐
         ▼                   ▼                   ▼
   ┌───────────┐      ┌───────────┐      ┌───────────┐
   │  Google   │      │   Lead    │      │  Callback │
   │  Sheets   │      │  Capture  │      │ Scheduler │
   │   (FAQ)   │      │           │      │           │
   └───────────┘      └───────────┘      └───────────┘
         │                   │                   │
         └───────────────────┼───────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                  OLLAMA LLM                                      │
│            (Llama 3.2 1B/3B)                                    │
│  - Generates context-aware response                             │
│  - Uses system prompt with course data                          │
│  - Returns: response text                                       │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                  LANGUAGE MAPPING                                │
│  - Map detected language to TTS voice                            │
│  - en: af_sarah, hi: hf_psharma, ta: hf_tamil                  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                  KOKORO TTS                                      │
│            (Text-to-Speech)                                     │
│  - Converts text to audio                                       │
│  - Uses language-specific voice                                 │
│  - Returns: audio bytes (WAV/MP3)                               │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                  AUDIO STREAM                                    │
│            (Twilio Media Stream)                                │
│  - Streams audio back to caller                                 │
│  - Chunked for low latency                                      │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                  CALL END                                        │
│  - Log call details to database                                 │
│  - Save lead (if captured)                                      │
│  - Send notifications (if configured)                           │
└─────────────────────────────────────────────────────────────────┘
```

---

## 6. Detailed Implementation Plan

### Phase 1: Foundation (Week 1)

#### Day 1-2: Infrastructure Setup

| Task | Command/Action |
|------|----------------|
| Create VPS | Provision 1x GPU VPS (NVIDIA T4/A100) |
| Install Docker | `curl -fsSL https://get.docker.com | sh` |
| Install NVIDIA | `apt install nvidia-driver-535 nvidia-container-toolkit` |
| Setup Docker Compose | Create docker-compose.yml |
| Pull images | postgres:15, redis:7, python:3.11 |

**Docker Compose Services:**
```yaml
version: '3.8'
services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: repcon
      POSTGRES_USER: repcon
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://repcon:${DB_PASSWORD}@postgres:5432/repcon
      - REDIS_URL=redis://redis:6379
      - OLLAMA_BASE_URL=http://ollama:11434
    depends_on:
      - postgres
      - redis
      - ollama

  ollama:
    image: ollama/ollama:latest
    volumes:
      - ollama_data:/root/.ollama
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
```

#### Day 3-4: Core Voice Pipeline

| Task | Implementation |
|------|----------------|
| FastAPI setup | Create main.py with endpoints |
| Twilio webhook | `/webhooks/twilio voice` endpoint |
| STT handler | Implement faster-whisper integration |
| TTS handler | Implement Kokoro TTS integration |
| VAD integration | Add Silero VAD for voice detection |
| LLM handler | Connect Ollama API |
| Audio streaming | Implement Twilio Media Stream |

**Voice Pipeline Code Structure:**
```python
# backend/app/voice_pipeline.py
class VoicePipeline:
    def __init__(self):
        self.vad = SileroVAD()
        self.stt = STTHandler()  # faster-whisper
        self.tts = TTSHandler()   # Kokoro
        self.llm = LLMHandler()   # Ollama
        self.lang_detect = LanguageDetector()
    
    async def process_audio_chunk(self, audio_chunk: bytes) -> bytes:
        # 1. VAD - detect speech
        if not self.vad.is_speech(audio_chunk):
            return None
        
        # 2. Detect language
        # (use first chunk with enough audio)
        
        # 3. STT - transcribe
        text = await self.stt.transcribe(audio_chunk, language)
        
        # 4. Generate response
        response = await self.llm.generate(
            text, 
            context=self.get_course_context(),
            language=language
        )
        
        # 5. TTS - convert to audio
        audio = await self.tts.speak(response, language=language)
        
        return audio
```

#### Day 5-7: Google Sheets Integration

| Task | Implementation |
|------|----------------|
| Google Sheets API | Set up service account |
| Course sync | Sync every 1 hour via cron |
| Cache courses | Store in PostgreSQL |
| Error handling | Retry with exponential backoff |

**Google Sheets Format:**
```
| Course Name | Duration | Fee (INR) | Job Roles | Mode | Prerequisites |
|-------------|----------|-----------|-----------|------|---------------|
| Python DS   | 6 months | 35,000    | Data Analyst, ML Engineer | Online | Basic programming |
```

#### Day 7: Multi-language Setup

| Task | Implementation |
|------|----------------|
| Language detection | Use langdetect library |
| STT language mapping | Map to Whisper language codes |
| TTS voice mapping | Map to Kokoro voice IDs |
| Prompt templates | Create per-language prompts |

**Language Mapping:**
```python
LANGUAGE_CONFIG = {
    'en': {'stt': 'en', 'tts_voice': 'af_sarah', 'prompt_file': 'en.txt'},
    'hi': {'stt': 'hi', 'tts_voice': 'hf_psharma', 'prompt_file': 'hi.txt'},
    'te': {'stt': 'te', 'tts_voice': 'hf_telugu', 'prompt_file': 'te.txt'},
    'ta': {'stt': 'ta', 'tts_voice': 'hf_tamil', 'prompt_file': 'ta.txt'},
    'ur': {'stt': 'ur', 'tts_voice': 'hf_urdu', 'prompt_file': 'ur.txt'},
    'kn': {'stt': 'kn', 'tts_voice': 'hf_kannada', 'prompt_file': 'kn.txt'},
}
```

---

### Phase 2: Lead Capture (Week 2)

#### Day 8-10: Lead Collection Flow

| Step | Action | Data Captured |
|------|--------|---------------|
| 1 | Greeting | - |
| 2 | Ask intent | Inquiry type |
| 3 | Provide info | Course details |
| 4 | Capture interest | Course name |
| 5 | Capture contact | Name, Phone, Email |
| 6 | Confirm & Close | Summary |

**Conversation Flow Example:**
```
AI: Namaste! Welcome to TechVision Academy. How can I help you today?
Caller: I want to know about your data science course.
AI: We have a Python Data Science course. It's 6 months, costs ₹35,000, and prepares you for roles like Data Analyst and Machine Learning Engineer. Would you like to know more or enroll?
Caller: Yes, I'm interested. My name is Rahul.
AI: Nice to meet you, Rahul! Could you share your phone number for our counselor to contact you?
Caller: Yes, it's 9876543210.
AI: Thank you! Our team will call you shortly at 9876543210. Is there anything else you'd like to know?
Caller: No, that's all.
AI: Thank you for calling TechVision Academy. Have a great day!
```

#### Day 11-14: Admin Dashboard

| Feature | Implementation |
|---------|----------------|
| Lead list | React + TanStack Table |
| Filters | By date, course, status |
| Search | By name, phone, email |
| Export | CSV download |
| Lead details | Modal with full info |
| Call history | Linked to lead |
| Analytics | Charts (conversions, etc.) |

**Dashboard Pages:**
1. **Dashboard** - Overview, stats, recent leads
2. **Leads** - Full lead list with filters
3. **Calls** - Call log with recordings
4. **Courses** - Manage course data
5. **Settings** - Institute config, voice prompts

---

### Phase 3: Testing & Optimization (Week 3)

#### Day 15-18: Call Flow Tuning

| Test | Criteria | Target |
|------|----------|--------|
| Greeting | Plays correctly | <1 sec |
| Speech detection | Accurate | >95% |
| Transcription | Accurate | >90% |
| Response generation | Contextual | Relevant |
| TTS quality | Natural | >4/5 |
| End-to-end latency | Total time | <2 sec |
| Language detection | Accuracy | >90% |

#### Day 19-21: Load Testing

| Metric | Target |
|--------|--------|
| Concurrent calls | 10+ |
| CPU usage | <80% |
| GPU usage | <90% |
| Memory | <16GB |
| Latency | <2.5 sec |
| Error rate | <1% |

---

## 7. Code Structure

```
repcon-voice-agent/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 # FastAPI entry point
│   │   ├── config.py               # Configuration
│   │   ├── voice_pipeline.py       # Core voice processing
│   │   ├── handlers/
│   │   │   ├── __init__.py
│   │   │   ├── stt_handler.py      # Speech-to-text
│   │   │   ├── tts_handler.py       # Text-to-speech
│   │   │   ├── vad_handler.py       # Voice activity detection
│   │   │   ├── llm_handler.py       # LLM integration
│   │   │   ├── lang_detector.py    # Language detection
│   │   │   └── intent_classifier.py # Intent classification
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── google_sheets.py    # Google Sheets sync
│   │   │   ├── lead_capture.py     # Lead collection
│   │   │   ├── call_logger.py      # Call logging
│   │   │   └── notifications.py     # Alert services
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── institute.py         # Institute model
│   │   │   ├── course.py            # Course model
│   │   │   ├── student.py           # Student/Lead model
│   │   │   ├── call.py              # Call log model
│   │   │   └── voice_config.py      # Voice config model
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── lead.py              # Pydantic schemas
│   │   │   ├── call.py
│   │   │   └── course.py
│   │   ├── database/
│   │   │   ├── __init__.py
│   │   │   ├── connection.py       # DB connection
│   │   │   └── migrations/         # Alembic migrations
│   │   ├── routers/
│   │   │   ├── __init__.py
│   │   │   ├── leads.py             # Lead endpoints
│   │   │   ├── calls.py             # Call endpoints
│   │   │   ├── courses.py           # Course endpoints
│   │   │   └── webhooks.py          # Twilio webhooks
│   │   └── prompts/
│   │       ├── __init__.py
│   │       ├── en.txt               # English prompt
│   │       ├── hi.txt               # Hindi prompt
│   │       ├── te.txt               # Telugu prompt
│   │       ├── ta.txt               # Tamil prompt
│   │       ├── ur.txt               # Urdu prompt
│   │       └── kn.txt               # Kannada prompt
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_handlers.py
│   │   ├── test_pipeline.py
│   │   └── test_api.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── main.jsx
│   │   ├── App.jsx
│   │   ├── api/
│   │   │   ├── client.js            # API client
│   │   │   └── endpoints.js
│   │   ├── components/
│   │   │   ├── Layout.jsx
│   │   │   ├── Header.jsx
│   │   │   ├── Sidebar.jsx
│   │   │   ├── DataTable.jsx
│   │   │   ├── StatsCard.jsx
│   │   │   └── LoadingSpinner.jsx
│   │   ├── pages/
│   │   │   ├── Dashboard.jsx
│   │   │   ├── Leads.jsx
│   │   │   ├── LeadDetail.jsx
│   │   │   ├── Calls.jsx
│   │   │   ├── Courses.jsx
│   │   │   └── Settings.jsx
│   │   ├── hooks/
│   │   │   ├── useLeads.js
│   │   │   ├── useCalls.js
│   │   │   └── useAuth.js
│   │   ├── context/
│   │   │   └── AuthContext.jsx
│   │   └── styles/
│   │       └── index.css
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
├── infrastructure/
│   ├── docker/
│   │   ├── docker-compose.yml
│   │   ├── Dockerfile.backend
│   │   ├── Dockerfile.frontend
│   │   └── nginx.conf
│   ├── terraform/                   # Infrastructure as Code
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   └── ansible/                    # Configuration management
│       ├── playbook.yml
│       └── inventory.ini
├── database/
│   ├── schema.sql
│   ├── seed_data.sql
│   └── migrations/
│       └── (alembic migrations)
├── config/
│   ├── google-sheets-credentials.json
│   └── twilio-config.env.example
├── scripts/
│   ├── setup.sh
│   ├── deploy.sh
│   └── backup.sh
├── docs/
│   ├── PROTOTYPE_PLAN.md
│   ├── MULTI_LANGUAGE_SUPPORT.md
│   ├── API_DOCS.md
│   └── DEPLOYMENT.md
├── README.md
├── .gitignore
├── docker-compose.yml
├── Dockerfile
└── Makefile
```

---

## 8. Database Schema

### 8.1 Tables Overview

```sql
-- Complete Database Schema for RepCon Voice Agent
-- PostgreSQL 15+

-- 8.1.1 Institutes (Multi-tenant)
CREATE TABLE institutes (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    phone_number VARCHAR(20),
    whatsapp_number VARCHAR(20),
    email VARCHAR(255),
    address TEXT,
    logo_url TEXT,
    website VARCHAR(255),
    google_sheet_url TEXT,
    google_sheet_id VARCHAR(255),
    timezone VARCHAR(50) DEFAULT 'Asia/Kolkata',
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 8.1.2 Users (Admin users for each institute)
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    institute_id INTEGER REFERENCES institutes(id) ON DELETE CASCADE,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    role VARCHAR(50) DEFAULT 'admin', -- admin, manager, viewer
    is_active BOOLEAN DEFAULT true,
    last_login TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 8.1.3 Voice Configs (Institute-specific voice settings)
CREATE TABLE voice_configs (
    id SERIAL PRIMARY KEY,
    institute_id INTEGER REFERENCES institutes(id) ON DELETE CASCADE UNIQUE,
    greeting_message TEXT DEFAULT 'Hello! Welcome to our institute. How can I help you today?',
    goodbye_message TEXT DEFAULT 'Thank you for calling. Have a great day!',
    timeout_message TEXT DEFAULT 'Sorry, I didn't catch that. Could you please repeat?',
    system_prompt TEXT,
    language VARCHAR(10) DEFAULT 'en',
    voice_id VARCHAR(50),
    max_call_duration INTEGER DEFAULT 300, -- seconds
    max_silence_duration INTEGER DEFAULT 5, -- seconds
    enable_recording BOOLEAN DEFAULT false,
    enable_transcription BOOLEAN DEFAULT true,
    enable_voicemail BOOLEAN DEFAULT true,
    voicemail_action VARCHAR(20) DEFAULT 'callback', -- callback, sms, email
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 8.1.4 Courses
CREATE TABLE courses (
    id SERIAL PRIMARY KEY,
    institute_id INTEGER REFERENCES institutes(id) ON DELETE CASCADE,
    course_name VARCHAR(255) NOT NULL,
    course_code VARCHAR(50),
    description TEXT,
    duration VARCHAR(50) NOT NULL,
    duration_days INTEGER,
    fee DECIMAL(10,2) NOT NULL,
    fee_currency VARCHAR(3) DEFAULT 'INR',
    job_roles TEXT[],
    syllabus TEXT,
    prerequisites TEXT,
    eligibility TEXT,
    mode VARCHAR(20) DEFAULT 'online', -- online, offline, hybrid
    start_date DATE,
    batch_time VARCHAR(100),
    certificate TEXT,
    placement_assistance BOOLEAN DEFAULT false,
    source_updated TIMESTAMP,
    source_id VARCHAR(255), -- Google Sheets row ID
    is_active BOOLEAN DEFAULT true,
    display_order INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 8.1.5 Course FAQs
CREATE TABLE course_faqs (
    id SERIAL PRIMARY KEY,
    course_id INTEGER REFERENCES courses(id) ON DELETE CASCADE,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    display_order INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 8.1.6 Students/Leads
CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    institute_id INTEGER REFERENCES institutes(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    phone_country_code VARCHAR(5) DEFAULT '+91',
    email VARCHAR(255),
    whatsapp_opt_in BOOLEAN DEFAULT false,
    course_interest INTEGER REFERENCES courses(id),
    source VARCHAR(50) DEFAULT 'voice_agent', -- voice_agent, website, referral, walkin
    status VARCHAR(50) DEFAULT 'new', -- new, contacted, interested, enrolled, lost, not_responsive
    priority VARCHAR(20) DEFAULT 'normal', -- low, normal, high, urgent
    assigned_to INTEGER REFERENCES users(id),
    notes TEXT,
    follow_up_date DATE,
    last_contacted_at TIMESTAMP,
    converted_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 8.1.7 Student Activity Log
CREATE TABLE student_activities (
    id SERIAL PRIMARY KEY,
    student_id INTEGER REFERENCES students(id) ON DELETE CASCADE,
    activity_type VARCHAR(50) NOT NULL, -- call, email, sms, note, status_change
    description TEXT,
    metadata JSONB,
    performed_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 8.1.8 Calls
CREATE TABLE calls (
    id SERIAL PRIMARY KEY,
    student_id INTEGER REFERENCES students(id) ON DELETE SET NULL,
    institute_id INTEGER REFERENCES institutes(id) ON DELETE CASCADE,
    caller_phone VARCHAR(20) NOT NULL,
    caller_country_code VARCHAR(5) DEFAULT '+91',
    direction VARCHAR(10) DEFAULT 'inbound', -- inbound, outbound
    status VARCHAR(20) DEFAULT 'no_answer', -- completed, no_answer, busy, failed, voicemail
    duration INTEGER, -- seconds
    wait_time INTEGER, -- seconds before answered
    recording_url TEXT,
    recording_duration INTEGER,
    transcript TEXT,
    transcript_language VARCHAR(10),
    summary TEXT,
    sentiment VARCHAR(20), -- positive, neutral, negative
    outcome VARCHAR(50), -- interested, not_interested, callback_requested, enrolled, etc.
    cost DECIMAL(10,2) DEFAULT 0,
    twilio_call_sid VARCHAR(100),
    started_at TIMESTAMP,
    answered_at TIMESTAMP,
    ended_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 8.1.9 Call Transcripts (Chunked for long calls)
CREATE TABLE call_transcripts (
    id SERIAL PRIMARY KEY,
    call_id INTEGER REFERENCES calls(id) ON DELETE CASCADE,
    sequence_number INTEGER NOT NULL,
    speaker VARCHAR(20) DEFAULT 'unknown', -- ai, caller
    text TEXT NOT NULL,
    language VARCHAR(10),
    start_time INTEGER, -- milliseconds from call start
    end_time INTEGER,
    confidence DECIMAL(5,4),
    audio_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 8.1.10 Call Events (For debugging)
CREATE TABLE call_events (
    id SERIAL PRIMARY KEY,
    call_id INTEGER REFERENCES calls(id) ON DELETE CASCADE,
    event_type VARCHAR(50) NOT NULL, -- call_started, speech_detected, transcript, etc.
    event_data JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 8.1.11 IVR Flows (Future: menu-based routing)
CREATE TABLE ivr_flows (
    id SERIAL PRIMARY KEY,
    institute_id INTEGER REFERENCES institutes(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    flow_data JSONB NOT NULL, -- Tree structure of IVR
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 8.1.12 Analytics Summary (Materialized views for dashboard)
CREATE TABLE daily_stats (
    id SERIAL PRIMARY KEY,
    institute_id INTEGER REFERENCES institutes(id) ON DELETE CASCADE,
    date DATE NOT NULL,
    total_calls INTEGER DEFAULT 0,
    answered_calls INTEGER DEFAULT 0,
    missed_calls INTEGER DEFAULT 0,
    total_duration INTEGER DEFAULT 0,
    new_leads INTEGER DEFAULT 0,
    converted_leads INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(institute_id, date)
);

-- 8.1.13 Settings (Key-value store)
CREATE TABLE settings (
    id SERIAL PRIMARY KEY,
    institute_id INTEGER REFERENCES institutes(id) ON DELETE CASCADE,
    key VARCHAR(100) NOT NULL,
    value TEXT,
    description VARCHAR(255),
    is_encrypted BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(institute_id, key)
);

-- 8.1.14 Audit Log
CREATE TABLE audit_logs (
    id SERIAL PRIMARY KEY,
    institute_id INTEGER REFERENCES institutes(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id),
    action VARCHAR(100) NOT NULL,
    entity_type VARCHAR(50),
    entity_id INTEGER,
    old_value JSONB,
    new_value JSONB,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 8.2 Indexes

```sql
-- Performance indexes
CREATE INDEX idx_students_institute ON students(institute_id);
CREATE INDEX idx_students_status ON students(status);
CREATE INDEX idx_students_phone ON students(phone);
CREATE INDEX idx_students_course ON students(course_interest);
CREATE INDEX idx_students_created ON students(created_at DESC);

CREATE INDEX idx_calls_institute ON calls(institute_id);
CREATE INDEX idx_calls_student ON calls(student_id);
CREATE INDEX idx_calls_status ON calls(status);
CREATE INDEX idx_calls_created ON calls(created_at DESC);
CREATE INDEX idx_calls_direction ON calls(direction);

CREATE INDEX idx_courses_institute ON courses(institute_id);
CREATE INDEX idx_courses_active ON courses(is_active);

CREATE INDEX idx_student_activities_student ON student_activities(student_id DESC);
CREATE INDEX idx_student_activities_type ON student_activities(activity_type);

CREATE INDEX idx_call_transcripts_call ON call_transcripts(call_id);
CREATE INDEX idx_call_events_call ON call_events(call_id);

CREATE INDEX idx_audit_institute ON audit_logs(institute_id, created_at DESC);
CREATE INDEX idx_audit_user ON audit_logs(user_id, created_at DESC);

-- Full-text search indexes (PostgreSQL)
CREATE INDEX idx_students_search ON students USING gin(to_tsvector('english', name || ' ' || COALESCE(phone, '') || ' ' || COALESCE(email, '')));
CREATE INDEX idx_courses_search ON courses USING gin(to_tsvector('english', course_name || ' ' || COALESCE(description, '')));
```

### 8.3 Functions & Triggers

```sql
-- Auto-update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply to all tables with updated_at
CREATE TRIGGER update_institutes_updated_at BEFORE UPDATE ON institutes
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_students_updated_at BEFORE UPDATE ON students
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_calls_updated_at BEFORE UPDATE ON calls
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Daily stats aggregation trigger
CREATE OR REPLACE FUNCTION update_daily_stats()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO daily_stats (institute_id, date, total_calls, answered_calls, missed_calls, new_leads)
    VALUES (
        NEW.institute_id,
        CURRENT_DATE,
        1,
        CASE WHEN NEW.status = 'completed' THEN 1 ELSE 0 END,
        CASE WHEN NEW.status = 'no_answer' THEN 1 ELSE 0 END,
        CASE WHEN NEW.student_id IS NOT NULL AND NEW.source = 'voice_agent' THEN 1 ELSE 0 END
    )
    ON CONFLICT (institute_id, date) DO UPDATE SET
        total_calls = daily_stats.total_calls + 1,
        answered_calls = daily_stats.answered_calls + CASE WHEN NEW.status = 'completed' THEN 1 ELSE 0 END,
        missed_calls = daily_stats.missed_calls + CASE WHEN NEW.status = 'no_answer' THEN 1 ELSE 0 END,
        new_leads = daily_stats.new_leads + CASE WHEN NEW.student_id IS NOT NULL AND NEW.source = 'voice_agent' THEN 1 ELSE 0 END;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER trigger_update_daily_stats AFTER INSERT ON calls
    FOR EACH ROW EXECUTE FUNCTION update_daily_stats();
```

---

## 9. Voice Pipeline Flow

### 9.1 Complete Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           INBOUND CALL                                   │
│                      (Twilio → Webhook)                                 │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         CALL INITIATED                                   │
│  • Twilio sends webhook to /webhooks/twilio                             │
│  • Create call record in database                                       │
│  • Return TwiML with <Connect><Stream>                                  │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                     START MEDIA STREAM                                   │
│  • Twilio opens WebSocket connection                                    │
│  • Bidirectional audio streaming begins                                 │
│  • Initialize pipeline components                                       │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                       GREETING MESSAGE                                    │
│  • Fetch institute voice config                                        │
│  • Generate greeting in configured language                            │
│  • Convert to speech (TTS)                                             │
│  • Stream audio to caller                                               │
│  • Wait for caller response                                            │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │
                    ┌────────────┴────────────┐
                    │                         │
                    ▼                         ▼
            ┌───────────┐             ┌───────────┐
            │  SPEECH   │             │  SILENCE  │
            │ DETECTED  │             │ DETECTED  │
            └─────┬─────┘             └─────┬─────┘
                  │                         │
                  ▼                         ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    AUDIO CHUNK PROCESSING                                 │
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │ 1. Receive audio chunk (50ms)                                    │  │
│  │ 2. VAD: Check if speech (Silero)                                 │  │
│  │ 3. If speech:                                                    │  │
│  │    a. Accumulate audio buffer                                    │  │
│  │    b. Detect language (after 1st chunk with speech)            │  │
│  │    c. STT: Transcribe (Whisper)                                  │  │
│  │    d. Add to transcript buffer                                   │  │
│  │    e. If complete sentence:                                      │  │
│  │        i.   Intent classification                                │  │
│  │        ii.  Retrieve context (courses from DB)                   │  │
│  │        iii. Generate response (Ollama)                            │  │
│  │        iv.  Convert to speech (Kokoro TTS)                      │  │
│  │        v.   Stream audio to caller                               │  │
│  │ 4. If silence > max_silence:                                     │  │
│  │    a. Play timeout message                                       │  │
│  │    b. Wait for response                                          │  │
│  │    c. If no response: end call                                   │  │
│  └──────────────────────────────────────────────────────────────────┘  │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      INTENT CLASSIFICATION                               │
│                                                                          │
│  Rules-based detection:                                                  │
│  ┌────────────────────────────────────────────────────────────────────┐ │
│  | Intent          | Keywords                                        | │
│  |-----------------|------------------------------------------------| |
│  | course_info     | course, class, syllabus, learn, study          | │
│  | fee_inquiry     | fee, cost, price, charges, rupees, rupees      | |
│  | duration        | duration, long, months, weeks, time            | │
│  | job_placement   | job, placement, career, salary, package        | │
│  | admission       | admission, enroll, join, register               | |
│  | contact_capture | name, number, phone, call, contact             | |
│  | complaint       | problem, issue, complaint, refund              | |
│  | goodbye         | bye, thank, goodbye, tc, thanks               | │
│  └────────────────────────────────────────────────────────────────────┘ │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      LEAD CAPTURE FLOW                                   │
│                                                                          │
│  Step 1: Extract Name                                                   │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │ AI: "Could I know your name please?"                             │  │
│  │ Caller: "My name is Rahul"                                       │  │
│  │ Extract: name = "Rahul"                                          │  │
│  └──────────────────────────────────────────────────────────────────┘  │
│                                  │                                       │
│                                  ▼                                       │
│  Step 2: Extract Phone                                                  │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │ AI: "Thank you Rahul. Could you share your phone number?"        │  │
│  │ Caller: "It's 9876543210"                                        │  │
│  │ Extract: phone = "9876543210"                                    │  │
│  └──────────────────────────────────────────────────────────────────┘  │
│                                  │                                       │
│                                  ▼                                       │
│  Step 3: Extract Email (Optional)                                       │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │ AI: "Would you like to share your email for updates?"           │  │
│  │ Caller: "Yes, it's rahul@email.com"                              │  │
│  │ Extract: email = "rahul@email.com"                               │  │
│  └──────────────────────────────────────────────────────────────────┘  │
│                                  │                                       │
│                                  ▼                                       │
│  Step 4: Confirm & Save                                                │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │ AI: "I've noted your details. Our team will call you at        │  │
│  │     9876543210. Is there anything else you'd like to know?"    │  │
│  │ Save: student record to database                                 │  │
│  └──────────────────────────────────────────────────────────────────┘  │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         CALL END                                         │
│  • Send goodbye message                                                 │
│  • Close audio stream                                                   │
│  • Update call record (duration, status, transcript)                    │
│  • Log call events                                                      │
│  • Send notifications (if configured)                                   │
└─────────────────────────────────────────────────────────────────────────┘
```

### 9.2 State Machine

```
                    ┌──────────────┐
                    │   INITIAL    │
                    └──────┬───────┘
                           │ Call started
                           ▼
                    ┌──────────────┐
          ┌────────▶│  GREETING    │◀────────┐
          │         └──────┬───────┘        │
          │                │                 │
          │         Caller speaks           │ No response
          │                │                 │ (timeout)
          │                ▼                 │
          │         ┌──────────────┐        │
          │         │  PROCESSING   │─────────┘
          │         └──────┬───────┘
          │                │
          │         ┌──────┴───────┐
          │         │              │
          │    Intent detected   Silence
          │         │              │
          │         ▼              ▼
          │   ┌──────────┐   ┌──────────┐
          │   │ RESPOND  │   │ TIMEOUT  │
          │   └────┬─────┘   └────┬─────┘
          │        │               │
          │   More speech      Response
          │        │               │
          └────────┼───────────────┘
                   │
                   ▼
            ┌──────────────┐
            │  LEAD_CAPTURE │ (if collecting info)
            └──────┬───────┘
                   │
            Caller ends
                   │
                   ▼
            ┌──────────────┐
            │  COMPLETED   │
            └──────────────┘
```

---

## 10. Multi-Language Support

### 10.1 Supported Languages

| Language | Code | STT Model | TTS Voice | Prompt |
|----------|------|-----------|-----------|--------|
| English | en | large-v3 | af_sarah | en.txt |
| Hindi | hi | large-v3 | hf_psharma | hi.txt |
| Telugu | te | large-v3 | hf_telugu | te.txt |
| Urdu | ur | large-v3 | hf_urdu | ur.txt |
| Tamil | ta | large-v3 | hf_tamil | ta.txt |
| Kannada | kn | large-v3 | hf_kannada | kn.txt |

### 10.2 Language Detection

```python
# services/language_detector.py
from langdetect import detect, LangDetectException
import fasttext

class LanguageDetector:
    def __init__(self):
        # Use langdetect for primary detection
        # Can use fasttext for better accuracy
        self.supported = ['en', 'hi', 'te', 'ur', 'ta', 'kn']
    
    def detect(self, text: str) -> str:
        """Detect language from transcribed text"""
        try:
            lang = detect(text)
            if lang in self.supported:
                return lang
            return 'en'  # Default to English
        except LangDetectException:
            return 'en'
    
    def detect_from_audio(self, audio_chunk: bytes) -> str:
        """Detect language from audio (future: use whisper language detection)"""
        # For now, detect from first transcribed text
        # Whisper can also detect language automatically
        return None  # Let Whisper handle it
```

### 10.3 Language-Specific Prompts

**English (en.txt):**
```
You are a helpful voice assistant for an educational institute.
Your role is to:
1. Greet callers warmly
2. Provide accurate information about courses, fees, duration, and job opportunities
3. Capture caller details (name, phone, email) for follow-up
4. Be polite, concise, and professional

Guidelines:
- Keep responses under 30 seconds of speech
- Speak clearly and at moderate pace
- Confirm information before ending call
- Always offer to help with anything else
```

**Hindi (hi.txt):**
```
आप एक शैक्षणिक संस्थान के लिए एक सहायक वॉइस सहायक हैं।
आपकी भूमिका:
1. कॉलर का स्वागत करें
2. पाठ्यक्रम, शुल्क, अवधि और नौकरी के अवसरों के बारे में सटीक जानकारी दें
3. फॉलो-अप के लिए कॉलर का विवरण (नाम, फोन, ईमेल) लें
4. विनम्र, संक्षिप्त और पेशेवर रहें
```

### 10.4 TTS Voice Configuration

```python
TTS_VOICES = {
    'en': {
        'voice_id': 'af_sarah',
        'name': 'Sarah',
        'gender': 'female',
        'description': 'American English, neutral'
    },
    'hi': {
        'voice_id': 'hf_psharma',
        'name': 'Pooja Sharma',
        'gender': 'female',
        'description': 'Hindi, Indian accent'
    },
    'ta': {
        'voice_id': 'hf_tamil',
        'name': 'Tamil Speaker',
        'gender': 'female',
        'description': 'Tamil, Indian accent'
    },
    'te': {
        'voice_id': 'hf_telugu',
        'name': 'Telugu Speaker',
        'gender': 'female',
        'description': 'Telugu, Indian accent'
    },
    'ur': {
        'voice_id': 'hf_urdu',
        'name': 'Urdu Speaker',
        'gender': 'female',
        'description': 'Urdu, South Asian'
    },
    'kn': {
        'voice_id': 'hf_kannada',
        'name': 'Kannada Speaker',
        'gender': 'female',
        'description': 'Kannada, Indian accent'
    }
}
```

---

## 11. Phone Number & Telephony

### 11.1 Provider Comparison

| Provider | Setup Cost | Monthly Cost | Per Min Cost | Features | Pros |
|----------|------------|--------------|--------------|----------|------|
| **Twilio** | $1 | $1/mo | $0.008/min | Webhooks, Recording, IVR | Reliable, good docs |
| **VoIP.ms** | $0 | $0.50/mo | $0.01/min | DID, Forwarding | Cheap, flexible |
| **Plivo** | $0 | $1/mo | $0.007/min | APIs, SMS | Good alternative |
| **Exotel** | ₹500 | ₹200/mo | ₹1.50/min | India-specific | Local support |
| **Knowlarity** | ₹0 | ₹300/mo | ₹2/min | Cloud telephony | Popular in India |

### 11.2 Recommended: Twilio

**Setup:**
1. Create Twilio account
2. Buy Indian DID number (~$1/mo)
3. Configure webhook URLs
4. Set up TwiML for media stream

**Webhook Configuration:**

| Event | URL | Method |
|-------|-----|--------|
| Voice incoming | `https://your-domain.com/webhooks/twilio/voice` | POST |
| Status callback | `https://your-domain.com/webhooks/twilio/status` | POST |

**TwiML for Media Stream:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Connect>
        <Stream url="wss://your-domain.com/media-stream" />
    </Connect>
</Response>
```

### 11.3 Call Flow with Twilio

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Caller    │────▶│   Twilio    │────▶│  Webhook    │
│   (Phone)   │     │   (Cloud)   │     │  (Backend)  │
└─────────────┘     └─────────────┘     └─────────────┘
       │                                       │
       │ Audio                                 │ WebSocket
       │ Stream                                │ Stream
       │                                       │
       ▼                                       ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Caller    │◀────│   Twilio    │◀────│  WebSocket  │
│   (Phone)   │     │   (Cloud)   │     │   Server    │
└─────────────┘     └─────────────┘     └─────────────┘
```

---

## 12. Google Sheets Integration

### 12.1 Sheet Structure

**Sheet 1: Courses**
```
| Course Name | Course Code | Duration | Fee | Job Roles | Mode | Prerequisites | Syllabus |
|-------------|-------------|----------|-----|-----------|------|---------------|----------|
| Python DS   | PDS-001     | 6 months | 35000 | Data Analyst, ML Engineer | Online | Basic programming | Python, Pandas, ML |
```

**Sheet 2: FAQs**
```
| Question | Answer | Course |
|----------|--------|--------|
| What is the fee? | Fee is ₹35,000 | Python DS |
| Duration? | 6 months | Python DS |
```

### 12.2 Sync Implementation

```python
# services/google_sheets.py
import gspread
from google.oauth2 import service_account
from datetime import datetime

class GoogleSheetsSync:
    def __init__(self, credentials_path: str):
        self.scope = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive'
        ]
        self.credentials = service_account.Credentials.from_service_account_file(
            credentials_path, 
            scopes=self.scope
        )
        self.client = gspread.Client(auth=self.credentials)
    
    def sync_courses(self, spreadsheet_url: str, institute_id: int):
        """Sync courses from Google Sheets to database"""
        spreadsheet = self.client.open_by_url(spreadsheet_url)
        sheet = spreadsheet.sheet1
        records = sheet.get_all_records()
        
        courses = []
        for record in records:
            course = {
                'institute_id': institute_id,
                'course_name': record.get('Course Name'),
                'course_code': record.get('Course Code'),
                'duration': record.get('Duration'),
                'fee': float(record.get('Fee', 0)),
                'job_roles': record.get('Job Roles', '').split(', '),
                'mode': record.get('Mode', 'online'),
                'prerequisites': record.get('Prerequisites', ''),
                'syllabus': record.get('Syllabus', ''),
                'source_updated': datetime.utcnow()
            }
            courses.append(course)
        
        return courses
```

### 12.3 Cron Schedule

| Task | Frequency | Command |
|------|-----------|---------|
| Course sync | Every 1 hour | `0 * * * * curl -X POST /sync/courses` |
| FAQ sync | Every 1 hour | `0 * * * * curl -X POST /sync/faqs` |
| Stats cleanup | Daily | `0 0 * * * DELETE FROM call_events WHERE created_at < NOW() - 30 days` |

---

## 13. Admin Dashboard

### 13.1 Pages & Features

#### Dashboard (Home)
- **Stats Cards:** Total calls, Leads today, Conversion rate, Revenue
- **Charts:** Calls per day (line), Leads by course (bar), Status distribution (pie)
- **Recent Activity:** Latest leads, recent calls

#### Leads
- **Data Table:** Name, Phone, Email, Course, Status, Date, Actions
- **Filters:** Status, Course, Date range, Source
- **Search:** By name, phone, email
- **Actions:** View details, Edit, Delete, Export CSV
- **Bulk:** Export selected, Change status

#### Calls
- **Data Table:** Caller, Duration, Status, Recording, Transcript
- **Filters:** Date, Status, Duration
- **Playback:** Listen to recording
- **Transcript:** View full conversation

#### Courses
- **List:** All courses with details
- **Sync:** Manual sync from Google Sheets
- **Edit:** Update course details
- **Toggle:** Active/Inactive

#### Settings
- **Institute:** Name, phone, address
- **Voice:** Greeting, prompts, language
- **Integrations:** Google Sheets URL, Twilio config
- **Users:** Manage admin users
- **Billing:** (Future) Payment history

### 13.2 Tech Stack

| Component | Technology |
|-----------|------------|
| Framework | React 18 + Vite |
| UI Library | Material UI (MUI) or Tailwind CSS |
| State | React Query + Context |
| Tables | TanStack Table |
| Charts | Recharts |
| Forms | React Hook Form |
| HTTP | Axios |
| Auth | JWT (stored in httpOnly cookie) |

---

## 14. Security & Compliance

### 14.1 Data Security

| Aspect | Implementation |
|--------|----------------|
| **Encryption at rest** | PostgreSQL with pgcrypto |
| **Encryption in transit** | TLS 1.3 (Let's Encrypt) |
| **API authentication** | JWT with short expiry |
| **Password hashing** | bcrypt (cost factor 12) |
| **Input validation** | Pydantic schemas |
| **SQL injection** | ORM (SQLAlchemy) + parameterized queries |
| **Rate limiting** | Redis-based rate limiter |
| **CORS** | Strict origin allowlist |

### 14.2 India Data Compliance (Draft)

| Requirement | Implementation |
|-------------|----------------|
| **Data localization** | Host in India (AWS Mumbai / GCP India) |
| **Consent** | Opt-in for recording, SMS, WhatsApp |
| **Right to delete** | Admin can delete user data |
| **Data retention** | Configurable retention policy |
| **TRAI compliance** | DND compliance, opt-out options |

### 14.3 Recording Consent Flow

```
Caller connects
       │
       ▼
Play: "This call may be recorded for quality..."
       │
       ├── Continue ──▶ Process call, log consent
       │
       └── Disconnect (if DND)
```

### 14.4 API Security

```python
# Rate limiting configuration
RATE_LIMITS = {
    'webhooks': '100/minute',
    'api_calls': '1000/hour',
    'auth': '10/minute'
}

# JWT Configuration
JWT_CONFIG = {
    'algorithm': 'HS256',
    'access_token_expire_minutes': 30,
    'refresh_token_expire_days': 7
}
```

---

## 15. Monitoring & Logging

### 15.1 Logging Strategy

| Log Level | Use Case |
|-----------|----------|
| **DEBUG** | Detailed execution flow |
| **INFO** | Normal operations |
| **WARNING** | Recoverable issues |
| **ERROR** | Failures requiring attention |
| **CRITICAL** | System-wide failures |

### 15.2 What to Log

```python
# Log structure
{
    "timestamp": "2026-03-02T10:30:00Z",
    "level": "INFO",
    "event": "call_started",
    "call_id": 12345,
    "institute_id": 1,
    "caller_phone": "+919876543210",
    "metadata": {
        "twilio_call_sid": "CAxxx",
        "duration": 0
    }
}

# Events to log
CALL_EVENTS = [
    'call_started',
    'call_answered',
    'speech_detected',
    'transcript_received',
    'llm_response',
    'tts_generated',
    'lead_captured',
    'call_ended',
    'call_failed',
    'error'
]
```

### 15.3 Monitoring Metrics

| Metric | Target | Alert Threshold |
|--------|--------|----------------|
| **Uptime** | 99.9% | < 99.5% |
| **Latency (STT)** | < 500ms | > 1000ms |
| **Latency (TTS)** | < 200ms | > 500ms |
| **Latency (E2E)** | < 2s | > 3s |
| **Error rate** | < 1% | > 5% |
| **CPU usage** | < 70% | > 85% |
| **GPU usage** | < 80% | > 95% |
| **Memory** | < 12GB | > 14GB |

### 15.4 Tools

| Purpose | Tool |
|---------|------|
| **Logging** | Python logging → JSON → File/CloudWatch |
| **Metrics** | Prometheus + Grafana |
| **Alerting** | PagerDuty / Opsgenie |
| **APM** | Sentry (error tracking) |
| **Health checks** | /health endpoint |

---

## 16. Testing Checklist

### 16.1 Functional Tests

| # | Test Case | Expected Result |
|---|-----------|-----------------|
| 1 | Inbound call connects | Voice agent answers |
| 2 | Greeting plays | Caller hears greeting |
| 3 | Course query | Correct info provided |
| 4 | Lead capture - Name | Name extracted correctly |
| 5 | Lead capture - Phone | Phone validated & saved |
| 6 | Lead capture - Email | Email validated & saved |
| 7 | Call ends | Lead saved to database |
| 8 | Admin dashboard loads | Leads visible |
| 9 | CSV export | File downloads |
| 10 | Google Sheets sync | Courses updated |

### 16.2 Non-Functional Tests

| # | Test Case | Target |
|---|-----------|--------|
| 1 | Concurrent calls | 10+ simultaneous |
| 2 | Latency (E2E) | < 2 seconds |
| 3 | Stress test | 100 calls/hour |
| 4 | Recovery | Auto-recover on failure |
| 5 | Recording | Audio saved correctly |
| 6 | Long call | Works for 10+ minutes |

### 16.3 Language Tests

| Language | Test Phrase | Response |
|----------|-------------|----------|
| English | "What courses?" | English response |
| Hindi | "Courses batayein" | Hindi response |
| Telugu | "Courses ela undi?" | Telugu response |
| Urdu | "Kya courses hain?" | Urdu response |
| Tamil | "Enna courses iru?" | Tamil response |
| Kannada | "Yaaru courses?" | Kannada response |

---

## 17. CI/CD Pipeline

### 17.1 GitHub Actions Workflow

```yaml
# .github/workflows/ci.yml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -r backend/requirements.txt
          pip install -r backend/requirements-dev.txt
      
      - name: Run tests
        run: pytest --cov=backend
      
      - name: Lint
        run: |
          black --check backend/
          flake8 backend/
          mypy backend/

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Build Docker images
        run: |
          docker build -t repcon-backend:${{ github.sha }} ./backend
          docker build -t repcon-frontend:${{ github.sha }} ./frontend
      
      - name: Push to registry
        run: |
          echo ${{ secrets.DOCKER_TOKEN }} | docker login -u ${{ secrets.DOCKER_USER }} --password-stdin
          docker push registry/repcon-backend:${{ github.sha }}

  deploy:
    needs: build
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to production
        run: |
          # SSH to server and pull latest
          ssh ${{ secrets.PROD_HOST }} "
            cd /opt/repcon
            docker-compose pull
            docker-compose up -d
          "
```

### 17.2 Deployment Stages

| Stage | Trigger | Action |
|-------|---------|--------|
| **Dev** | Push to `develop` | Deploy to dev server |
| **Staging** | Push to `main` | Deploy to staging |
| **Production** | Release tag | Deploy to production |

---

## 18. Cost Analysis

### 18.1 Single Institute (Prototype) - With 150 Calls/Day

| Item | Monthly Cost (INR) | Notes |
|------|-------------------|-------|
| **VoIP Number (Twilio)** | 100 | $1.20/mo |
| **GPU VPS (1x T4 - upgraded)** | 3,500 | ~$42/mo (higher for 150 calls) |
| **PostgreSQL** | 500 | Managed DB with better specs |
| **Redis** | 0 | Included in VPS |
| **Domain & SSL** | 200 | .in domain |
| **Twilio Usage (22,500 min)** | 1,800 | $0.008/min × 22,500 = $180 |
| **Misc** | 400 | Backup, monitoring |
| **Total** | **₹6,500/mo** | |

> Note: Original ₹3,000 estimate was for ~30 calls/day. With 150 calls/day (5x load), cost increases but still highly profitable!

### 18.2 Scale: 100 Institutes (150 calls/day each = 15,000 calls/day total)

| Item | Monthly Cost (INR) | Notes |
|------|-------------------|-------|
| **VoIP Numbers (100)** | 10,000 | $1 × 100 |
| **Twilio Usage (2.25M min/mo)** | 180,000 | $0.008 × 2,250,000 min |
| **GPU Servers (3x A100)** | 60,000 | $720/mo - upgraded for load |
| **PostgreSQL (Managed)** | 8,000 | $96/mo - higher specs |
| **Redis** | 2,000 | $24/mo |
| **Load Balancer** | 5,000 | $60/mo |
| **Storage (S3)** | 3,000 | $36/mo |
| **Domain & SSL** | 500 | $6/mo |
| **Monitoring** | 2,000 | $24/mo |
| **Misc** | 4,500 | $54/mo |
| **Total Cost** | **₹275,000/mo** | |
| **Per Institute** | **₹2,750/mo** | |

### 18.3 Profit Calculation (With 150 Calls/Day Load)

| Institutes | Revenue (₹) | Cost (₹) | Profit (₹) | Per Institute |
|------------|-------------|----------|------------|---------------|
| 1 | 30,000 | 6,500 | **23,500** | 23,500 |
| 10 | 300,000 | 40,000 | **260,000** | 26,000 |
| 50 | 1,500,000 | 150,000 | **1,350,000** | 27,000 |
| 100 | 3,000,000 | 275,000 | **2,725,000** | 27,250 |

---

## 19. Risk Analysis

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| GPU shortage | Medium | High | Use cloud GPU (Lambda, Paperspace) |
| LLM latency | Medium | Medium | Optimize prompts, use smaller model |
| Twilio pricing changes | Low | Medium | Build abstraction layer, support VoIP.ms |
| Language detection fails | Medium | Low | Fallback to English |
| Data breach | Low | Critical | Encryption, access controls, audit logs |
| Legal compliance | Medium | High | Consult legal, build compliant |
| Competitor | Low | Medium | First-mover advantage in India |

---

## 20. Success Metrics

### 20.1 KPIs

| Metric | Definition | Target |
|--------|------------|--------|
| **Call Answer Rate** | Answered / Total calls | > 80% |
| **Lead Capture Rate** | Leads captured / Total calls | > 60% |
| **Conversion Rate** | Enrolled / Total leads | > 10% |
| **Average Call Duration** | Total duration / Calls | 2-5 min |
| **Latency (E2E)** | Time from speech to response | < 2 sec |
| **Uptime** | Available / Total time | > 99.9% |
| **Cost per Lead** | Monthly cost / New leads | < ₹50 |
| **Customer Satisfaction** | Post-call survey | > 4/5 |

### 20.2 Dashboard Metrics

- Today's calls
- This week's leads
- Conversion funnel
- Popular courses
- Peak call hours
- Geographic distribution

---

## 21. Next Steps

### Phase 1: Prototype (Week 1-3)
- [ ] Setup GPU server
- [ ] Install Docker & dependencies
- [ ] Deploy voice pipeline
- [ ] Connect Twilio
- [ ] Integrate Google Sheets
- [ ] Build admin dashboard
- [ ] Test with sample calls
- [ ] Deploy for single institute pilot

### Phase 2: Polish (Month 2)
- [ ] Optimize latency
- [ ] Add more languages
- [ ] Improve lead capture rate
- [ ] Add analytics dashboard
- [ ] Implement caching

### Phase 3: Scale (Month 3-6)
- [ ] Multi-tenant architecture
- [ ] Add 10 more institutes
- [ ] Implement IVR menu
- [ ] Add outbound calling
- [ ] SMS/WhatsApp integration

### Phase 4: Growth (Month 6-12)
- [ ] Scale to 100 institutes
- [ ] Add CRM integrations
- [ ] Build partner network
- [ ] Expand to other verticals

---

## Document Information

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-03-01 | AI | Initial draft |
| 2.0 | 2026-03-01 | AI | Added research |
| 3.0 | 2026-03-02 | AI | Comprehensive review, all details added |

---

*This document serves as the comprehensive requirements for RepCon Voice Agent prototyping.*
