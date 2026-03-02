# RepCon Voice Agent

AI-Powered Voice Receptionist for Small-Scale Educational Institutes in India

## Overview

RepCon Voice Agent is an AI-powered telephone receptionist that handles inbound inquiries for educational institutes 24/7/365. It uses open-source AI models (Whisper, Kokoro TTS, Ollama) to understand caller intent, provide course information, and capture leads automatically.

## Features

- **24/7 Call Answering** - Never miss an inquiry
- **Multi-Language Support** - English, Hindi, Telugu, Tamil, Urdu, Kannada
- **Course Information** - Provides accurate details from Google Sheets
- **Lead Capture** - Automatically captures name, phone, email, interest
- **Admin Dashboard** - View leads, calls, and analytics
- **Open Source** - Self-hosted, no per-minute costs

## Quick Start

### Prerequisites

- Docker & Docker Compose
- NVIDIA GPU (T4 or better) for AI inference
- Twilio Account (for phone number)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/itsaslamopenclawdata/VoiceAgent_Prototype.git
cd VoiceAgent_Prototype
```

2. Copy environment template:
```bash
cp backend/.env.example backend/.env
```

3. Edit `.env` with your configuration:
- Twilio credentials
- Google Sheets API (optional)
- Database credentials

4. Start services:
```bash
docker-compose up -d
```

5. Access:
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Frontend: http://localhost:3000

## Architecture

```
┌─────────────┐     PSTN      ┌─────────────┐
│   Caller    │──────────────▶│   Twilio    │
└─────────────┘               └──────┬──────┘
                                     │
                                     │ Webhook
                                     ▼
                              ┌─────────────┐
                              │   Backend   │
                              │  (FastAPI)  │
                              └──────┬──────┘
                                     │
           ┌─────────────────────────┼─────────────────────────┐
           │                         │                         │
           ▼                         ▼                         ▼
    ┌─────────────┐          ┌─────────────┐          ┌─────────────┐
    │     STT     │          │     LLM     │          │     TTS     │
    │  (Whisper)  │          │   (Ollama)  │          │   (Kokoro)  │
    └─────────────┘          └─────────────┘          └─────────────┘
```

## Tech Stack

| Component | Technology |
|-----------|------------|
| Backend | FastAPI (Python) |
| Database | PostgreSQL 15 |
| Cache | Redis 7 |
| STT | faster-whisper |
| TTS | Kokoro |
| LLM | Ollama (Llama 3.2) |
| VAD | Silero |
| Telephony | Twilio |
| Container | Docker |

## Documentation

- [PRD](docs/VoiceAgentPrototype_PRD.md)
- [Implementation Plan](docs/Prototype_Implementation.md)
- [Multi-Language Support](docs/MULTI_LANGUAGE_SUPPORT.md)

## License

MIT License

## Support

For issues and questions, please open a GitHub issue.
