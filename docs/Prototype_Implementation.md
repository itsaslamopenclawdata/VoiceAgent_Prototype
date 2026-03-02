# RepCon Voice Agent - Prototype Implementation Plan

## Version: 1.0
## Date: 2026-03-02
## Project: RepCon Voice Agent Prototype

---

# TABLE OF CONTENTS

1. [Document Purpose](#1-document-purpose)
2. [Implementation Structure Overview](#2-implementation-structure-overview)
3. [Wave 1: Foundation & Infrastructure](#3-wave-1-foundation--infrastructure)
4. [Wave 2: Core Voice Pipeline](#4-wave-2-core-voice-pipeline)
5. [Wave 3: Integrations & Dashboard](#5-wave-3-integrations--dashboard)
6. [Wave 4: Testing & Launch](#6-wave-4-testing--launch)
7. [Sequential vs Parallel Activities](#7-sequential-vs-parallel-activities)
8. [Subagent Assignment Matrix](#8-subagent-assignment-matrix)

---

# 1. DOCUMENT PURPOSE

This document provides a **detailed implementation plan** for the RepCon Voice Agent Prototype based on the PRD (VoiceAgentPrototype_PRD.md). The implementation is structured into:

- **Waves**: Major release phases
- **Phases**: Logical groupings of related work
- **Tracks**: Specific workstreams within phases
- **Tasks**: Single units of work (atomic)

Each task is a **single unit of work** that can be assigned to a subagent for execution.

---

# 2. IMPLEMENTATION STRUCTURE OVERVIEW

```
IMPLEMENTATION STRUCTURE
├── WAVE 1: Foundation & Infrastructure (Week 1)
│   ├── Phase 1.1: Infrastructure Setup
│   ├── Phase 1.2: Database & Models
│   └── Phase 1.3: Backend Scaffolding
│
├── WAVE 2: Core Voice Pipeline (Week 2)
│   ├── Phase 2.1: AI Service Integration
│   ├── Phase 2.2: Voice Pipeline Orchestration
│   └── Phase 2.3: Twilio Integration
│
├── WAVE 3: Integrations & Dashboard (Week 3)
│   ├── Phase 3.1: Google Sheets Integration
│   ├── Phase 3.2: Multi-Language Support
│   └── Phase 3.3: Admin Dashboard
│
├── WAVE 4: Testing & Launch (Week 4)
│   ├── Phase 4.1: Testing & QA
│   ├── Phase 4.2: Deployment
│   └── Phase 4.3: Launch & Documentation
│
└── CONCURRENCY MATRIX
    ├── Sequential Activities
    └── Parallel Activities
```

---

# 3. WAVE 1: FOUNDATION & INFRASTRUCTURE

**Duration**: Week 1 (Days 1-7)
**Objective**: Set up infrastructure, database, and backend foundation

## Phase 1.1: Infrastructure Setup

### Track 1.1.1: Cloud & Development Environment

| Task ID | Task Name | Description | Dependencies |
|---------|-----------|-------------|--------------|
| T-101 | Provision GPU Cloud Server | Create VM with NVIDIA T4, 16GB VRAM, 8 vCPU, 32GB RAM | None |
| T-102 | Install Docker & Docker Compose | Install Docker engine, Docker Compose plugin | T-101 |
| T-103 | Configure Nginx Reverse Proxy | Set up Nginx with SSL termination | T-102 |
| T-104 | Set Up Development Environment | Configure VSCode, Python 3.11+, Git | T-102 |
| T-105 | Create Project Directory Structure | Create backend/, frontend/, tests/ directories | T-102 |
| T-106 | Set Up Environment Variables Template | Create .env.example with all required variables | None |

### Track 1.1.2: Container Services

| Task ID | Task Name | Description | Dependencies |
|---------|-----------|-------------|--------------|
| T-107 | Create PostgreSQL Container | Docker container with PostgreSQL 15, persistent volume | T-102 |
| T-108 | Create Redis Container | Docker container with Redis 7 for caching | T-102 |
| T-109 | Create Ollama Container | Docker container for LLM inference | T-102 |
| T-110 | Configure Docker Networking | Set up internal network for services | T-107, T-108, T-109 |
| T-111 | Set Up Health Check Scripts | Create health check endpoints for all services | T-107, T-108, T-109 |

## Phase 1.2: Database & Models

### Track 1.2.1: Database Schema

| Task ID | Task Name | Description | Dependencies |
|---------|-----------|-------------|--------------|
| T-112 | Create institutes Table | SQL schema with all fields (name, slug, phone, etc.) | T-107 |
| T-113 | Create users Table | SQL schema with auth fields, roles | T-112 |
| T-114 | Create voice_configs Table | SQL schema for voice settings per institute | T-112 |
| T-115 | Create courses Table | SQL schema with JSON array for job_roles | T-112 |
| T-116 | Create students Table | SQL schema for leads with status enum | T-112 |
| T-117 | Create calls Table | SQL schema for call records with transcript | T-112 |
| T-118 | Create student_activities Table | SQL schema for activity logging | T-116 |
| T-119 | Create call_transcripts Table | SQL schema for conversation storage | T-117 |
| T-120 | Create daily_stats Table | SQL schema for aggregated statistics | T-112 |
| T-121 | Create settings Table | SQL schema for key-value config | T-112 |
| T-122 | Create audit_logs Table | SQL schema for tracking changes | T-112 |
| T-123 | Create Indexes | Add indexes for frequently queried columns | T-112 to T-122 |
| T-124 | Create Triggers | Add triggers for updated_at, audit logging | T-112 to T-122 |

### Track 1.2.2: Database Models (Python)

| Task ID | Task Name | Description | Dependencies |
|---------|-----------|-------------|--------------|
| T-125 | Install SQLAlchemy & Pydantic | Add dependencies to requirements.txt | T-104 |
| T-126 | Create Base Model | Create base.py with declarative base | T-125 |
| T-127 | Create Institute Model | SQLAlchemy model + Pydantic schema | T-126 |
| T-128 | Create User Model | SQLAlchemy model + Pydantic schema | T-127 |
| T-129 | Create VoiceConfig Model | SQLAlchemy model + Pydantic schema | T-127 |
| T-130 | Create Course Model | SQLAlchemy model + Pydantic schema | T-127 |
| T-131 | Create Student (Lead) Model | SQLAlchemy model + Pydantic schema | T-127 |
| T-132 | Create Call Model | SQLAlchemy model + Pydantic schema | T-127 |
| T-133 | Create Transcript Model | SQLAlchemy model + Pydantic schema | T-127 |
| T-134 | Create Activity Model | SQLAlchemy model + Pydantic schema | T-127 |
| T-135 | Create DailyStats Model | SQLAlchemy model + Pydantic schema | T-127 |
| T-136 | Set Up Alembic Migrations | Configure migration tool for schema changes | T-125 |
| T-137 | Create Initial Migration | Generate and run first migration | T-136 |

### Track 1.2.3: Database Seeding

| Task ID | Task Name | Description | Dependencies |
|---------|-----------|-------------|--------------|
| T-138 | Create Seed Script Structure | Create seeds/ directory with __init__.py | T-137 |
| T-139 | Seed Institute Data | Insert sample institute (TechVision Academy) | T-138 |
| T-140 | Seed User Data | Insert admin user with bcrypt password | T-139 |
| T-141 | Seed Voice Config Data | Insert default voice settings | T-139 |
| T-142 | Seed Course Data | Insert 8 sample courses from PRD | T-139 |
| T-143 | Seed Student Data | Insert 10 sample leads | T-139 |
| T-144 | Seed Call Data | Insert sample call records | T-139 |
| T-145 | Verify All Data | Run SELECT queries to verify seeding | T-140, T-141, T-142, T-143, T-144 |

## Phase 1.3: Backend Scaffolding

### Track 1.3.1: FastAPI Application Setup

| Task ID | Task Name | Description | Dependencies |
|---------|-----------|-------------|--------------|
| T-146 | Install FastAPI Dependencies | Add fastapi, uvicorn, python-multipart | T-104 |
| T-147 | Create main.py | Initialize FastAPI app with CORS, docs | T-146 |
| T-148 | Configure Application Settings | Create config.py with settings class | T-147 |
| T-149 | Set Up Logging | Configure structured logging | T-147 |
| T-150 | Create Database Dependency | Implement get_db() for SQLAlchemy | T-125, T-147 |
| T-151 | Create Error Handlers | Custom exceptions and handlers | T-147 |

### Track 1.3.2: API Routes Structure

| Task ID | Task Name | Description | Dependencies |
|---------|-----------|-------------|--------------|
| T-152 | Create API Router Structure | Set up routers/ directory with __init__.py | T-147 |
| T-153 | Create Auth Routes | POST /login, /logout, /refresh | T-152 |
| T-154 | Create Leads CRUD Routes | GET/POST/PUT/DELETE /leads | T-152 |
| T-155 | Create Calls Routes | GET /calls, GET /calls/{id} | T-152 |
| T-156 | Create Courses Routes | GET /courses, POST /courses/sync | T-152 |
| T-157 | Create Stats Routes | GET /stats/dashboard, /stats/analytics | T-152 |
| T-158 | Create Settings Routes | GET/PUT /settings | T-152 |
| T-159 | Create Health Check Routes | GET /health, GET /ready | T-147 |
| T-160 | Create Webhook Routes | POST /webhooks/twilio/* | T-152 |

### Track 1.3.3: Service Layer

| Task ID | Task Name | Description | Dependencies |
|---------|-----------|-------------|--------------|
| T-161 | Create LeadService | Business logic for lead operations | T-128, T-131 |
| T-162 | Create CallService | Business logic for call operations | T-129, T-132 |
| T-163 | Create CourseService | Business logic for course operations | T-130 |
| T-164 | Create AuthService | JWT token generation, verification | T-128 |
| T-165 | Create StatsService | Dashboard metrics calculation | T-135 |
| T-166 | Implement Dependency Injection | Wire services to routes | T-161, T-162, T-163, T-164, T-165 |

---

# 4. WAVE 2: CORE VOICE PIPELINE

**Duration**: Week 2 (Days 8-14)
**Objective**: Build the core voice processing pipeline (STT → LLM → TTS)

## Phase 2.1: AI Service Integration

### Track 2.1.1: Speech-to-Text (STT) Service

| Task ID | Task Name | Description | Dependencies |
|---------|-----------|-------------|--------------|
| T-167 | Install faster-whisper | Add to requirements.txt | T-104 |
| T-168 | Create STT Service Class | stt_service.py with Whisper integration | T-167 |
| T-169 | Download Whisper Model | large-v3 model, ~3GB | T-168 |
| T-170 | Implement Transcription Method | transcribe(audio_bytes) → text | T-168 |
| T-171 | Implement Language Detection | detect_language(text) → lang_code | T-168 |
| T-172 | Add Audio Preprocessing | Noise reduction, volume normalization | T-168 |
| T-173 | Create STT API Endpoint | POST /api/v1/stt/transcribe | T-169 |
| T-174 | Add STT Caching | Cache transcriptions for repeated queries | T-173 |
| T-175 | Test STT Accuracy | Run benchmark tests | T-170 |

### Track 2.1.2: Text-to-Speech (TTS) Service

| Task ID | Task Name | Description | Dependencies |
|---------|-----------|-------------|--------------|
| T-176 | Install Kokoro TTS | Add to requirements.txt | T-104 |
| T-177 | Create TTS Service Class | tts_service.py with Kokoro integration | T-176 |
| T-178 | Download TTS Models | All 6 language voice models | T-177 |
| T-179 | Implement Text-to-Audio | synthesize(text, voice_id) → audio | T-177 |
| T-180 | Implement Voice Selection | get_voice(language) → voice_id | T-179 |
| T-181 | Configure Audio Settings | Speed 0.9x, volume normalization | T-179 |
| T-182 | Implement Chunking | Split audio into 100ms chunks for streaming | T-181 |
| T-183 | Create TTS API Endpoint | POST /api/v1/tts/synthesize | T-182 |
| T-184 | Test All 6 Languages | Verify TTS output quality | T-183 |

### Track 2.1.3: Language Model (LLM) Service

| Task ID | Task Name | Description | Dependencies |
|---------|-----------|-------------|--------------|
| T-185 | Pull Llama 3.2 Model | ollama pull llama3.2 | T-109 |
| T-186 | Create LLM Service Class | llm_service.py with Ollama integration | T-185 |
| T-187 | Implement Prompt Templates | System prompts for each language | T-186 |
| T-188 | Implement Response Generation | generate(prompt, context) → response | T-186 |
| T-189 | Add Context Injection | Inject course data into prompts | T-188 |
| T-190 | Implement Response Caching | Cache LLM responses | T-188 |
| T-191 | Optimize Response Length | Limit responses for voice | T-188 |
| T-192 | Create LLM API Endpoint | POST /api/v1/llm/generate | T-191 |
| T-193 | Test LLM Responses | Verify context-aware answers | T-192 |

### Track 2.1.4: Voice Activity Detection (VAD)

| Task ID | Task Name | Description | Dependencies |
|---------|-----------|-------------|--------------|
| T-194 | Install Silero VAD | Add to requirements.txt | T-104 |
| T-195 | Create VAD Service Class | vad_service.py with Silero | T-194 |
| T-196 | Implement Voice Detection | detect(audio_chunk) → bool | T-195 |
| T-197 | Configure Silence Threshold | Set sensitivity levels | T-196 |
| T-198 | Implement Speech Segmentation | Detect start/end of speech | T-196 |
| T-199 | Test VAD Performance | Verify accuracy on sample audio | T-198 |

## Phase 2.2: Voice Pipeline Orchestration

### Track 2.2.1: Pipeline Core

| Task ID | Task Name | Description | Dependencies |
|---------|-----------|-------------|--------------|
| T-200 | Create VoicePipeline Class | Main orchestration class | T-174, T-183, T-192, T-198 |
| T-201 | Implement Audio Flow | Process incoming audio chunks | T-200 |
| T-202 | Implement Response Flow | Generate and stream audio response | T-200 |
| T-203 | Create Conversation Manager | Track conversation state, history | T-201 |
| T-204 | Implement Intent Classification | Classify user intent from text | T-203 |
| T-205 | Create Intent Patterns | Define patterns for course, fee, lead, goodbye | T-204 |
| T-206 | Implement Lead Capture Logic | Extract name, phone from conversation | T-204 |
| T-207 | Implement Error Handling | Graceful degradation on failures | T-200 |
| T-208 | Add Retry Logic | Exponential backoff for AI services | T-207 |

### Track 2.2.2: Multi-Turn Conversation

| Task ID | Task Name | Description | Dependencies |
|---------|-----------|-------------|--------------|
| T-209 | Design Conversation Flowchart | Visual flow for call handling | T-203 |
| T-210 | Implement Greeting Handler | Play welcome message | T-209 |
| T-211 | Implement Query Handler | Route to appropriate response | T-209 |
| T-212 | Implement Lead Capture Flow | Name → Phone → Confirm | T-209 |
| T-213 | Implement Goodbye Handler | End call gracefully | T-209 |
| T-214 | Implement Timeout Handler | Handle silence/no response | T-209 |
| T-215 | Add Conversation Logging | Log all interactions | T-212 |
| T-216 | Test Full Conversation | E2E test of call flow | T-215 |

### Track 2.2.3: Real-Time Streaming

| Task ID | Task Name | Description | Dependencies |
|---------|-----------|-------------|--------------|
| T-217 | Set Up WebSocket Server | FastAPI WebSocket endpoint | T-147 |
| T-218 | Implement Audio Streaming | Stream TTS audio to client | T-217 |
| T-219 | Implement Bi-directional Stream | Twilio ↔ Backend ↔ Twilio | T-217 |
| T-220 | Buffer Audio Chunks | Implement buffer for smooth playback | T-218 |
| T-221 | Handle Reconnection | Graceful WebSocket reconnection | T-218 |
| T-222 | Test Latency | Measure end-to-end delay | T-221 |

## Phase 2.3: Twilio Integration

### Track 2.3.1: Webhook Setup

| Task ID | Task Name | Description | Dependencies |
|---------|-----------|-------------|--------------|
| T-223 | Create Twilio Webhook Handler | Handle incoming call webhooks | T-160 |
| T-224 | Implement Voice Response | Generate TwiML for greeting | T-223 |
| T-225 | Configure Media Stream | Set up WebSocket for audio | T-224 |
| T-226 | Handle Call Status Callbacks | Track call status changes | T-223 |
| T-227 | Implement Call Recording | Optional call recording | T-223 |
| T-228 | Configure TwiML Bin | For static responses | T-224 |

### Track 2.3.2: Phone Number Configuration

| Task ID | Task Name | Description | Dependencies |
|---------|-----------|-------------|--------------|
| T-229 | Purchase Twilio India DID | Get +91 phone number | None |
| T-230 | Configure Voice URL | Point to webhook endpoint | T-229 |
| T-231 | Enable Media Streaming | Activate stream capability | T-230 |
| T-232 | Set Up Status Callback | Configure callback URL | T-230 |
| T-233 | Configure Recording Settings | Set recording preferences | T-232 |
| T-234 | Test Inbound Call | Verify call flow end-to-end | T-233 |

### Track 2.3.3: Call Lifecycle Management

| Task ID | Task Name | Description | Dependencies |
|---------|-----------|-------------|--------------|
| T-235 | Create Call Record | On call initiation | T-162 |
| T-236 | Update Call on Answer | Mark answered timestamp | T-235 |
| T-237 | Update Call on End | Save duration, transcript | T-235 |
| T-238 | Handle Missed Calls | Log unanswered calls | T-235 |
| T-239 | Handle Failed Calls | Log error conditions | T-235 |
| T-240 | Calculate Call Cost | Track Twilio charges | T-237 |
| T-241 | Test Call Flow | Full E2E call test | T-240 |

---

# 5. WAVE 3: INTEGRATIONS & DASHBOARD

**Duration**: Week 3 (Days 15-21)
**Objective**: Add external integrations and build admin dashboard

## Phase 3.1: Google Sheets Integration

### Track 3.1 API Setup

| Task ID.1: Sheets | Task Name | Description | Dependencies |
|---------|-----------|-------------|--------------|
| T-242 | Create Google Cloud Project | Set up GCP for Sheets API | None |
| T-243 | Enable Sheets API | Enable in GCP console | T-242 |
| T-244 | Create Service Account | For authentication | T-243 |
| T-245 | Generate Service Account Key | Download JSON credentials | T-244 |
| T-246 | Share Sample Spreadsheet | Share with service account | T-244 |
| T-247 | Install Google Client Library | Add to requirements.txt | T-104 |
| T-248 | Create Sheets Service | sheets_service.py | T-247 |

### Track 3.1.2: Data Synchronization

| Task ID | Task Name | Description | Dependencies |
|---------|-----------|-------------|--------------|
| T-249 | Implement Course Fetch | Read from Google Sheets | T-248 |
| T-250 | Map Sheet Columns to DB | Column mapping logic | T-249 |
| T-251 | Implement Incremental Sync | Detect changes only | T-250 |
| T-252 | Handle New Courses | Add to database | T-251 |
| T-253 | Handle Updated Courses | Update existing records | T-251 |
| T-254 | Handle Deleted Courses | Mark inactive or remove | T-251 |
| T-255 | Add Error Handling | Retry logic, logging | T-252 |
| T-256 | Create Manual Sync Endpoint | POST /api/v1/courses/sync | T-255 |

### Track 3.1.3: Automated Sync

| Task ID | Task Name | Description | Dependencies |
|---------|-----------|-------------|--------------|
| T-257 | Set Up Cron Job | Schedule hourly sync | T-256 |
| T-258 | Implement Sync Lock | Prevent concurrent syncs | T-257 |
| T-259 | Add Sync Notifications | Alert on failure | T-257 |
| T-260 | Create Sync Status Endpoint | Check last sync time | T-259 |
| T-261 | Test Full Sync | Verify data accuracy | T-260 |

## Phase 3.2: Multi-Language Support

### Track 3.2.1: Language Detection

| Task ID | Task Name | Description | Dependencies |
|---------|-----------|-------------|--------------|
| T-262 | Implement Fast Detection | Quick language check on first audio | T-171 |
| T-263 | Handle Language Switching | Mid-call language change | T-262 |
| T-264 | Add Language Preference | Per-institute language setting | T-262 |
| T-265 | Test Language Detection | 90%+ accuracy target | T-264 |

### Track 3.2.2: Language-Specific Prompts

| Task ID | Task Name | Description | Dependencies |
|---------|-----------|-------------|--------------|
| T-266 | Create English Prompt | System prompt template | T-187 |
| T-267 | Create Hindi Prompt | Hindi system prompt | T-187 |
| T-268 | Create Telugu Prompt | Telugu system prompt | T-187 |
| T-269 | Create Tamil Prompt | Tamil system prompt | T-187 |
| T-270 | Create Urdu Prompt | Urdu system prompt | T-187 |
| T-271 | Create Kannada Prompt | Kannada system prompt | T-187 |
| T-272 | Test All Language Prompts | Verify responses | T-271 |

### Track 3.2.3: Voice Selection

| Task ID | Task Name | Description | Dependencies |
|---------|-----------|-------------|--------------|
| T-273 | Configure English Voices | af_sarah voice settings | T-180 |
| T-274 | Configure Hindi Voices | hf_psharma voice settings | T-180 |
| T-275 | Configure Telugu Voices | hf_telugu voice settings | T-180 |
| T-276 | Configure Tamil Voices | hf_tamil voice settings | T-180 |
| T-277 | Configure Urdu Voices | hf_urdu voice settings | T-180 |
| T-278 | Configure Kannada Voices | hf_kannada voice settings | T-180 |
| T-279 | Test All Voices | Quality check | T-278 |

## Phase 3.3: Admin Dashboard

### Track 3.3.1: Frontend Setup

| Task ID | Task Name | Description | Dependencies |
|---------|-----------|-------------|--------------|
| T-280 | Initialize React Project | Vite + React + TypeScript | T-104 |
| T-281 | Install Dependencies | React Router, Axios, Tailwind | T-280 |
| T-282 | Set Up Tailwind CSS | Configure design system | T-281 |
| T-283 | Create Project Structure | components/, pages/, hooks/ | T-280 |
| T-284 | Set Up API Client | Axios instance with interceptors | T-283 |
| T-285 | Create Authentication Context | Manage auth state | T-283 |

### Track 3.3.2: Dashboard Pages

| Task ID | Task Name | Description | Dependencies |
|---------|-----------|-------------|--------------|
| T-286 | Create Login Page | Login form with validation | T-285 |
| T-287 | Create Dashboard Home | Stats cards, charts | T-285 |
| T-288 | Create Leads List Page | Table with filters, search | T-285 |
| T-289 | Create Lead Detail Page | Full lead info, history | T-288 |
| T-290 | Create Calls List Page | Call history table | T-285 |
| T-291 | Create Call Detail Page | Transcript, recording | T-290 |
| T-292 | Create Courses Page | Course list, sync button | T-285 |
| T-293 | Create Settings Page | Institute config, voice settings | T-285 |

### Track 3.3.3: Dashboard Components

| Task ID | Task Name | Description | Dependencies |
|---------|-----------|-------------|--------------|
| T-294 | Create Layout Component | Sidebar, header, main | T-283 |
| T-295 | Create Sidebar Navigation | Menu items | T-294 |
| T-296 | Create Stats Card Component | Reusable metric card | T-294 |
| T-297 | Create Data Table Component | Sortable, filterable table | T-294 |
| T-298 | Create Modal Component | For forms, details | T-294 |
| T-299 | Create Chart Components | Line, bar, pie charts | T-294 |
| T-300 | Create Form Components | Input, select, date picker | T-294 |
| T-301 | Create Toast Notifications | Success/error messages | T-294 |

### Track 3.3.4: Dashboard Integration

| Task ID | Task Name | Description | Dependencies |
|---------|-----------|-------------|--------------|
| T-302 | Connect Dashboard to API | Wire up all endpoints | T-286 to T-293 |
| T-303 | Implement Lead CRUD | Create, update, delete leads | T-302 |
| T-304 | Implement CSV Export | Export leads to CSV | T-302 |
| T-305 | Implement Course Sync | Trigger from dashboard | T-302 |
| T-306 | Implement Settings Save | Save voice config | T-302 |
| T-307 | Add Loading States | Skeleton loaders | T-303 |
| T-308 | Add Error Handling | Error boundaries, toasts | T-307 |
| T-309 | Test All Pages | Functional testing | T-308 |

---

# 6. WAVE 4: TESTING & LAUNCH

**Duration**: Week 4 (Days 22-28)
**Objective**: Comprehensive testing and production deployment

## Phase 4.1: Testing & QA

### Track 4.1.1: Unit Tests

| Task ID | Task Name | Description | Dependencies |
|---------|-----------|-------------|--------------|
| T-310 | Set Up Test Framework | Configure pytest, fixtures | T-104 |
| T-311 | Write Model Tests | Test all SQLAlchemy models | T-125 |
| T-312 | Write Service Tests | Test business logic | T-161 to T-165 |
| T-313 | Write API Tests | Test all endpoints | T-152 to T-160 |
| T-314 | Write STT Tests | Test speech-to-text | T-167 |
| T-315 | Write TTS Tests | Test text-to-speech | T-176 |
| T-316 | Write LLM Tests | Test language model | T-185 |
| T-317 | Write Voice Pipeline Tests | Test orchestration | T-200 |
| T-318 | Run All Unit Tests | Verify 80%+ coverage | T-317 |

### Track 4.1.2: Integration Tests

| Task ID | Task Name | Description | Dependencies |
|---------|-----------|-------------|--------------|
| T-319 | Set Up Test Database | Docker container for tests | T-310 |
| T-320 | Write Auth Integration Tests | Login, JWT, RBAC | T-319 |
| T-321 | Write Leads Integration Tests | Full CRUD flow | T-319 |
| T-322 | Write Calls Integration Tests | Call lifecycle | T-319 |
| T-323 | Write Sheets Integration Tests | Sync functionality | T-319 |
| T-324 | Write Twilio Integration Tests | Webhook handling | T-319 |
| T-325 | Run Integration Tests | Verify component interaction | T-324 |

### Track 4.1.3: End-to-End Tests

| Task ID | Task Name | Description | Dependencies |
|---------|-----------|-------------|--------------|
| T-326 | Write Call Flow E2E Tests | Full voice call test | T-241 |
| T-327 | Write Lead Capture E2E Tests | Complete lead flow | T-326 |
| T-328 | Write Dashboard E2E Tests | UI interaction tests | T-309 |
| T-329 | Write Multi-Language E2E Tests | All 6 languages | T-272 |
| T-330 | Run All E2E Tests | Verify full system | T-329 |

### Track 4.1.4: Load Testing

| Task ID | Task Name | Description | Dependencies |
|---------|-----------|-------------|--------------|
| T-331 | Set Up Locust | Load testing tool | T-104 |
| T-332 | Write API Load Tests | Test /leads, /calls endpoints | T-331 |
| T-333 | Write Concurrent Call Simulation | 10, 20 concurrent calls | T-332 |
| T-334 | Run Load Tests | Measure performance | T-333 |
| T-335 | Analyze Results | Identify bottlenecks | T-334 |
| T-336 | Optimize Performance | Fix identified issues | T-335 |

## Phase 4.2: Deployment

### Track 4.2.1: Staging Deployment

| Task ID | Task Name | Description | Dependencies |
|---------|-----------|-------------|--------------|
| T-337 | Set Up Staging Server | Cloud VM for staging | T-101 |
| T-338 | Configure Environment | Staging .env file | T-337 |
| T-339 | Build Docker Images | Backend, frontend images | T-338 |
| T-340 | Set Up Docker Compose | Staging compose file | T-339 |
| T-341 | Configure Nginx | SSL, reverse proxy | T-340 |
| T-342 | Deploy to Staging | Run containers | T-341 |
| T-343 | Run Smoke Tests | Verify basic functionality | T-342 |

### Track 4.2.2: Production Deployment

| Task ID | Task Name | Description | Dependencies |
|---------|-----------|-------------|--------------|
| T-344 | Set Up Production Server | GPU-enabled production VM | T-101 |
| T-345 | Configure Production Env | Secure .env file | T-344 |
| T-346 | Set Up Monitoring | Prometheus + Grafana | T-345 |
| T-347 | Configure Backups | Automated database backups | T-345 |
| T-348 | Set Up Alerting | PagerDuty or similar | T-346 |
| T-349 | Build Production Images | Optimized Docker builds | T-347 |
| T-350 | Deploy to Production | Run containers | T-349 |
| T-351 | Verify Production Health | Check all services | T-350 |

### Track 4.2.3: DNS & SSL

| Task ID | Task Name | Description | Dependencies |
|---------|-----------|-------------|--------------|
| T-352 | Purchase Domain | repcon.in or similar | None |
| T-353 | Configure DNS | A record, CNAME | T-352 |
| T-354 | Set Up SSL Certificate | Let's Encrypt | T-353 |
| T-355 | Update Twilio Webhook | Point to production URL | T-354 |
| T-356 | Verify HTTPS | Test secure access | T-355 |

## Phase 4.3: Launch & Documentation

### Track 4.3.1: Launch Preparation

| Task ID | Task Name | Description | Dependencies |
|---------|-----------|-------------|--------------|
| T-357 | Create Runbook | Operational procedures | T-351 |
| T-358 | Create On-Call Schedule | Support rotation | T-357 |
| T-359 | Prepare Communication | Launch announcement | T-358 |
| T-360 | Set Up Support Channel | Slack/Discord for issues | T-359 |
| T-361 | Final UAT | Test with real institute | T-360 |

### Track 4.3.2: Documentation

| Task ID | Task Name | Description | Dependencies |
|---------|-----------|-------------|--------------|
| T-362 | Write API Documentation | OpenAPI/Swagger | T-152 to T-160 |
| T-363 | Write User Guide | Admin dashboard manual | T-309 |
| T-364 | Write Deployment Guide | Infrastructure setup | T-344 |
| T-365 | Write Troubleshooting Guide | Common issues | T-364 |
| T-366 | Update README | Project overview | T-365 |

### Track 4.3.3: Post-Launch

| Task ID | Task Name | Description | Dependencies |
|---------|-----------|-------------|--------------|
| T-367 | Monitor System Health | 24/7 monitoring | T-346 |
| T-368 | Collect User Feedback | Gather initial feedback | T-361 |
| T-369 | Fix Critical Issues | Address reported bugs | T-368 |
| T-370 | Plan Next Sprint | Prioritize improvements | T-369 |

---

# 7. SEQUENTIAL VS PARALLEL ACTIVITIES

## 7.1 Sequential Activities (Must Be Done in Order)

These activities have dependencies and **MUST** be executed in order:

### Infrastructure & Setup (Sequential Chain)
```
T-101 → T-102 → T-103 → T-104 → T-105 → T-106 → T-107 → T-108 → T-109
```

### Database Setup (Sequential Chain)
```
T-112 → T-113 → T-114 → T-115 → T-116 → T-117 → T-118 → T-119 → T-120 → T-121 → T-122
T-123 → T-124 → T-125 → T-126 → T-127 → T-128 → T-129 → T-130 → T-131 → T-132 → T-133 → T-134 → T-135 → T-136 → T-137
```

### Backend Foundation (Sequential Chain)
```
T-146 → T-147 → T-148 → T-149 → T-150 → T-151 → T-152 → T-153 → T-154 → T-155 → T-156 → T-157 → T-158 → T-159 → T-160
```

### AI Services (Sequential Chain)
```
T-167 → T-168 → T-169 → T-170 → T-171 → T-172 → T-173 → T-174 → T-175
T-176 → T-177 → T-178 → T-179 → T-180 → T-181 → T-182 → T-183 → T-184
T-185 → T-186 → T-187 → T-188 → T-189 → T-190 → T-191 → T-192 → T-193
```

### Voice Pipeline (Sequential Chain)
```
T-200 → T-201 → T-202 → T-203 → T-204 → T-205 → T-206 → T-207 → T-208
T-209 → T-210 → T-211 → T-212 → T-213 → T-214 → T-215 → T-216
T-217 → T-218 → T-219 → T-220 → T-221 → T-222
```

### Twilio Integration (Sequential Chain)
```
T-223 → T-224 → T-225 → T-226 → T-227 → T-228
T-229 → T-230 → T-231 → T-232 → T-233 → T-234
T-235 → T-236 → T-237 → T-238 → T-239 → T-240 → T-241
```

### Google Sheets (Sequential Chain)
```
T-242 → T-243 → T-244 → T-245 → T-246 → T-247 → T-248
T-249 → T-250 → T-251 → T-252 → T-253 → T-254 → T-255 → T-256
T-257 → T-258 → T-259 → T-260 → T-261
```

### Multi-Language (Sequential Chain)
```
T-262 → T-263 → T-264 → T-265
T-266 → T-267 → T-268 → T-269 → T-270 → T-271 → T-272
T-273 → T-274 → T-275 → T-276 → T-277 → T-278 → T-279
```

### Frontend (Sequential Chain)
```
T-280 → T-281 → T-282 → T-283 → T-284 → T-285
T-286 → T-287 → T-288 → T-289 → T-290 → T-291 → T-292 → T-293
T-294 → T-295 → T-296 → T-297 → T-298 → T-299 → T-300 → T-301
T-302 → T-303 → T-304 → T-305 → T-306 → T-307 → T-308 → T-309
```

### Testing (Sequential Chain)
```
T-310 → T-311 → T-312 → T-313 → T-314 → T-315 → T-316 → T-317 → T-318
T-319 → T-320 → T-321 → T-322 → T-323 → T-324 → T-325
T-326 → T-327 → T-328 → T-329 → T-330
T-331 → T-332 → T-333 → T-334 → T-335 → T-336
```

### Deployment (Sequential Chain)
```
T-337 → T-338 → T-339 → T-340 → T-341 → T-342 → T-343
T-344 → T-345 → T-346 → T-347 → T-348 → T-349 → T-350 → T-351
T-352 → T-353 → T-354 → T-355 → T-356
```

### Documentation (Sequential Chain)
```
T-357 → T-358 → T-359 → T-360 → T-361
T-362 → T-363 → T-364 → T-365 → T-366
T-367 → T-368 → T-369 → T-370
```

## 7.2 Parallel Activities (Can Be Done Concurrently)

These activities have **NO dependencies** on each other and can be executed in parallel by different subagents:

### Track-Level Parallelization

| Parallel Group | Tasks | Description |
|----------------|-------|-------------|
| **Infrastructure Containers** | T-107, T-108, T-109 | PostgreSQL, Redis, Ollama containers can be created in parallel |
| **Database Tables** | T-112 to T-122 | All tables can be created in parallel |
| **Python Models** | T-127 to T-135 | All models can be created in parallel |
| **Seed Data** | T-139 to T-144 | All seed data can be inserted in parallel |
| **API Routes** | T-153 to T-160 | All route files can be created in parallel |
| **Service Layer** | T-161 to T-165 | All services can be created in parallel |
| **AI Services** | T-167, T-176, T-185, T-194 | STT, TTS, LLM, VAD can be set up in parallel |
| **Language Prompts** | T-266 to T-271 | All 6 language prompts can be created in parallel |
| **Voice Configuration** | T-273 to T-278 | All 6 language voices can be configured in parallel |
| **Frontend Pages** | T-286 to T-293 | All pages can be created in parallel |
| **Dashboard Components** | T-294 to T-301 | All components can be created in parallel |
| **Unit Tests** | T-311 to T-317 | All unit tests can be written in parallel |
| **Integration Tests** | T-320 to T-324 | All integration tests can be written in parallel |
| **E2E Tests** | T-326 to T-329 | All E2E tests can be written in parallel |

### Phase-Level Parallelization

| Phase | Parallel Tracks |
|-------|-----------------|
| **Phase 1.1** | Track 1.1.1 can run in parallel with Track 1.1.2 |
| **Phase 1.2** | Track 1.2.1, 1.2.2, 1.2.3 can run in parallel |
| **Phase 1.3** | Track 1.3.1, 1.3.2, 1.3.3 can run in parallel |
| **Phase 2.1** | Track 2.1.1, 2.1.2, 2.1.3, 2.1.4 can run in parallel |
| **Phase 2.2** | Track 2.2.1, 2.2.2, 2.2.3 can run in parallel |
| **Phase 3.1** | Track 3.1.1, 3.1.2, 3.1.3 can run in parallel |
| **Phase 3.2** | Track 3.2.1, 3.2.2, 3.2.3 can run in parallel |
| **Phase 3.3** | Track 3.3.1, 3.3.2, 3.3.3, 3.3.4 can run in parallel |
| **Phase 4.1** | Track 4.1.1, 4.1.2, 4.1.3, 4.1.4 can run in parallel |

---

# 8. SUBAGENT ASSIGNMENT MATRIX

## 8.1 Recommended Subagent Distribution

| Wave | Phase | Track | Tasks | Recommended Subagents |
|------|-------|-------|-------|----------------------|
| 1 | 1.1 | 1.1.1 | T-101 to T-106 | **DevOps Agent** |
| 1 | 1.1 | 1.1.2 | T-107 to T-111 | **DevOps Agent** |
| 1 | 1.2 | 1.2.1 | T-112 to T-124 | **Database Agent** |
| 1 | 1.2 | 1.2.2 | T-125 to T-137 | **Backend Agent** |
| 1 | 1.2 | 1.2.3 | T-138 to T-145 | **Database Agent** |
| 1 | 1.3 | 1.3.1 | T-146 to T-151 | **Backend Agent** |
| 1 | 1.3 | 1.3.2 | T-152 to T-160 | **Backend Agent** |
| 1 | 1.3 | 1.3.3 | T-161 to T-166 | **Backend Agent** |
| 2 | 2.1 | 2.1.1 | T-167 to T-175 | **ML Engineer Agent** |
| 2 | 2.1 | 2.1.2 | T-176 to T-184 | **ML Engineer Agent** |
| 2 | 2.1 | 2.1.3 | T-185 to T-193 | **ML Engineer Agent** |
| 2 | 2.1 | 2.1.4 | T-194 to T-199 | **ML Engineer Agent** |
| 2 | 2.2 | 2.2.1 | T-200 to T-208 | **Voice Engineer Agent** |
| 2 | 2.2 | 2.2.2 | T-209 to T-216 | **Voice Engineer Agent** |
| 2 | 2.2 | 2.2.3 | T-217 to T-222 | **Voice Engineer Agent** |
| 2 | 2.3 | 2.3.1 | T-223 to T-228 | **Backend Agent** |
| 2 | 2.3 | 2.3.2 | T-229 to T-234 | **DevOps Agent** |
| 2 | 2.3 | 2.3.3 | T-235 to T-241 | **Backend Agent** |
| 3 | 3.1 | 3.1.1 | T-242 to T-248 | **Integration Agent** |
| 3 | 3.1 | 3.1.2 | T-249 to T-256 | **Integration Agent** |
| 3 | 3.1 | 3.1.3 | T-257 to T-261 | **Integration Agent** |
| 3 | 3.2 | 3.2.1 | T-262 to T-265 | **ML Engineer Agent** |
| 3 | 3.2 | 3.2.2 | T-266 to T-272 | **ML Engineer Agent** |
| 3 | 3.2 | 3.2.3 | T-273 to T-279 | **ML Engineer Agent** |
| 3 | 3.3 | 3.3.1 | T-280 to T-285 | **Frontend Agent** |
| 3 | 3.3 | 3.3.2 | T-286 to T-293 | **Frontend Agent** |
| 3 | 3.3 | 3.3.3 | T-294 to T-301 | **Frontend Agent** |
| 3 | 3.3 | 3.3.4 | T-302 to T-309 | **Frontend Agent** |
| 4 | 4.1 | 4.1.1 | T-310 to T-318 | **QA Engineer Agent** |
| 4 | 4.1 | 4.1.2 | T-319 to T-325 | **QA Engineer Agent** |
| 4 | 4.1 | 4.1.3 | T-326 to T-330 | **QA Engineer Agent** |
| 4 | 4.1 | 4.1.4 | T-331 to T-336 | **QA Engineer Agent** |
| 4 | 4.2 | 4.2.1 | T-337 to T-343 | **DevOps Agent** |
| 4 | 4.2 | 4.2.2 | T-344 to T-351 | **DevOps Agent** |
| 4 | 4.2 | 4.2.3 | T-352 to T-356 | **DevOps Agent** |
| 4 | 4.3 | 4.3.1 | T-357 to T-361 | **Product Manager Agent** |
| 4 | 4.3 | 4.3.2 | T-362 to T-366 | **Technical Writer Agent** |
| 4 | 4.3 | 4.3.3 | T-367 to T-370 | **DevOps Agent** |

## 8.2 Concurrency Strategy

### Maximum Parallelization Example

During Week 1 (Wave 1), the following can run in parallel:

```
Subagent 1 (DevOps):     T-101 → T-102 → T-103 → T-104 → T-105 → T-106 → T-107
Subagent 2 (Database):   T-112 → T-113 → T-114 → T-115 → T-116 → T-117 → T-118
Subagent 3 (Backend):    T-125 → T-126 → T-127 → T-128 → T-129 → T-130 → T-131
```

This reduces total time from sum of all tasks to approximately max(task_duration) per wave.

---

# APPENDIX A: TASK SUMMARY

| Wave | Phase | Tracks | Total Tasks |
|------|-------|--------|-------------|
| 1 | 3 | 9 | 66 |
| 2 | 3 | 9 | 75 |
| 3 | 3 | 9 | 64 |
| 4 | 3 | 9 | 61 |
| **Total** | **12** | **36** | **266** |

---

# APPENDIX B: DEPENDENCY GRAPH (KEY MILESTONES)

```
Wave 1 Complete (All Phase 1.x)
    ↓
Wave 2 Complete (All Phase 2.x)
    ↓
Wave 3 Complete (All Phase 3.x)
    ↓
Wave 4 Complete (All Phase 4.x)
    ↓
PRODUCTION LAUNCH
```

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-03-02 | AI | Initial Implementation Plan |

---

*This implementation plan provides the roadmap for building the RepCon Voice Agent Prototype. Each task is a single unit of work that can be assigned to a subagent for execution.*
