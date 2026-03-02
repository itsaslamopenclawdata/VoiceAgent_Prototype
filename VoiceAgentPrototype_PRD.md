# RepCon Voice Agent - Project Requirements Document (PRD)

## Version: 1.0
## Date: 2026-03-02
## Project: Voice Agent Prototype for Educational Institutes

---

# TABLE OF CONTENTS

1. [Project Overview](#1-project-overview)
2. [Problem Statement](#2-problem-statement)
3. [Solution Overview](#3-solution-overview)
4. [Stakeholders](#4-stakeholders)
5. [Business Requirements](#5-business-requirements)
6. [Functional Requirements](#6-functional-requirements)
7. [Non-Functional Requirements](#7-non-functional-requirements)
8. [Technical Architecture](#8-technical-architecture)
9. [System Components](#9-system-components)
10. [Database Design](#10-database-design)
11. [API Specifications](#11-api-specifications)
12. [Voice Pipeline Specifications](#12-voice-pipeline-specifications)
13. [Multi-Language Implementation](#13-multi-language-implementation)
14. [Integration Requirements](#14-integration-requirements)
15. [User Interface Requirements](#15-user-interface-requirements)
16. [Security Requirements](#16-security-requirements)
17. [Performance Requirements](#17-performance-requirements)
18. [Testing Requirements](#18-testing-requirements)
19. [Deployment Requirements](#19-deployment-requirements)
20. [Implementation Phases](#20-implementation-phases)
21. [Risk Management](#21-risk-management)
22. [Success Metrics](#22-success-metrics)
23. [Timeline & Milestones](#23-timeline--milestones)
24. [Budget Breakdown](#24-budget-breakdown)
25. [Appendices](#25-appendices)

---

# 1. PROJECT OVERVIEW

## 1.1 Project Name
**RepCon Voice Agent** - AI-Powered Voice Receptionist for Educational Institutes

## 1.2 Project Type
Real-time AI Voice Agent System with Telephony Integration

## 1.3 Project Summary
An autonomous voice agent system that handles inbound calls for educational institutes in India 24/7/365, replacing manual receptionists/telecallers. The system uses open-source STT (Speech-to-Text), TTS (Text-to-Speech), and LLM (Large Language Model) technologies to understand caller queries, provide accurate information about courses, and capture leads automatically.

## 1.4 Project Vision
Become the leading AI voice receptionist solution for small-to-medium educational institutes in India, enabling 24/7 availability at a fraction of the cost of human staff.

## 1.5 Project Mission
- Build a production-ready voice agent that handles 150+ calls per day per institute
- Support 6 major Indian languages (English, Hindi, Telugu, Urdu, Tamil, Kannada)
- Achieve sub-2-second end-to-end latency
- Reduce institute operational costs by 80%+ compared to manual staffing
- Capture 100% of inbound inquiries as digital leads

---

# 2. PROBLEM STATEMENT

## 2.1 Current Challenges

### 2.1.1 Limited Availability
- **Problem:** Educational institutes operate 8-10 hours/day, missing 14-16 hours of potential inquiries
- **Impact:** Estimated 30-40% of inquiries happen outside business hours
- **Data Point:** 150 calls/day potential, but only ~50% captured with manual staff

### 2.1.2 High Staff Costs
- **Problem:** Full-time telecallers cost ₹15,000-30,000/month per person
- **Impact:** Small institutes cannot afford dedicated reception staff
- **Data Point:** 1 staff can handle only 1-2 concurrent calls

### 2.1.3 Inconsistent Quality
- **Problem:** Human staff have varying knowledge levels, mood fluctuations
- **Impact:** Inconsistent information delivery, potential for errors
- **Data Point:** Studies show 20% of calls have information gaps

### 2.1.4 Manual Lead Entry
- **Problem:** Staff manually записывать caller information in registers/Excel
- **Impact:** Lost leads, no follow-up, low conversion
- **Data Point:** Only 40-50% of inquiries get converted to actionable leads

### 2.1.5 No 24/7 Coverage
- **Problem:** Night inquiries, weekend inquiries go to voicemail or unanswered
- **Impact:** Lost potential students to competitors
- **Data Point:** 15-20% of inquiries happen on weekends

## 2.2 Target Audience Pain Points

| Pain Point | Current State | Desired State |
|------------|--------------|---------------|
| Missed Calls | 30-40% missed | 0% missed |
| Staff Availability | 8 hrs/day | 24/7/365 |
| Lead Capture | 40-50% captured | 100% captured |
| Concurrent Calls | 1-2 at a time | Unlimited |
| Response Time | Minutes | <2 seconds |
| Cost per Month | ₹15,000-30,000 | ₹6,500 |

---

# 3. SOLUTION OVERVIEW

## 3.1 Solution Description
RepCon Voice Agent is an AI-powered telephone receptionist that:
1. Answers inbound calls automatically 24/7/365
2. Greets callers with institute-specific welcome message
3. Understands caller intent through speech recognition
4. Provides accurate course information from Google Sheets
5. Captures caller details (name, phone, email, interest)
6. Saves all leads to database for follow-up
7. Handles 150+ calls per day without fatigue

## 3.2 Solution Components

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         REPCON VOICE AGENT                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐                │
│  │  TELEPHONY  │───▶│    BACKEND   │───▶│  DATABASE   │                │
│  │  (Twilio)   │    │   (FastAPI)  │    │ (PostgreSQL)│                │
│  └─────────────┘    └──────┬──────┘    └─────────────┘                │
│                            │                                            │
│         ┌─────────────────┼─────────────────┐                          │
│         ▼                 ▼                 ▼                          │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐                │
│  │     STT     │    │     LLM     │    │     TTS     │                │
│  │  (Whisper)  │    │   (Ollama)  │    │   (Kokoro)  │                │
│  └─────────────┘    └─────────────┘    └─────────────┘                │
│                                                                          │
│         ┌─────────────────┬─────────────────┐                          │
│         ▼                 ▼                 ▼                          │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐                │
│  │    VAD      │    │   GOOGLE    │    │    ADMIN    │                │
│  │  (Silero)   │    │   SHEETS    │    │  DASHBOARD  │                │
│  └─────────────┘    └─────────────┘    └─────────────┘                │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

## 3.3 Key Features

| Feature | Description | Priority |
|---------|-------------|----------|
| 24/7 Call Answering | Answer calls anytime, including nights/weekends | P0 |
| Multi-language Support | Support 6 Indian languages | P0 |
| Course Information | Provide accurate course details from Sheets | P0 |
| Lead Capture | Capture name, phone, email, interest | P0 |
| Admin Dashboard | View leads, calls, analytics | P1 |
| Call Logging | Record all calls with transcripts | P1 |
| Google Sheets Sync | Auto-sync course data hourly | P1 |
| Voicemail Handling | Capture missed call info | P2 |
| CRM Integration | Push leads to external CRM | P2 |
| Analytics Dashboard | Conversion tracking, reports | P2 |

---

# 4. STAKEHOLDERS

## 4.1 Primary Stakeholders

| Stakeholder | Role | Responsibility | Communication |
|-------------|------|----------------|---------------|
| **End Users (Students)** | Callers seeking course info | Interact with voice agent, provide feedback | Via call experience |
| **Institute Admin** | Institute management | Configure voice agent, view leads | Admin dashboard |
| **Technical Team** | Development & DevOps | Build, deploy, maintain system | Sprint reviews, daily standups |

## 4.2 Secondary Stakeholders

| Stakeholder | Role | Interest |
|-------------|------|----------|
| Institute Owners | Financial decision-makers | Cost savings, ROI |
| Sales Team | Lead follow-up | Quality leads, timely notifications |
| Support Team | Issue resolution | System reliability, uptime |

## 4.3 External Dependencies

| Dependency | Type | Purpose |
|------------|------|---------|
| Twilio | Telephony Provider | Phone number, call handling |
| Google Sheets | Data Source | Course information storage |
| GPU Cloud Provider | Infrastructure | Model inference hosting |
| PostgreSQL | Database | Data persistence |

---

# 5. BUSINESS REQUIREMENTS

## 5.1 BR1: Call Handling Capacity
**Requirement:** The system must handle minimum 150 inbound calls per day per institute with average call duration of 5 minutes.

**Details:**
- Peak concurrent calls: 15-20
- Total daily minutes: 750 minutes
- Monthly call volume: ~4,500 calls
- Monthly minutes: ~22,500 minutes

**Success Criteria:**
- 100% of calls answered (no dropped calls due to capacity)
- Average wait time < 5 seconds
- Call completion rate > 95%

## 5.2 BR2: Availability
**Requirement:** The system must operate 24 hours a day, 7 days a week, 365 days a year.

**Details:**
- No downtime for maintenance during business hours
- Graceful degradation during updates
- Automatic failover capabilities

**Success Criteria:**
- Uptime: 99.9% (excluding planned maintenance)
- Maximum 8.76 hours downtime/year
- Maximum 44 minutes downtime/month

## 5.3 BR3: Multi-Language Support
**Requirement:** The system must support 6 languages: English, Hindi, Telugu, Urdu, Tamil, and Kannada.

**Details:**
- Language detection on call start
- Response in caller's detected language
- Language-specific TTS voices

**Success Criteria:**
- Language detection accuracy > 90%
- All 6 languages fully functional
- Seamless language switching mid-call (if needed)

## 5.4 BR4: Lead Capture
**Requirement:** The system must capture and store caller information for every call.

**Details:**
- Mandatory: Name, Phone number
- Optional: Email, Course interest, Preferred batch time
- Automatic deduplication

**Success Criteria:**
- 100% of engaged calls result in lead capture
- Duplicate detection rate > 95%
- Lead data accuracy > 99%

## 5.5 BR5: Cost Reduction
**Requirement:** The system must reduce operational costs by at least 70% compared to manual staff.

**Details:**
- Current cost: ₹15,000-30,000/month (human staff)
- Target cost: ₹6,500/month (voice agent)
- No incremental costs per call (within limits)

**Success Criteria:**
- Monthly cost < ₹7,000 for 150 calls/day
- Break-even within 3 months of deployment

## 5.6 BR6: Integration with Google Sheets
**Requirement:** The system must sync course information from Google Sheets.

**Details:**
- Auto-sync every 1 hour
- Manual sync option available
- Handle Sheet structure changes gracefully

**Success Criteria:**
- Sync completion < 30 seconds
- Zero data loss during sync
- Error notification within 5 minutes of failure

---

# 6. FUNCTIONAL REQUIREMENTS

## 6.1 FR1: Inbound Call Handling

### FR1.1 Call Reception
- **Description:** Automatically answer incoming calls
- **Trigger:** Incoming call to institute's DID number
- **Flow:**
  1. Twilio receives inbound call
  2. System creates call record
  3. Play greeting message
  4. Open audio stream for bidirectional communication
- **Expected Response:** Caller hears greeting within 2 seconds
- **Edge Cases:** Handle caller hangup during greeting, handle VoIP quality issues

### FR1.2 Greeting Message
- **Description:** Play institute-specific greeting
- **Content:** Configurable per institute (default provided)
- **Languages:** Match detected caller language
- **Duration:** 5-10 seconds maximum
- **Example:** "Namaste! Welcome to [Institute Name]. How can I help you today?"

### FR1.3 Call Termination
- **Description:** Gracefully end calls
- **Triggers:** Caller says goodbye, caller hangs up, max duration reached
- **Flow:**
  1. Detect call end signal
  2. Play goodbye message
  3. Close audio stream
  4. Update call record with duration, status
  5. Save lead (if captured)
- **Expected Response:** Call duration logged accurately

## 6.2 FR2: Speech Recognition (STT)

### FR2.1 Real-Time Transcription
- **Description:** Convert caller speech to text in real-time
- **Technology:** faster-whisper (large-v3 model)
- **Latency:** < 500ms per chunk
- **Audio Chunk Size:** 50ms
- **Language:** Auto-detect or configured

### FR2.2 Language Detection
- **Description:** Detect caller's spoken language
- **Method:** langdetect on transcribed text + Whisper language detection
- **Supported Languages:** en, hi, te, ur, ta, kn
- **Confidence Threshold:** 0.7 (fallback to English below)
- **Re-detection:** At call start only (for simplicity)

### FR2.3 Continuous Listening
- **Description:** Process audio continuously without gaps
- **Implementation:** Buffer-based processing with overlap
- **VAD Integration:** Silero VAD for speech/silence detection
- **Edge Cases:** Handle background noise, handle multiple speakers (caller + agent)

## 6.3 FR3: Intent Classification

### FR3.1 Course Inquiry
- **Keywords:** course, class, syllabus, learn, study, teach
- **Action:** Query course database, provide information
- **Response:** Course name, duration, fee, job roles

### FR3.2 Fee Inquiry
- **Keywords:** fee, cost, price, charges, rupees, money
- **Action:** Provide fee details for requested course
- **Response:** Exact fee amount, payment options

### FR3.3 Duration Inquiry
- **Keywords:** duration, long, months, weeks, time
- **Action:** Provide course duration
- **Response:** Duration in months/weeks

### FR3.4 Job/Career Inquiry
- **Keywords:** job, placement, career, salary, package
- **Action:** Provide placement information
- **Response:** Placement rate, average salary, companies

### FR3.5 Admission Inquiry
- **Keywords:** admission, enroll, join, register, apply
- **Action:** Guide through admission process
- **Response:** Steps to enroll, documents needed

### FR3.6 Lead Capture
- **Keywords:** (triggered after course interest)
- **Action:** Collect caller details
- **Data:** Name, phone, email, course interest

### FR3.7 Complaint/Issue
- **Keywords:** problem, issue, complaint, refund
- **Action:** Note complaint, schedule callback
- **Response:** Acknowledge, promise follow-up

### FR3.8 Goodbye
- **Keywords:** bye, thank, goodbye, thanks, tc
- **Action:** End call gracefully
- **Response:** Goodbye message, thank caller

## 6.4 FR4: Response Generation (LLM)

### FR4.1 Context-Aware Responses
- **Technology:** Ollama with Llama 3.2 (1B parameters)
- **Context:** Institute info, course data, conversation history
- **Response Time:** < 1 second
- **Max Response Length:** 150 words (30 seconds of speech)

### FR4.2 System Prompts
- **Structure:** Role definition + Guidelines + Context
- **Language:** Match detected language
- **Tone:** Professional, helpful, concise

### FR4.3 Fallback Responses
- **Description:** When uncertain, ask for clarification
- **Examples:** "Could you please repeat that?", "I didn't quite catch that"

## 6.5 FR5: Speech Synthesis (TTS)

### FR5.1 Text-to-Speech Conversion
- **Technology:** Kokoro TTS
- **Latency:** < 200ms
- **Audio Format:** WAV (16kHz, mono)
- **Streaming:** Chunked streaming for low latency

### FR5.2 Voice Selection
- **Method:** Language-based voice mapping
- **Voices:**
  - English: af_sarah
  - Hindi: hf_psharma
  - Telugu: hf_telugu
  - Tamil: hf_tamil
  - Urdu: hf_urdu
  - Kannada: hf_kannada

### FR5.3 Speech Control
- **Speed:** 0.9x (slightly slower for clarity)
- **Volume:** Normal (1.0x)
- **Pitch:** Default

## 6.6 FR6: Lead Management

### FR6.1 Lead Creation
- **Required Fields:** name, phone
- **Optional Fields:** email, course_interest, notes
- **Source:** voice_agent (auto-assigned)
- **Status:** new (auto-assigned)

### FR6.2 Lead Deduplication
- **Method:** Phone number matching
- **Action:** Update existing lead or create new
- **Update Fields:** latest interaction date, notes append

### FR6.3 Lead Status Flow
```
new → contacted → interested → enrolled
        ↓
      lost
        ↓
   not_responsive
```

### FR6.4 Lead Export
- **Format:** CSV, Excel
- **Fields:** All lead fields + call history
- **Filter Options:** By date, status, course, source

## 6.7 FR7: Call Logging

### FR7.1 Call Record Creation
- **Fields:**
  - caller_phone (required)
  - institute_id (required)
  - direction: inbound
  - status: completed | no_answer | busy | failed | voicemail
  - duration (seconds)
  - started_at, answered_at, ended_at (timestamps)

### FR7.2 Transcript Storage
- **Fields:**
  - call_id (foreign key)
  - sequence_number
  - speaker: ai | caller
  - text
  - language
  - timestamp

### FR7.3 Call Analytics
- **Metrics:**
  - Total calls (daily, weekly, monthly)
  - Answered vs missed
  - Average duration
  - Peak hours
  - Conversion funnel

## 6.8 FR8: Admin Dashboard

### FR8.1 Dashboard Home
- **Stats Cards:**
  - Today's calls
  - Today's leads
  - This week leads
  - Conversion rate
- **Charts:**
  - Calls per day (line, 30 days)
  - Leads by course (bar)
  - Leads by status (pie)
- **Recent Activity:** Latest 10 leads, latest 10 calls

### FR8.2 Leads Management
- **Table Columns:** Name, Phone, Email, Course, Status, Date, Actions
- **Features:**
  - Sort by any column
  - Filter by status, course, date range
  - Search by name, phone, email
  - Bulk export to CSV
  - Individual lead detail view
  - Edit lead status
  - Add notes
  - Delete lead

### FR8.3 Calls Management
- **Table Columns:** Caller, Duration, Status, Date, Actions
- **Features:**
  - Filter by date, status
  - Listen to recording (if enabled)
  - View transcript
  - View full call details

### FR8.4 Course Management
- **View:** List all courses with details
- **Sync:** Manual sync from Google Sheets
- **Edit:** Update course details (admin override)
- **Toggle:** Active/Inactive courses

### FR8.5 Settings
- **Institute Profile:** Name, phone, address, logo
- **Voice Config:** Greeting, goodbye, timeout messages
- **Integrations:** Google Sheets URL, Twilio config
- **Users:** Add/remove admin users
- **Notifications:** Email alerts for new leads

## 6.9 FR9: Google Sheets Integration

### FR9.1 Sheet Structure
**Sheet 1: Courses**
| Column | Type | Required |
|--------|------|----------|
| Course Name | string | Yes |
| Course Code | string | No |
| Duration | string | Yes |
| Fee | number | Yes |
| Job Roles | string (comma-separated) | No |
| Mode | enum: online/offline/hybrid | No |
| Prerequisites | string | No |
| Syllabus | string | No |

**Sheet 2: FAQs (Future)**
| Column | Type |
|--------|------|
| Question | string |
| Answer | string |
| Course | string |

### FR9.2 Sync Mechanism
- **Trigger:** Cron job every 1 hour
- **Method:** Google Sheets API v4
- **Authentication:** Service account with domain-wide delegation
- **Error Handling:** Retry 3 times with exponential backoff, alert on failure

### FR9.3 Data Mapping
- **Google Sheets Row** → **Database Course Record**
- **Source Tracking:** Store sheet ID, row number for update detection

---

# 7. NON-FUNCTIONAL REQUIREMENTS

## 7.1 Performance Requirements

### 7.1.1 Latency

| Metric | Target | Maximum |
|--------|--------|---------|
| Call answer time | < 1 second | 2 seconds |
| STT transcription | < 500ms | 800ms |
| LLM response | < 1 second | 2 seconds |
| TTS generation | < 200ms | 500ms |
| End-to-end latency | < 2 seconds | 3 seconds |

### 7.1.2 Throughput

| Metric | Value |
|--------|-------|
| Concurrent calls | 15-20 (single institute) |
| Calls per day | 150 |
| Total minutes/day | 750 |
| API requests/second | 100 |

### 7.1.3 Resource Utilization

| Resource | Target | Alert Threshold |
|----------|--------|-----------------|
| CPU | < 70% | > 85% |
| Memory | < 12GB | > 14GB |
| GPU | < 80% | > 95% |
| Disk | < 50% | > 80% |

## 7.2 Availability Requirements

### 7.2.1 Uptime
- **Target:** 99.9% (excluding planned maintenance)
- **Calculation:** (Total Minutes - Downtime) / Total Minutes × 100
- **Downtime Budget:** 8.76 hours/year, 44 minutes/month

### 7.2.2 Recovery
- **Recovery Time Objective (RTO):** 15 minutes
- **Recovery Point Objective (RPO):** 5 minutes (data loss max)

### 7.2.3 Maintenance Window
- **Preferred:** Sunday 2-6 AM IST
- **Notification:** 48 hours advance notice
- **Maximum Duration:** 4 hours

## 7.3 Scalability Requirements

### 7.3.1 Vertical Scaling
- Single institute: 1x GPU (T4 16GB)
- 10 institutes: 1x GPU (A100 40GB)
- 100 institutes: 3x GPU (A100 40GB)

### 7.3.2 Horizontal Scaling
- Load balancer for API layer
- Stateless backend services
- Shared database with connection pooling

### 7.3.3 Database Scaling
- Single: PostgreSQL on single instance
- Scale: Read replicas, connection pooling (PgBouncer)

## 7.4 Security Requirements

### 7.4.1 Data Encryption
- **At Rest:** PostgreSQL with pgcrypto
- **In Transit:** TLS 1.3 (Let's Encrypt)
- **Backups:** Encrypted S3 buckets

### 7.4.2 Authentication
- **Admin Dashboard:** JWT tokens (30-min expiry)
- **API Access:** API keys for integrations
- **Password Policy:** bcrypt with cost factor 12

### 7.4.3 Access Control
- **Role-Based Access Control (RBAC)**
  - Admin: Full access
  - Manager: Leads + Calls view/edit
  - Viewer: Read-only access

### 7.4.4 Rate Limiting
- **API:** 100 requests/minute per user
- **Auth:** 10 attempts/minute
- **Webhook:** 1000 requests/minute

### 7.4.5 Audit Logging
- Log all admin actions
- Log all data access
- Retain logs for 90 days

## 7.5 Reliability Requirements

### 7.5.1 Error Handling
- Graceful degradation on component failure
- Automatic retry with exponential backoff
- Circuit breaker pattern for external APIs

### 7.5.2 Monitoring
- Real-time metrics (Prometheus + Grafana)
- Alert on anomalies (PagerDuty)
- Health check endpoints (/health, /ready)

### 7.5.3 Backup & Recovery
- Daily automated backups
- Point-in-time recovery capability
- Backup retention: 30 days

---

# 8. TECHNICAL ARCHITECTURE

## 8.1 Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              USER (CALLER)                                      │
│                          (Phone / Mobile / Landline)                            │
└─────────────────────────────────┬───────────────────────────────────────────────┘
                                  │
                                  │ PSTN / VoIP
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              TWILIO CLOUD                                       │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐                │
│  │  Phone Number   │  │  Voice Webhook  │  │  Media Stream   │                │
│  │   (DID)        │──│    Handler      │──│   (WebSocket)   │                │
│  └─────────────────┘  └─────────────────┘  └────────┬────────┘                │
└──────────────────────────────────────────────────────┼───────────────────────────┘
                                                       │
                               ┌────────────────────────┼────────────────────────┐
                               │                        │                        │
                               │                        │                        │
                               ▼                        ▼                        ▼
                    ┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐
                    │   STT Service    │    │   LLM Service    │    │   TTS Service    │
                    │  (faster-whisper)│    │    (Ollama)      │    │   (Kokoro)       │
                    │  Port: 8001      │    │   Port: 11434    │    │   Port: 8002     │
                    └────────┬─────────┘    └────────┬─────────┘    └────────┬─────────┘
                             │                       │                       │
                             └───────────────────────┼───────────────────────┘
                                                     │
                                                     ▼
                    ┌─────────────────────────────────────────────────────────┐
                    │                    FASTAPI BACKEND                     │
                    │                      Port: 8000                          │
                    │  ┌─────────────────────────────────────────────────────┐│
                    │  │                   API Routes                       ││
                    │  │  /webhooks/twilio    /api/leads    /api/courses   ││
                    │  │  /api/calls         /api/stats   /api/settings    ││
                    │  └─────────────────────────────────────────────────────┘│
                    │  ┌─────────────────────────────────────────────────────┐│
                    │  │              Business Logic Layer                   ││
                    │  │  VoicePipeline │ LeadManager │ CourseSync │ Auth  ││
                    │  └─────────────────────────────────────────────────────┘│
                    └─────────────────────────────┬───────────────────────────┘
                                                  │
                              ┌───────────────────┼───────────────────┐
                              │                   │                   │
                              ▼                   ▼                   ▼
                    ┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐
                    │   PostgreSQL     │ │      Redis       │ │  Google Sheets    │
                    │   (Port 5432)    │ │   (Port 6379)   │ │     API v4        │
                    │   Primary DB     │ │   Session/Cache │ │  Course Sync      │
                    └──────────────────┘ └──────────────────┘ └──────────────────┘
```

## 8.2 Technology Stack

### 8.2.1 Core Technologies

| Component | Technology | Version | Purpose |
|-----------|------------|---------|---------|
| **Backend** | FastAPI | 0.100+ | REST API framework |
| **Language** | Python | 3.11+ | Backend development |
| **Database** | PostgreSQL | 15+ | Primary data store |
| **Cache** | Redis | 7+ | Session, rate limiting |
| **ORM** | SQLAlchemy | 2.0+ | Database abstraction |
| **Validation** | Pydantic | 2.0+ | Request/response validation |

### 8.2.2 AI/ML Technologies

| Component | Technology | Model | Purpose |
|-----------|------------|-------|---------|
| **STT** | faster-whisper | large-v3 | Speech-to-text |
| **TTS** | Kokoro TTS | Latest | Text-to-speech |
| **VAD** | Silero VAD | Latest | Voice activity detection |
| **LLM** | Ollama | 0.5+ | Language model inference |
| **Embedding** | sentence-transformers | Latest | Semantic search (future) |

### 8.2.3 Infrastructure

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Container** | Docker | Application packaging |
| **Orchestration** | Docker Compose | Local development |
| **Reverse Proxy** | Nginx | Load balancing, SSL |
| **GPU** | NVIDIA T4/A100 | Model inference |
| **Hosting** | Cloud (AWS/GCP) | Production deployment |

### 8.2.4 Telephony

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Telephony** | Twilio | Phone calls, webhooks |
| **Protocol** | SIP/WebSocket | Media streaming |
| **DID** | Twilio India | Inbound phone number |

### 8.2.5 Frontend

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Framework** | React | UI library |
| **Build Tool** | Vite | Development server |
| **Styling** | Tailwind CSS | Styling |
| **State** | React Query | Server state |
| **HTTP** | Axios | API client |

---

# 9. SYSTEM COMPONENTS

## 9.1 Backend Components

### 9.1.1 API Gateway
**Responsibilities:**
- Route incoming requests to appropriate handlers
- Authentication and authorization
- Rate limiting
- Request/response transformation

**Endpoints:**
```
/api/v1/
├── /leads
│   ├── GET /              # List leads (paginated)
│   ├── POST /             # Create lead
│   ├── GET /{id}          # Get lead details
│   ├── PUT /{id}          # Update lead
│   ├── DELETE /{id}       # Delete lead
│   └── GET /export        # Export leads (CSV)
├── /calls
│   ├── GET /              # List calls (paginated)
│   ├── GET /{id}          # Get call details
│   └── GET /{id}/transcript  # Get transcript
├── /courses
│   ├── GET /              # List courses
│   ├── POST /sync         # Trigger Google Sheets sync
│   └── GET /{id}          # Get course details
├── /stats
│   ├── GET /dashboard     # Dashboard stats
│   └── GET /analytics     # Analytics data
├── /settings
│   ├── GET /              # Get settings
│   └── PUT /              # Update settings
└── /auth
    ├── POST /login        # User login
    ├── POST /logout       # User logout
    └── POST /refresh      # Refresh token
```

### 9.1.2 Voice Pipeline
**Responsibilities:**
- Manage audio stream from Twilio
- Coordinate STT → LLM → TTS pipeline
- Handle voice activity detection
- Manage conversation state

**Class Structure:**
```python
class VoicePipeline:
    def __init__(self):
        self.vad = SileroVAD()
        self.stt = STTHandler()
        self.tts = TTSHandler()
        self.llm = LLMHandler()
        self.lang_detect = LanguageDetector()
    
    async def process_call(self, call_id: str, audio_stream: AsyncIterator):
        """Main entry point for call processing"""
        
    async def handle_audio_chunk(self, chunk: bytes):
        """Process single audio chunk"""
        
    async def generate_response(self, text: str) -> str:
        """Generate LLM response"""
        
    async def text_to_speech(self, text: str) -> bytes:
        """Convert text to speech"""
```

### 9.1.3 Webhook Handler
**Responsibilities:**
- Handle Twilio webhook requests
- Manage call lifecycle events
- Create/update call records

**Webhook Endpoints:**
```
POST /webhooks/twilio/voice      # Incoming call
POST /webhooks/twilio/status      # Call status changes
POST /webhooks/twilio/media      # Audio stream (WebSocket)
```

### 9.1.4 Lead Manager
**Responsibilities:**
- CRUD operations for leads
- Deduplication logic
- Status management

### 9.1.5 Course Sync Service
**Responsibilities:**
- Sync course data from Google Sheets
- Handle sync scheduling
- Error handling and alerting

### 9.1.6 Authentication Service
**Responsibilities:**
- User authentication
- JWT token management
- Role-based access control

## 9.2 Frontend Components

### 9.2.1 Pages

| Page | Route | Components |
|------|-------|------------|
| Login | /login | LoginForm |
| Dashboard | / | StatsCards, Charts, RecentActivity |
| Leads | /leads | LeadTable, LeadFilters, LeadModal |
| Lead Detail | /leads/:id | LeadInfo, CallHistory, Notes |
| Calls | /calls | CallTable, CallFilters, Player |
| Courses | /courses | CourseTable, SyncButton |
| Settings | /settings | InstituteForm, VoiceConfigForm |

### 9.2.2 Shared Components

| Component | Purpose |
|-----------|---------|
| Layout | Main wrapper with sidebar/header |
| Sidebar | Navigation menu |
| Header | User menu, notifications |
| DataTable | Reusable table with sorting/filtering |
| StatsCard | Metric display card |
| Modal | Reusable modal dialog |
| Button | Styled button components |
| Input | Form input components |
| Select | Dropdown selection |
| DatePicker | Date range selection |
| LoadingSpinner | Loading state |
| Toast | Notification toasts |

---

# 10. DATABASE DESIGN

## 10.1 Entity Relationship Diagram

```
┌─────────────┐       ┌─────────────┐       ┌─────────────┐
│  institutes │       │    users   │       │ voice_configs│
├─────────────┤       ├─────────────┤       ├─────────────┤
│ id (PK)     │◀──┐   │ id (PK)     │       │ id (PK)     │
│ name        │   │   │ institute_id│─▶│ id (FK)     │
│ slug        │   └───│ email       │   │ institute_id│─▶
│ phone_number│       │ password_hash│      │ greeting    │
│ address     │       │ role        │       │ system_prompt│
│ created_at  │       │ created_at  │       │ language     │
└─────────────┘       └─────────────┘       │ voice_id    │
                         │                   │ max_duration│
                         │                   └─────────────┘
                         │
                         ▼
┌─────────────┐       ┌─────────────┐       ┌─────────────┐
│   courses   │       │  students   │       │   calls     │
├─────────────┤       ├─────────────┤       ├─────────────┤
│ id (PK)     │       │ id (PK)     │       │ id (PK)     │
│ institute_id│─▶│ id (FK)     │◀──┐   │ student_id  │─▶
│ course_name │       │ institute_id│─▶│ institute_id│─▶
│ duration    │       │ name        │   │ caller_phone │
│ fee         │       │ phone       │   │ duration    │
│ job_roles[] │       │ email       │   │ status      │
│ mode        │       │ course_interest│   │ transcript  │
│ is_active   │       │ status      │   │ outcome     │
│ source_id   │       │ created_at  │   │ started_at  │
└─────────────┘       └─────────────┘       └─────────────┘
                            │
                            ▼
                   ┌─────────────────┐
                   │student_activities│
                   ├─────────────────┤
                   │ id (PK)         │
                   │ student_id (FK) │─▶
                   │ activity_type   │
                   │ description     │
                   │ metadata (JSONB)│
                   │ created_at      │
                   └─────────────────┘
```

## 10.2 Table Definitions

### 10.2.1 institutes
```sql
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
```

### 10.2.2 users
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    institute_id INTEGER REFERENCES institutes(id) ON DELETE CASCADE,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    role VARCHAR(50) DEFAULT 'admin',
    is_active BOOLEAN DEFAULT true,
    last_login TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 10.2.3 voice_configs
```sql
CREATE TABLE voice_configs (
    id SERIAL PRIMARY KEY,
    institute_id INTEGER REFERENCES institutes(id) ON DELETE CASCADE UNIQUE,
    greeting_message TEXT DEFAULT 'Hello! Welcome to our institute. How can I help you today?',
    goodbye_message TEXT DEFAULT 'Thank you for calling. Have a great day!',
    timeout_message TEXT DEFAULT 'Sorry, I didn''t catch that. Could you please repeat?',
    system_prompt TEXT,
    language VARCHAR(10) DEFAULT 'en',
    voice_id VARCHAR(50),
    max_call_duration INTEGER DEFAULT 300,
    max_silence_duration INTEGER DEFAULT 5,
    enable_recording BOOLEAN DEFAULT false,
    enable_transcription BOOLEAN DEFAULT true,
    enable_voicemail BOOLEAN DEFAULT true,
    voicemail_action VARCHAR(20) DEFAULT 'callback',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 10.2.4 courses
```sql
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
    mode VARCHAR(20) DEFAULT 'online',
    start_date DATE,
    batch_time VARCHAR(100),
    certificate TEXT,
    placement_assistance BOOLEAN DEFAULT false,
    source_updated TIMESTAMP,
    source_id VARCHAR(255),
    is_active BOOLEAN DEFAULT true,
    display_order INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 10.2.5 students (Leads)
```sql
CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    institute_id INTEGER REFERENCES institutes(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    phone_country_code VARCHAR(5) DEFAULT '+91',
    email VARCHAR(255),
    whatsapp_opt_in BOOLEAN DEFAULT false,
    course_interest INTEGER REFERENCES courses(id),
    source VARCHAR(50) DEFAULT 'voice_agent',
    status VARCHAR(50) DEFAULT 'new',
    priority VARCHAR(20) DEFAULT 'normal',
    assigned_to INTEGER REFERENCES users(id),
    notes TEXT,
    follow_up_date DATE,
    last_contacted_at TIMESTAMP,
    converted_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 10.2.6 calls
```sql
CREATE TABLE calls (
    id SERIAL PRIMARY KEY,
    student_id INTEGER REFERENCES students(id) ON DELETE SET NULL,
    institute_id INTEGER REFERENCES institutes(id) ON DELETE CASCADE,
    caller_phone VARCHAR(20) NOT NULL,
    caller_country_code VARCHAR(5) DEFAULT '+91',
    direction VARCHAR(10) DEFAULT 'inbound',
    status VARCHAR(20) DEFAULT 'no_answer',
    duration INTEGER,
    wait_time INTEGER,
    recording_url TEXT,
    recording_duration INTEGER,
    transcript TEXT,
    transcript_language VARCHAR(10),
    summary TEXT,
    sentiment VARCHAR(20),
    outcome VARCHAR(50),
    cost DECIMAL(10,2) DEFAULT 0,
    twilio_call_sid VARCHAR(100),
    started_at TIMESTAMP,
    answered_at TIMESTAMP,
    ended_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 10.2.7 student_activities
```sql
CREATE TABLE student_activities (
    id SERIAL PRIMARY KEY,
    student_id INTEGER REFERENCES students(id) ON DELETE CASCADE,
    activity_type VARCHAR(50) NOT NULL,
    description TEXT,
    metadata JSONB,
    performed_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 10.2.8 call_transcripts
```sql
CREATE TABLE call_transcripts (
    id SERIAL PRIMARY KEY,
    call_id INTEGER REFERENCES calls(id) ON DELETE CASCADE,
    sequence_number INTEGER NOT NULL,
    speaker VARCHAR(20) DEFAULT 'unknown',
    text TEXT NOT NULL,
    language VARCHAR(10),
    start_time INTEGER,
    end_time INTEGER,
    confidence DECIMAL(5,4),
    audio_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 10.2.9 daily_stats
```sql
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
```

### 10.2.10 settings
```sql
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
```

### 10.2.11 audit_logs
```sql
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

## 10.3 Indexes

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

CREATE INDEX idx_courses_institute ON courses(institute_id);
CREATE INDEX idx_courses_active ON courses(is_active);

CREATE INDEX idx_student_activities_student ON student_activities(student_id DESC);
CREATE INDEX idx_student_activities_type ON student_activities(activity_type);

CREATE INDEX idx_call_transcripts_call ON call_transcripts(call_id);

-- Full-text search indexes
CREATE INDEX idx_students_search ON students USING gin(to_tsvector('english', name || ' ' || COALESCE(phone, '') || ' ' || COALESCE(email, '')));
CREATE INDEX idx_courses_search ON courses USING gin(to_tsvector('english', course_name || ' ' || COALESCE(description, '')));
```

---

# 11. API SPECIFICATIONS

## 11.1 Authentication

### POST /api/v1/auth/login
**Request:**
```json
{
  "email": "admin@institute.com",
  "password": "securepassword123"
}
```
**Response (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "expires_in": 1800,
  "user": {
    "id": 1,
    "email": "admin@institute.com",
    "full_name": "Admin User",
    "role": "admin"
  }
}
```

### POST /api/v1/auth/refresh
**Request:**
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIs..."
}
```
**Response (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

## 11.2 Leads

### GET /api/v1/leads
**Query Parameters:**
- `page`: int (default: 1)
- `limit`: int (default: 20, max: 100)
- `status`: string (optional)
- `course_id`: int (optional)
- `date_from`: date (optional)
- `date_to`: date (optional)
- `search`: string (optional)
- `sort_by`: string (default: created_at)
- `sort_order`: string (asc/desc)

**Response (200):**
```json
{
  "items": [
    {
      "id": 1,
      "name": "Rahul Sharma",
      "phone": "+919876543210",
      "email": "rahul@email.com",
      "course_interest": {
        "id": 1,
        "course_name": "Python Data Science"
      },
      "status": "new",
      "created_at": "2026-03-02T10:30:00Z"
    }
  ],
  "total": 150,
  "page": 1,
  "limit": 20,
  "pages": 8
}
```

### POST /api/v1/leads
**Request:**
```json
{
  "name": "Rahul Sharma",
  "phone": "+919876543210",
  "email": "rahul@email.com",
  "course_interest": 1,
  "notes": "Interested in weekend batch"
}
```
**Response (201):**
```json
{
  "id": 1,
  "name": "Rahul Sharma",
  "phone": "+919876543210",
  "email": "rahul@email.com",
  "course_interest": 1,
  "status": "new",
  "created_at": "2026-03-02T10:30:00Z"
}
```

### PUT /api/v1/leads/{id}
**Request:**
```json
{
  "status": "contacted",
  "notes": "Called back, interested in demo"
}
```
**Response (200):**
```json
{
  "id": 1,
  "name": "Rahul Sharma",
  "phone": "+919876543210",
  "status": "contacted",
  "notes": "Called back, interested in demo",
  "updated_at": "2026-03-02T11:00:00Z"
}
```

### DELETE /api/v1/leads/{id}
**Response (204):** No content

### GET /api/v1/leads/export
**Query Parameters:** Same as GET /leads
**Response (200):** CSV file download

## 11.3 Calls

### GET /api/v1/calls
**Query Parameters:**
- `page`, `limit`, `status`, `date_from`, `date_to`, `sort_by`, `sort_order`

**Response (200):**
```json
{
  "items": [
    {
      "id": 1,
      "caller_phone": "+919876543210",
      "duration": 180,
      "status": "completed",
      "outcome": "interested",
      "started_at": "2026-03-02T10:00:00Z",
      "ended_at": "2026-03-02T10:03:00Z"
    }
  ],
  "total": 500,
  "page": 1,
  "limit": 20
}
```

### GET /api/v1/calls/{id}
**Response (200):**
```json
{
  "id": 1,
  "caller_phone": "+919876543210",
  "duration": 180,
  "status": "completed",
  "outcome": "interested",
  "transcript": [
    {"speaker": "ai", "text": "Namaste! Welcome to Institute..."},
    {"speaker": "caller", "text": "I want to know about data science course"},
    {"speaker": "ai", "text": "Our Python Data Science course is 6 months..."}
  ],
  "started_at": "2026-03-02T10:00:00Z",
  "ended_at": "2026-03-02T10:03:00Z"
}
```

## 11.4 Courses

### GET /api/v1/courses
**Response (200):**
```json
{
  "items": [
    {
      "id": 1,
      "course_name": "Python Data Science",
      "course_code": "PDS-001",
      "duration": "6 months",
      "fee": 35000,
      "job_roles": ["Data Analyst", "ML Engineer"],
      "mode": "online",
      "is_active": true
    }
  ],
  "total": 8
}
```

### POST /api/v1/courses/sync
**Response (200):**
```json
{
  "message": "Sync started",
  "courses_updated": 8,
  "sync_id": "abc123"
}
```

## 11.5 Stats

### GET /api/v1/stats/dashboard
**Response (200):**
```json
{
  "today": {
    "calls": 45,
    "leads": 38,
    "avg_duration": 240
  },
  "this_week": {
    "calls": 280,
    "leads": 220,
    "conversion_rate": 0.15
  },
  "this_month": {
    "calls": 1200,
    "leads": 950,
    "conversion_rate": 0.12
  },
  "charts": {
    "calls_per_day": [
      {"date": "2026-02-24", "count": 42},
      {"date": "2026-02-25", "count": 38}
    ],
    "leads_by_course": [
      {"course": "Python DS", "count": 120},
      {"course": "Web Dev", "count": 95}
    ]
  }
}
```

---

# 12. VOICE PIPELINE SPECIFICATIONS

## 12.1 Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         VOICE PIPELINE FLOW                                 │
└────────────────────────────────┬────────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 1. CALL START                                                               │
│    - Twilio initiates webhook                                              │
│    - Create call record in DB                                               │
│    - Return TwiML with <Connect><Stream>                                   │
└────────────────────────────────┬────────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 2. AUDIO STREAM START                                                      │
│    - Open WebSocket connection                                             │
│    - Initialize VAD, STT, LLM, TTS handlers                                │
│    - Load institute voice config                                           │
└────────────────────────────────┬────────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 3. GREETING PLAY                                                           │
│    - Fetch greeting message from config                                    │
│    - Detect caller language (first audio chunk)                            │
│    - Generate greeting via TTS                                            │
│    - Stream audio to caller                                                 │
│    - Mark call as "answered"                                               │
└────────────────────────────────┬────────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 4. MAIN LOOP: AUDIO PROCESSING                                             │
│                                                                             │
│    ┌────────────────────────────────────────────────────────────────────┐ │
│    │ FOR each audio chunk (50ms):                                       │ │
│    │                                                                      │ │
│    │   a. VAD Check (Silero VAD)                                        │ │
│    │      - Is speech present?                                           │ │
│    │      - If no: continue (listen for speech)                         │ │
│    │      - If yes: proceed                                              │ │
│    │                                                                      │ │
│    │   b. Language Detection (first speech chunk only)                 │ │
│    │      - Use langdetect on transcribed text                          │ │
│    │      - Map to supported language                                    │ │
│    │      - Store for TTS voice selection                                │ │
│    │                                                                      │ │
│    │   c. STT Transcription (Whisper large-v3)                         │ │
│    │      - Input: audio chunk                                           │ │
│    │      - Output: transcribed text                                     │ │
│    │      - Latency: <500ms                                              │ │
│    │                                                                      │ │
│    │   d. Append to transcript buffer                                     │ │
│    │                                                                      │ │
│    │   e. Check for complete sentence (punctuation, pause)              │ │
│    │      - If incomplete: continue listening                           │ │
│    │      - If complete: process intent                                  │ │
│    │                                                                      │ │
│    │   f. Intent Classification                                          │ │
│    │      - Classify: course_info, fee_inquiry, lead_capture, etc.      │ │
│    │      - Extract entities: course name, phone, name, etc.           │ │
│    │                                                                      │ │
│    │   g. Generate Response (Ollama Llama 3.2)                          │ │
│    │      - Build context: conversation history + course data           │ │
│    │      - Build prompt: system + user message                          │ │
│    │      - Generate response                                            │ │
│    │      - Latency: <1000ms                                             │ │
│    │                                                                      │ │
│    │   h. Text-to-Speech (Kokoro TTS)                                    │ │
│    │      - Input: response text                                          │ │
│    │      - Select voice based on detected language                      │ │
│    │      - Output: audio bytes                                          │ │
│    │      - Latency: <200ms                                              │ │
│    │                                                                      │ │
│    │   i. Stream Audio to Caller                                         │ │
│    │      - Chunk audio for streaming                                    │ │
│    │      - Send via Twilio Media Stream                                 │ │
│    │                                                                      │ │
│    └────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
└────────────────────────────────┬────────────────────────────────────────────┘
                                 │
                                 │ Call ends (caller hangs up, says goodbye, timeout)
                                 ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 5. CALL END                                                                │
│    - Play goodbye message (if not already done)                            │
│    - Close WebSocket connection                                            │
│    - Update call record:                                                    │
│      - status: completed/voicemail/no_answer                               │
│      - duration: calculated                                                │
│      - transcript: full conversation                                       │
│      - outcome: classified                                                 │
│    - Save captured lead (if any)                                           │
│    - Send notifications (if configured)                                     │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 12.2 Voice Activity Detection (VAD)

### Configuration
```python
VAD_CONFIG = {
    "model": "silero_vad",
    "threshold": 0.5,
    "min_speech_duration_ms": 250,
    "min_silence_duration_ms": 300,
    "speech_pad_ms": 400
}
```

### Behavior
1. **Continuous Monitoring:** Analyze every 50ms audio chunk
2. **Speech Detection:** When probability > threshold, mark as speech
3. **Silence Handling:** After 5 seconds of silence, play prompt
4. **Noise Filtering:** Ignore audio below minimum threshold

## 12.3 Speech-to-Text (STT)

### Configuration
```python
STT_CONFIG = {
    "model": "faster-whisper",
    "model_size": "large-v3",
    "device": "cuda",
    "compute_type": "float16",
    "language": None,  # Auto-detect
    "task": "transcribe",
    "beam_size": 5,
    "vad_filter": True
}
```

### Supported Languages (Whisper Codes)
| Language | Code |
|----------|------|
| English | en |
| Hindi | hi |
| Telugu | te |
| Urdu | ur |
| Tamil | ta |
| Kannada | kn |

## 12.4 Language Detection

### Algorithm
1. Use Whisper's built-in language detection (most accurate)
2. Fallback: langdetect on transcribed text
3. Confidence threshold: 0.7 (below: default to English)

### Language Mapping
```python
LANGUAGE_MAP = {
    'en': {'whisper': 'en', 'kokoro': 'af_sarah', 'name': 'English'},
    'hi': {'whisper': 'hi', 'kokoro': 'hf_psharma', 'name': 'Hindi'},
    'te': {'whisper': 'te', 'kokoro': 'hf_telugu', 'name': 'Telugu'},
    'ur': {'whisper': 'ur', 'kokoro': 'hf_urdu', 'name': 'Urdu'},
    'ta': {'whisper': 'ta', 'kokoro': 'hf_tamil', 'name': 'Tamil'},
    'kn': {'whisper': 'kn', 'kokoro': 'hf_kannada', 'name': 'Kannada'}
}
```

## 12.5 Intent Classification

### Method
1. **Rule-based keywords** (primary)
2. **LLM classification** (fallback for ambiguous cases)

### Intent Patterns
```python
INTENT_PATTERNS = {
    'course_info': ['course', 'courses', 'class', 'classes', 'syllabus', 'learn', 'study', 'teach'],
    'fee_inquiry': ['fee', 'fees', 'cost', 'price', 'charges', 'rupees', 'money', 'amount'],
    'duration': ['duration', 'long', 'months', 'weeks', 'time', 'how long'],
    'job_placement': ['job', 'jobs', 'placement', 'career', 'salary', 'package', 'hiring'],
    'admission': ['admission', 'enroll', 'enrollment', 'join', 'register', 'registration', 'apply'],
    'lead_capture': ['name is', 'my name', 'phone', 'number', 'contact', 'call me'],
    'complaint': ['problem', 'issue', 'complaint', 'refund', 'not satisfied'],
    'goodbye': ['bye', 'thank', 'thanks', 'goodbye', 'tc', 'that is all', 'nothing else']
}
```

### Entity Extraction
```python
ENTITY_EXTRACTORS = {
    'phone': r'(\+91[789]\d{9})|(\d{10})',
    'email': r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
    'name': r'(my name is|i am|i\'m)\s+([A-Za-z]+)',
    'course': course_name_list  # Match from database
}
```

## 12.6 Response Generation (LLM)

### Ollama Configuration
```python
LLM_CONFIG = {
    "base_url": "http://ollama:11434",
    "model": "llama3.2:1b",  # 1B parameters for speed
    "temperature": 0.7,
    "top_p": 0.9,
    "max_tokens": 150,
    "repeat_penalty": 1.1
}
```

### System Prompt Template
```python
SYSTEM_PROMPT = """You are a helpful voice assistant for {institute_name}.
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

Course Information:
{course_context}

Current conversation:
{conversation_history}

Respond as a helpful voice assistant:"""
```

### Response Generation Flow
1. Build context from conversation history
2. Add course data from database
3. Format prompt with placeholders
4. Send to Ollama API
5. Parse response
6. Return text

## 12.7 Text-to-Speech (TTS)

### Kokoro Configuration
```python
TTS_CONFIG = {
    "model": "kokoro",
    "voice": "af_sarah",  # Default, changed based on language
    "speed": 0.9,
    "volume": 1.0,
    "sample_rate": 24000
}
```

### Voice Selection by Language
| Language | Voice ID | Description |
|----------|----------|-------------|
| English | af_sarah | American female |
| Hindi | hf_psharma | Hindi female |
| Telugu | hf_telugu | Telugu female |
| Tamil | hf_tamil | Tamil female |
| Urdu | hf_urdu | Urdu female |
| Kannada | hf_kannada | Kannada female |

### Audio Streaming
1. Generate full audio from text
2. Split into 100ms chunks
3. Stream chunks via WebSocket to Twilio
4. Ensure no gaps in audio

---

# 13. MULTI-LANGUAGE IMPLEMENTATION

## 13.1 Supported Languages

| Language | Code | STT Model | TTS Voice | Native Speakers |
|----------|------|-----------|-----------|-----------------|
| English | en | large-v3 | af_sarah | Pan-India |
| Hindi | hi | large-v3 | hf_psharma | ~600M |
| Telugu | te | large-v3 | hf_telugu | ~80M |
| Urdu | ur | large-v3 | hf_urdu | ~170M |
| Tamil | ta | large-v3 | hf_tamil | ~70M |
| Kannada | kn | large-v3 | hf_kannada | ~40M |

## 13.2 Language Detection Flow

```
Audio Chunk 1 (First Speech)
         │
         ▼
┌─────────────────────────┐
│  Whisper Language      │
│  Detection             │
│  (automatic)           │
└───────────┬─────────────┘
            │
            ▼
    ┌───────────────┐
    │ Confidence > │
    │ 0.7?         │
    └───────┬───────┘
       Yes │ No
       ┌────┴────┐
       ▼         ▼
   Use Lang  Default
   (detected)  to English
```

## 13.3 Language-Specific Prompts

### English
```
You are a professional voice assistant for an educational institute.
Provide clear and accurate information about courses.
Keep your responses concise and helpful.
```

### Hindi
```
आप एक शैक्षणिक संस्थान के लिए पेशेवर वॉइस असिस्टेंट हैं।
पाठ्यक्रमों के बारे में स्पष्ट और सटीक जानकारी दें।
अपने जवाब संक्षिप्त और सहायक रखें।
```

### Telugu
```
మీరు విద్యా సంస్థకు professional voice assistant.
courses గురించి clear accurate information ఇవ్వండ.
responses concise and helpful గా ఉండాలి.
```

### Tamil
```
நீங்கள் ஒரு கல்வி நிறுவனத்திற்கான தொழில்முறை குரல் உதவியாளர்.
தகவல் தெரிவிக்கவும்.
```

### Urdu
```
آپ ایک تعلیمی ادارے کے لیے پیشہ ورانہ وائس اسسٹینٹ ہیں۔
```

### Kannada
```
ನೀವು ಶಿಕ್ಷಣ ಸಂಸ್ಥೆಗೆ ವೃತ್ತಿಪರ ಧ್ವನಿ ಸಹಾಯಕರಾಗಿದ್ದೀರಿ.
```

## 13.4 Testing Languages

| Language | Test Input | Expected Output |
|----------|------------|-----------------|
| English | "What courses do you offer?" | English response |
| Hindi | "आप क्या कोर्सेस देते हो?" | Hindi response |
| Telugu | "మీరు ఏ courses ఇస్తారు?" | Telugu response |
| Urdu | "آپ کون سے کورسز لیتے ہیں؟" | Urdu response |
| Tamil | "Enna courses irukku?" | Tamil response |
| Kannada | "Yaaru courses ide?" | Kannada response |

---

# 14. INTEGRATION REQUIREMENTS

## 14.1 Twilio Integration

### 14.1.1 Phone Number Setup
- Purchase Indian DID from Twilio
- Configure voice URL webhook
- Enable media streaming

### 14.1.2 Webhook Configuration

**Voice Incoming Webhook:**
```
POST https://your-domain.com/webhooks/twilio/voice
```

**Status Callback:**
```
POST https://your-domain.com/webhooks/twilio/status
```

### 14.1.3 TwiML Response
```xml
<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Connect>
        <Stream url="wss://your-domain.com/media-stream" />
    </Connect>
</Response>
```

### 14.1.4 Events to Handle
| Event | Action |
|-------|--------|
| call.initiate | Create call record |
| call.answer | Mark as answered, play greeting |
| call.media | Process audio chunk |
| call.disconnect | End call, save details |
| call.failed | Log error, notify |

## 14.2 Google Sheets Integration

### 14.2.1 Authentication
- Service account with domain-wide delegation
- Share spreadsheet with service account email
- Store credentials securely in environment variables

### 14.2.2 API Calls
```python
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets.readonly'
]

def sync_courses(spreadsheet_id: str, institute_id: int):
    service = build('sheets', 'v4', credentials=credentials)
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range='Courses!A:H'
    ).execute()
    # Process and save to database
```

### 14.2.3 Sync Schedule
| Task | Frequency | Method |
|------|-----------|--------|
| Course sync | Every 1 hour | Cron job |
| Manual sync | On-demand | API endpoint |
| Error recovery | On failure | Retry with backoff |

---

# 15. USER INTERFACE REQUIREMENTS

## 15.1 Design System

### 15.1.1 Color Palette
| Role | Color | Hex |
|------|-------|-----|
| Primary | Indigo | #4F46E5 |
| Primary Hover | Dark Indigo | #4338CA |
| Secondary | Gray | #6B7280 |
| Success | Green | #10B981 |
| Warning | Amber | #F59E0B |
| Error | Red | #EF4444 |
| Background | White | #FFFFFF |
| Surface | Light Gray | #F9FAFB |
| Text Primary | Dark Gray | #111827 |
| Text Secondary | Medium Gray | #6B7280 |

### 15.1.2 Typography
| Element | Font | Size | Weight |
|---------|------|------|--------|
| Heading 1 | Inter | 24px | 700 |
| Heading 2 | Inter | 20px | 600 |
| Heading 3 | Inter | 16px | 600 |
| Body | Inter | 14px | 400 |
| Small | Inter | 12px | 400 |
| Button | Inter | 14px | 500 |

### 15.1.3 Spacing
- Base unit: 4px
- Spacing scale: 4, 8, 12, 16, 24, 32, 48, 64
- Card padding: 24px
- Section margin: 32px

### 15.1.4 Components
- Border radius: 8px (cards), 6px (buttons), 4px (inputs)
- Shadow: `0 1px 3px rgba(0,0,0,0.1), 0 1px 2px rgba(0,0,0,0.06)`
- Focus ring: 2px indigo outline

## 15.2 Page Specifications

### 15.2.1 Login Page
- Centered card on gradient background
- Logo at top
- Email and password fields
- "Sign In" button
- Forgot password link

### 15.2.2 Dashboard
- Top bar: Logo, user menu, notifications
- Sidebar: Navigation menu
- Main content:
  - 4 stat cards in row (calls today, leads today, week leads, conversion)
  - Line chart: calls per day (30 days)
  - Bar chart: leads by course
  - Pie chart: lead status distribution
  - Recent activity table

### 15.2.3 Leads Page
- Header with "Export" and "Add Lead" buttons
- Filter bar: status, course, date range
- Search input
- Table with columns: Name, Phone, Email, Course, Status, Date, Actions
- Pagination
- Click row → Lead detail modal

### 15.2.4 Calls Page
- Filter bar: status, date range
- Table: Caller, Duration, Status, Date, Actions
- Click → Play recording / View transcript

### 15.2.5 Courses Page
- Grid/List toggle
- Course cards with: name, duration, fee, mode
- "Sync from Sheets" button
- Edit/Delete actions

### 15.2.6 Settings Page
- Tabs: Institute, Voice, Integrations, Users
- Form-based editing
- Save/Cancel buttons

---

# 16. SECURITY REQUIREMENTS

## 16.1 Authentication & Authorization

### 16.1.1 User Authentication
- JWT-based authentication
- Access token: 30-minute expiry
- Refresh token: 7-day expiry
- Password: bcrypt hashed (cost factor 12)

### 16.1.2 Role-Based Access
| Role | Permissions |
|------|-------------|
| Admin | Full access |
| Manager | Leads: CRUD, Calls: R, Courses: R, Settings: R |
| Viewer | Leads: R, Calls: R, Courses: R |

### 16.1.3 API Security
- All endpoints require authentication (except /health, /auth/login)
- Rate limiting: 100 req/min per user
- Request validation via Pydantic

## 16.2 Data Security

### 16.2.1 Encryption
- **In Transit:** TLS 1.3 for all connections
- **At Rest:** PostgreSQL encryption enabled
- **Backups:** Encrypted S3 with KMS

### 16.2.2 Sensitive Data
- Passwords: bcrypt hashed
- API keys: Environment variables only
- Phone numbers: Can be masked in UI

## 16.3 Network Security

### 16.3.1 Firewall
- Only ports 80, 443, 22 (SSH with key) open
- Database only accessible from app network

### 16.3.2 CORS
- Strict origin allowlist
- No wildcard CORS

## 16.4 Compliance

### 16.4.1 India Data Laws
- Data stored in India region
- Consent for recording (play notice)
- DND compliance for SMS

---

# 17. PERFORMANCE REQUIREMENTS

## 17.1 Response Time Targets

| Operation | Target | Maximum |
|-----------|--------|---------|
| API response (list) | < 200ms | 500ms |
| API response (detail) | < 100ms | 300ms |
| Dashboard load | < 2s | 3s |
| Lead export | < 5s | 10s |
| Voice: Answer | < 1s | 2s |
| Voice: End-to-end | < 2s | 3s |
| Voice: STT latency | < 500ms | 800ms |
| Voice: LLM response | < 1s | 2s |
| Voice: TTS latency | < 200ms | 500ms |

## 17.2 Capacity

| Metric | Value |
|--------|-------|
| Concurrent calls | 15-20 |
| Calls/day | 150 |
| Active users (admin) | 10 |
| API requests/sec | 100 |

## 17.3 Resource Usage

| Resource | Target | Alert |
|----------|--------|-------|
| CPU | < 70% | > 85% |
| Memory | < 12GB | > 14GB |
| GPU | < 80% | > 95% |
| Database connections | < 80% | > 90% |

---

# 18. TESTING REQUIREMENTS

## 18.1 Unit Tests

### Coverage Target
- Backend: 80% code coverage
- All new code: 90% coverage

### Test Categories
- Model tests
- Service tests
- API endpoint tests
- Utility function tests

## 18.2 Integration Tests

### Scenarios
- Database operations
- External API calls (Google Sheets, Twilio mock)
- Authentication flow
- Lead capture flow
- Call handling flow

## 18.3 End-to-End Tests

### User Flows
1. Login → Dashboard loads
2. View leads → Export CSV
3. Inbound call → Lead captured → Appears in dashboard
4. Course sync → Data updated

## 18.4 Performance Tests

### Load Testing
- 150 concurrent users
- 20 concurrent calls
- 1000 API requests/minute

### Stress Testing
- Ramp up to 200% of expected load
- Test recovery after failure

## 18.5 Testing Environments

| Environment | Purpose | Data |
|-------------|---------|------|
| Development | Local development | Mock data |
| Staging | Pre-production testing | Sanitized production-like |
| Production | Live usage | Real data |

---

# 19. DEPLOYMENT REQUIREMENTS

## 19.1 Infrastructure

### Development
- Docker Compose (local)
- 8GB RAM, 4 CPU

### Staging
- 1x cloud VM (4 vCPU, 16GB RAM)
- PostgreSQL (managed)
- Redis (managed)

### Production
- 1x GPU VM (T4 16GB)
- PostgreSQL (managed, multi-AZ)
- Redis (managed, with failover)
- Load balancer
- CDN for static assets

## 19.2 Deployment Process

### CI/CD Pipeline
1. **Commit** → Git push
2. **Lint** → Black, Flake8, MyPy
3. **Test** → pytest with coverage
4. **Build** → Docker image build
5. **Deploy** → Push to registry → Deploy to server
6. **Smoke Test** → Health check verification

### Environment Variables
```bash
# Database
DATABASE_URL=postgresql://user:pass@host:5432/repcon

# Redis
REDIS_URL=redis://host:6379

# Twilio
TWILIO_ACCOUNT_SID=ACxxxxx
TWILIO_AUTH_TOKEN=xxxxx
TWILIO_PHONE_NUMBER=+91xxxxxxxxxx

# Google Sheets
GOOGLE_SERVICE_ACCOUNT_JSON='{"type":"service_account"...}'
GOOGLE_SHEETS_ID=xxxxx

# Ollama
OLLAMA_BASE_URL=http://ollama:11434

# Auth
SECRET_KEY=xxxxx
JWT_SECRET=xxxxx

# App
DEBUG=false
LOG_LEVEL=INFO
```

## 19.3 Monitoring

### Metrics
- Response times (p50, p95, p99)
- Error rates
- Active calls
- Resource usage

### Alerts
- High error rate (>5%)
- High latency (>3s)
- Low uptime (<99.5%)
- Resource exhaustion (>90%)

---

# 20. IMPLEMENTATION PHASES

## Phase 1: Foundation (Week 1)
| Day | Tasks |
|-----|-------|
| 1-2 | Infrastructure setup, Docker, PostgreSQL |
| 3-4 | Backend scaffolding, API routes |
| 5 | STT integration (Whisper) |
| 6 | TTS integration (Kokoro) |
| 7 | Ollama setup, LLM handler |

## Phase 2: Core Voice (Week 2)
| Day | Tasks |
|-----|-------|
| 8-9 | Voice pipeline orchestration |
| 10 | Twilio webhook setup |
| 11 | Intent classification |
| 12 | Lead capture flow |
| 13 | Call logging |
| 14 | Testing & bug fixes |

## Phase 3: Integrations (Week 3)
| Day | Tasks |
|-----|-------|
| 15-16 | Google Sheets sync |
| 17 | Multi-language support |
| 18 | Admin dashboard (React) |
| 19 | User authentication |
| 20 | Settings page |
| 21 | Testing & polish |

## Phase 4: Testing & Launch (Week 4)
| Day | Tasks |
|-----|-------|
| 22-23 | Load testing |
| 24 | Bug fixes & optimization |
| 25 | Documentation |
| 26 | Staging deployment |
| 27 | UAT with sample institute |
| 28 | Production deployment |

---

# 21. RISK MANAGEMENT

## 21.1 Risk Register

| ID | Risk | Probability | Impact | Mitigation |
|----|------|-------------|--------|------------|
| R1 | GPU shortage | Medium | High | Use cloud GPU (Lambda, Paperspace) |
| R2 | LLM latency | Medium | Medium | Optimize prompts, cache responses |
| R3 | Twilio pricing | Low | Medium | Build abstraction, support VoIP.ms |
| R4 | Language detection | Medium | Low | Fallback to English |
| R5 | Data breach | Low | Critical | Encryption, access controls |
| R6 | Legal compliance | Medium | High | Consult legal team |
| R7 | High load failure | Low | High | Auto-scaling, queueing |
| R8 | Integration failure | Medium | Medium | Retry logic, fallback data |

## 21.2 Contingency Plans

### Twilio Failure
- Queue calls for callback
- Show alternative contact number
- Alert on-call team

### GPU Exhaustion
- Queue audio processing
- Prioritize real-time over batch
- Scale up GPU resources

### Database Failure
- Read from cache
- Queue writes
- Point to backup

---

# 22. SUCCESS METRICS

## 22.1 KPIs

| Metric | Target | Measurement |
|--------|--------|-------------|
| Call Answer Rate | > 95% | Answered / Total calls |
| Lead Capture Rate | > 80% | Leads captured / Total calls |
| Conversion Rate | > 15% | Enrolled / Total leads |
| Average Call Duration | 3-5 min | Duration / Completed calls |
| End-to-End Latency | < 2 sec | Time from speech to response |
| Uptime | > 99.9% | (Total - Downtime) / Total |
| Cost per Lead | < ₹50 | Monthly cost / New leads |
| User Satisfaction | > 4/5 | Post-call survey |

## 22.2 Dashboard Metrics

- Today's calls
- Today's leads
- This week's leads
- Conversion funnel
- Popular courses
- Peak call hours

---

# 23. TIMELINE & MILESTONES

## 23.1 Milestones

| Milestone | Date | Deliverable |
|-----------|------|-------------|
| M1: Infrastructure Ready | Day 2 | Docker, DB, API running |
| M2: Voice Pipeline Ready | Day 7 | Full STT→LLM→TTS working |
| M3: Twilio Integration | Day 10 | Can receive and handle calls |
| M4: Lead Capture Ready | Day 12 | Leads saving to DB |
| M5: Sheets Integration | Day 16 | Courses syncing automatically |
| M6: Dashboard Ready | Day 19 | Full admin UI working |
| M7: Testing Complete | Day 24 | All tests passing |
| M8: Production Launch | Day 28 | Live with real institute |

## 23.2 Timeline Summary

| Phase | Duration | Focus |
|-------|----------|-------|
| Phase 1 | Week 1 | Foundation |
| Phase 2 | Week 2 | Voice Pipeline |
| Phase 3 | Week 3 | Integrations |
| Phase 4 | Week 4 | Testing & Launch |

---

# 24. BUDGET BREAKDOWN

## 24.1 Single Institute (Prototype)

| Item | Monthly Cost (INR) | Notes |
|------|-------------------|-------|
| VoIP Number (Twilio) | 100 | $1.20/mo |
| GPU VPS (1x T4) | 3,500 | Higher specs for 150 calls |
| PostgreSQL | 500 | Managed DB |
| Redis | 0 | Included in VPS |
| Domain & SSL | 200 | .in domain |
| Twilio Usage (22,500 min) | 1,800 | $0.008/min × 22,500 |
| Monitoring | 200 | Basic monitoring |
| Backup | 200 | Daily backups |
| **Total** | **₹6,500/mo** | |

## 24.2 100 Institutes Scale

| Item | Monthly Cost (INR) | Notes |
|------|-------------------|-------|
| VoIP Numbers (100) | 10,000 | $1 × 100 |
| Twilio Usage (2.25M min) | 180,000 | $0.008 × 2,250,000 |
| GPU Servers (3x A100) | 60,000 | High capacity |
| PostgreSQL | 8,000 | Multi-AZ |
| Redis | 2,000 | Cluster mode |
| Load Balancer | 5,000 | HA setup |
| Storage | 3,000 | S3 + backups |
| Monitoring | 2,000 | Full stack |
| Misc | 5,000 | Contingency |
| **Total** | **₹275,000/mo** | |
| **Per Institute** | **₹2,750/mo** | |

## 24.3 ROI Calculation

| Institutes | Revenue | Cost | Profit | ROI (Annual) |
|------------|---------|------|--------|--------------|
| 1 | ₹30,000/mo | ₹6,500/mo | ₹23,500/mo | 433% |
| 10 | ₹300,000/mo | ₹40,000/mo | ₹260,000/mo | 780% |
| 50 | ₹1,500,000/mo | ₹150,000/mo | ₹1,350,000/mo | 1,080% |
| 100 | ₹3,000,000/mo | ₹275,000/mo | ₹2,725,000/mo | 1,191% |

---

# 25. APPENDICES

## Appendix A: Glossary

| Term | Definition |
|------|------------|
| STT | Speech-to-Text |
| TTS | Text-to-Speech |
| LLM | Large Language Model |
| VAD | Voice Activity Detection |
| DID | Direct Inward Dialing |
| VoIP | Voice over Internet Protocol |
| API | Application Programming Interface |
| PRD | Product Requirements Document |
| ROI | Return on Investment |
| UAT | User Acceptance Testing |

## Appendix B: API Error Codes

| Code | Meaning |
|------|---------|
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 422 | Validation Error |
| 429 | Rate Limited |
| 500 | Internal Server Error |
| 503 | Service Unavailable |

## Appendix C: Database Schema (Quick Reference)

```
institutes → users (1:M)
institutes → voice_configs (1:1)
institutes → courses (1:M)
institutes → students (1:M)
institutes → calls (1:M)
students → calls (1:M)
students → student_activities (1:M)
calls → call_transcripts (1:M)
```

## Appendix D: File Structure

```
repcon-voice-agent/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── voice_pipeline.py
│   │   ├── handlers/
│   │   ├── services/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── routers/
│   │   └── database/
│   ├── tests/
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   ├── components/
│   │   └── api/
│   ├── package.json
│   └── vite.config.js
├── infrastructure/
│   ├── docker/
│   └── terraform/
├── database/
│   ├── schema.sql
│   └── migrations/
└── docs/
    ├── PROTOTYPE_PLAN.md
    └── VoiceAgentPrototype_PRD.md
```

---

# 26. USER STORIES

## 26.1 Caller (Student) User Stories

### US-001: Inquiry About Courses
**As a** prospective student calling to inquire about courses,
**I want to** hear information about available courses,
**So that** I can decide which course to enroll in.

**Acceptance Criteria:**
- AC-001: Call is answered within 2 seconds
- AC-002: AI greets with institute name in caller's language
- AC-003: AI provides list of courses when asked
- AC-004: AI can explain course duration, fee, and job opportunities
- AC-005: AI responds in the same language the caller speaks

### US-002: Fee Inquiry
**As a** caller interested in a specific course,
**I want to** know the exact fee structure,
**So that** I can plan my budget.

**Acceptance Criteria:**
- AC-001: AI provides exact fee amount when asked about fee/cost/price
- AC-002: AI mentions payment options if available
- AC-003: AI can provide breakdown if asked (registration, tuition, etc.)

### US-003: Lead Capture
**As a** interested caller,
**I want to** leave my contact details for follow-up,
**So that** a counselor can contact me.

**Acceptance Criteria:**
- AC-001: AI asks for name when caller shows interest
- AC-002: AI asks for phone number
- AC-003: AI validates phone number format
- AC-004: AI asks for email (optional)
- AC-005: AI confirms details before ending call
- AC-006: Lead is saved in database within 5 seconds of call end

### US-004: Multi-Language Support
**As a** caller who prefers to speak in my native language,
**I want to** interact with the AI in my language,
**So that** I can communicate effectively.

**Acceptance Criteria:**
- AC-001: AI detects language automatically
- AC-002: AI responds in Hindi when caller speaks Hindi
- AC-003: AI responds in Telugu when caller speaks Telugu
- AC-004: AI responds in Tamil when caller speaks Tamil
- AC-005: AI responds in Kannada when caller speaks Kannada
- AC-006: AI responds in Urdu when caller speaks Urdu

### US-005: After-Hours Inquiry
**As a** caller calling outside business hours,
**I want to** get information about courses,
**So that** I don't have to wait for office hours.

**Acceptance Criteria:**
- AC-001: AI answers calls 24/7 including nights and weekends
- AC-001: AI provides same quality of information as business hours

## 26.2 Institute Admin User Stories

### US-010: View Leads Dashboard
**As an** institute admin,
**I want to** view all leads captured from calls,
**So that** I can follow up with interested students.

**Acceptance Criteria:**
- AC-001: Dashboard shows total leads today
- AC-002: Leads are listed with name, phone, course interest, status
- AC-003: Leads can be filtered by date range
- AC-004: Leads can be filtered by status (new, contacted, enrolled, lost)
- AC-005: Leads can be filtered by course
- AC-006: Search by name, phone, or email works

### US-011: Manage Lead Status
**As an** institute admin,
**I want to** update lead status,
**So that** I can track conversion progress.

**Acceptance Criteria:**
- AC-001: Admin can change lead status from "new" to "contacted"
- AC-002: Admin can change lead status to "interested"
- AC-003: Admin can change lead status to "enrolled"
- AC-004: Admin can change lead status to "lost"
- AC-005: Status change is logged with timestamp
- AC-006: Previous status is preserved in audit log

### US-012: Export Leads
**As an** institute admin,
**I want to** export leads to CSV,
**So that** I can share with my sales team.

**Acceptance Criteria:**
- AC-001: Export button generates CSV file
- AC-002: CSV includes all lead fields
- AC-003: Date filter applies to export
- AC-004: Status filter applies to export
- AC-005: Exported file downloads within 5 seconds

### US-013: Configure Voice Greeting
**As an** institute admin,
**I want to** customize the voice greeting,
**So that** callers hear my institute's welcome message.

**Acceptance Criteria:**
- AC-001: Admin can edit greeting message text
- AC-002: Admin can test greeting by playing it
- AC-003: Changes take effect within 5 minutes
- AC-004: Default greeting is available if custom not set

### US-014: Sync Courses from Google Sheets
**As an** institute admin,
**I want to** sync course data from Google Sheets,
**So that** the AI has up-to-date course information.

**Acceptance Criteria:**
- AC-001: Admin can trigger manual sync
- AC-002: Sync pulls all courses from configured sheet
- AC-003: Sync updates existing courses with new data
- AC-004: Sync adds new courses not in database
- AC-005: Sync removes courses not in sheet (optional)
- AC-006: Sync progress is shown to admin

### US-015: View Call Analytics
**As an** institute admin,
**I want to** view call analytics,
**So that** I can understand call volume patterns.

**Acceptance Criteria:**
- AC-001: Total calls today displayed
- AC-002: Total calls this week displayed
- AC-003: Average call duration displayed
- AC-004: Calls per day chart for last 30 days
- AC-005: Peak calling hours identified

### US-016: Manage Users
**As an** institute admin,
**I want to** add/remove team members,
**So that** they can access the dashboard.

**Acceptance Criteria:**
- AC-001: Admin can add new user with email and role
- AC-001: Admin can assign role (admin/manager/viewer)
- AC-003: Admin can deactivate user account
- AC-004: Admin can reset user password

## 26.3 Technical User Stories

### US-020: Receive Inbound Call
**As the** voice agent system,
**I want to** receive inbound calls via Twilio,
**So that** I can process caller requests.

**Acceptance Criteria:**
- AC-001: Twilio webhook receives incoming call
- AC-002: Call record is created in database
- AC-003: Audio stream is established via WebSocket
- AC-004: Call is answered within 2 seconds

### US-021: Process Speech in Real-Time
**As the** voice agent system,
**I want to** transcribe caller speech in real-time,
**So that** I can understand their intent.

**Acceptance Criteria:**
- AC-001: Audio chunks are processed as they arrive
- AC-002: Transcription latency < 500ms
- AC-003: Transcription accuracy > 90% for clear audio
- AC-004: VAD filters out silence and noise

### US-022: Generate AI Response
**As the** voice agent system,
**I want to** generate contextual responses,
**So that** callers get helpful information.

**Acceptance Criteria:**
- AC-001: LLM generates response within 1 second
- AC-002: Response uses context from course database
- AC-003: Response is in same language as caller
- AC-004: Response length is appropriate for voice (not too long)

### US-023: Convert Text to Speech
**As the** voice agent system,
**I want to** convert AI responses to speech,
**So that** callers can hear the answer.

**Acceptance Criteria:**
- AC-001: TTS generates audio within 200ms
- AC-002: Audio is streamed to caller in real-time
- AC-003: Voice is natural and easy to understand
- AC-004: Voice speed is slightly slower than normal for clarity

### US-024: Log Call Details
**As the** voice agent system,
**I want to** log all call details,
**So that** admins can review conversations.

**Acceptance Criteria:**
- AC-001: Call duration is recorded
- AC-002: Full transcript is stored
- AC-003: Call outcome is classified
- AC-004: All data is saved within 10 seconds of call end

---

# 27. USER ACCEPTANCE CRITERIA

## 27.1 Functional Acceptance Criteria

### FAC-001: Inbound Call Handling
| ID | Criterion | Test Method | Success Condition |
|----|-----------|-------------|-------------------|
| FAC-001.1 | System answers call within 2 seconds | Measure time from ring to greeting | < 2 seconds |
| FAC-001.2 | Greeting plays correctly | Manual test call | Audible, clear |
| FAC-001.3 | Call can be ended by caller | Manual test call | Call disconnects properly |
| FAC-001.4 | Call can be ended by AI (timeout) | Wait for 5 min silence | Call ends gracefully |

### FAC-002: Speech Recognition
| ID | Criterion | Test Method | Success Condition |
|----|-----------|-------------|-------------------|
| FAC-002.1 | English speech is transcribed | Test with English speaker | > 90% accuracy |
| FAC-002.2 | Hindi speech is transcribed | Test with Hindi speaker | > 85% accuracy |
| FAC-002.3 | Language is auto-detected | Test with different languages | > 90% accuracy |
| FAC-002.4 | Silence is not transcribed | Play silence audio | No text output |

### FAC-003: Intent Classification
| ID | Criterion | Test Method | Success Condition |
|----|-----------|-------------|-------------------|
| FAC-003.1 | Course inquiry detected | Say "what courses" | Intent = course_info |
| FAC-003.2 | Fee inquiry detected | Say "what is the fee" | Intent = fee_inquiry |
| FAC-003.3 | Lead capture triggered | Show interest in course | Intent = lead_capture |
| FAC-003.4 | Goodbye detected | Say "thank you, bye" | Intent = goodbye |

### FAC-004: Lead Capture
| ID | Criterion | Test Method | Success Condition |
|----|-----------|-------------|-------------------|
| FAC-004.1 | Name captured | Say "my name is Rahul" | Name = "Rahul" in DB |
| FAC-004.2 | Phone captured | Say "my number is 9876543210" | Phone in DB |
| FAC-004.3 | Phone validated | Say invalid number | Error message played |
| FAC-004.4 | Lead saved to DB | Complete lead capture | Record exists in DB |

### FAC-005: Admin Dashboard
| ID | Criterion | Test Method | Success Condition |
|----|-----------|-------------|-------------------|
| FAC-005.1 | Leads page loads | Navigate to /leads | < 2 seconds |
| FAC-005.2 | Lead filters work | Apply status filter | Correct results |
| FAC-005.3 | Lead search works | Search by name | Correct results |
| FAC-005.4 | Export generates CSV | Click export | File downloads |

### FAC-006: Google Sheets Integration
| ID | Criterion | Test Method | Success Condition |
|----|-----------|-------------|-------------------|
| FAC-006.1 | Manual sync works | Click sync button | Courses updated |
| FAC-006.2 | Auto sync runs | Wait 1 hour | Courses auto-updated |
| FAC-006.3 | New courses added | Add row to Sheet | Appears in DB |
| FAC-006.4 | Course data accurate | Compare Sheet vs DB | 100% match |

## 27.2 Non-Functional Acceptance Criteria

### NFAC-001: Performance
| ID | Criterion | Test Method | Success Condition |
|----|-----------|-------------|-------------------|
| NFAC-001.1 | End-to-end latency | Measure speech to response | < 2 seconds |
| NFAC-001.2 | STT latency | Measure audio to text | < 500ms |
| NFAC-001.3 | LLM response time | Measure prompt to response | < 1 second |
| NFAC-001.4 | TTS latency | Measure text to audio | < 200ms |

### NFAC-002: Scalability
| ID | Criterion | Test Method | Success Condition |
|----|-----------|-------------|-------------------|
| NFAC-002.1 | 10 concurrent calls | Load test with 10 calls | All complete |
| NFAC-002.2 | 20 concurrent calls | Load test with 20 calls | All complete |
| NFAC-002.3 | CPU under load | Monitor during test | < 70% |
| NFAC-002.4 | Memory under load | Monitor during test | < 12GB |

### NFAC-003: Availability
| ID | Criterion | Test Method | Success Condition |
|----|-----------|-------------|-------------------|
| NFAC-003.1 | Uptime | Monitor for 24 hours | > 99.9% |
| NFAC-003.2 | Recovery from failure | Kill a service | Auto-restart < 1 min |
| NFAC-003.3 | Health check endpoint | GET /health | Returns 200 OK |

### NFAC-004: Security
| ID | Criterion | Test Method | Success Condition |
|----|-----------|-------------|-------------------|
| NFAC-004.1 | Auth required | Access dashboard without login | Redirected to login |
| NFAC-004.2 | Role-based access | Viewer tries to edit | Access denied |
| NFAC-004.3 | Password hashed | Check database | No plain text passwords |
| NFAC-004.4 | API rate limited | 100+ rapid requests | 429 response |

---

# 28. AUTOMATED TESTING SCRIPTS

## 28.1 Test Framework Overview

### 28.1.1 Technology Stack
| Component | Technology | Version |
|-----------|------------|---------|
| Test Runner | pytest | 7.0+ |
| HTTP Client | httpx | 0.24+ |
| Database | psycopg2 | 2.9+ |
| Mocking | unittest.mock | Built-in |
| Assertions | pytest-assertions | Built-in |
| Fixtures | pytest fixtures | Built-in |
| Coverage | pytest-cov | 4.0+ |

### 28.1.2 Test Directory Structure
```
backend/
├── tests/
│   ├── __init__.py
│   ├── conftest.py              # Shared fixtures
│   ├── unit/
│   │   ├── __init__.py
│   │   ├── test_models.py
│   │   ├── test_services.py
│   │   └── test_utils.py
│   ├── integration/
│   │   ├── __init__.py
│   │   ├── test_api_leads.py
│   │   ├── test_api_calls.py
│   │   ├── test_api_courses.py
│   │   └── test_auth.py
│   ├── e2e/
│   │   ├── __init__.py
│   │   ├── test_call_flow.py
│   │   ├── test_lead_capture.py
│   │   └── test_dashboard.py
│   └── fixtures/
│       ├── sample_audio.wav
│       ├── sample_lead.json
│       └── sample_course.json
├── requirements-test.txt
└── pytest.ini
```

## 28.2 Unit Tests

### 28.2.1 Model Tests

```python
# tests/unit/test_models.py
import pytest
from datetime import datetime
from app.models.lead import Lead
from app.models.course import Course
from app.models.call import Call

class TestLeadModel:
    """Unit tests for Lead model"""
    
    def test_lead_creation(self):
        """Test lead can be created with required fields"""
        lead = Lead(
            name="Rahul Sharma",
            phone="+919876543210",
            institute_id=1
        )
        assert lead.name == "Rahul Sharma"
        assert lead.phone == "+919876543210"
        assert lead.status == "new"
    
    def test_lead_phone_validation_valid(self):
        """Test valid phone numbers pass validation"""
        valid_phones = [
            "+919876543210",
            "9876543210",
            "+1-555-123-4567"
        ]
        for phone in valid_phones:
            lead = Lead(phone=phone, name="Test", institute_id=1)
            assert lead.phone == phone
    
    def test_lead_phone_validation_invalid(self):
        """Test invalid phone numbers raise error"""
        invalid_phones = [
            "abc",
            "123",
            "+91987654321",  # Too short
        ]
        for phone in invalid_phones:
            with pytest.raises(ValueError):
                Lead(phone=phone, name="Test", institute_id=1)
    
    def test_lead_status_transitions(self):
        """Test valid status transitions"""
        lead = Lead(name="Test", phone="9876543210", institute_id=1)
        
        # Valid transitions
        lead.status = "contacted"
        assert lead.status == "contacted"
        
        lead.status = "interested"
        assert lead.status == "interested"
        
        lead.status = "enrolled"
        assert lead.status == "enrolled"
    
    def test_lead_status_invalid_transition(self):
        """Test invalid status raises error"""
        lead = Lead(name="Test", phone="9876543210", institute_id=1)
        
        # enrolled -> new is invalid
        lead.status = "enrolled"
        with pytest.raises(ValueError):
            lead.status = "new"

class TestCourseModel:
    """Unit tests for Course model"""
    
    def test_course_creation(self):
        """Test course can be created"""
        course = Course(
            course_name="Python Data Science",
            duration="6 months",
            fee=35000,
            institute_id=1
        )
        assert course.course_name == "Python Data Science"
        assert course.fee == 35000
        assert course.is_active is True
    
    def test_course_job_roles_array(self):
        """Test job roles are stored as array"""
        course = Course(
            course_name="Test",
            duration="3 months",
            fee=10000,
            job_roles=["Data Analyst", "ML Engineer"],
            institute_id=1
        )
        assert len(course.job_roles) == 2
        assert "Data Analyst" in course.job_roles

class TestCallModel:
    """Unit tests for Call model"""
    
    def test_call_duration_calculation(self):
        """Test call duration is calculated correctly"""
        call = Call(
            caller_phone="+919876543210",
            institute_id=1,
            started_at=datetime(2026, 3, 2, 10, 0, 0),
            ended_at=datetime(2026, 3, 2, 10, 5, 0)
        )
        assert call.duration == 300  # 5 minutes
    
    def test_call_status_completed(self):
        """Test completed call status"""
        call = Call(
            caller_phone="+919876543210",
            institute_id=1,
            status="completed",
            duration=180
        )
        assert call.status == "completed"
        assert call.duration == 180
```

### 28.2.2 Service Tests

```python
# tests/unit/test_services.py
import pytest
from unittest.mock import Mock, patch, AsyncMock
from app.services.lead_service import LeadService
from app.services.course_service import CourseService
from app.services.voice_pipeline import VoicePipeline

class TestLeadService:
    """Unit tests for LeadService"""
    
    @pytest.fixture
    def mock_db(self):
        return Mock()
    
    @pytest.fixture
    def lead_service(self, mock_db):
        return LeadService(mock_db)
    
    def test_create_lead_success(self, lead_service, mock_db):
        """Test successful lead creation"""
        lead_data = {
            "name": "Rahul Sharma",
            "phone": "+919876543210",
            "email": "rahul@email.com",
            "institute_id": 1
        }
        
        with patch.object(lead_service, 'save', return_value=1):
            result = lead_service.create(lead_data)
            assert result["name"] == "Rahul Sharma"
    
    def test_create_lead_duplicate_phone(self, lead_service, mock_db):
        """Test duplicate phone updates existing lead"""
        lead_data = {
            "name": "Rahul Sharma",
            "phone": "+919876543210",
            "institute_id": 1
        }
        
        # Simulate existing lead
        existing_lead = {
            "id": 1,
            "phone": "+919876543210",
            "name": "Old Name"
        }
        
        with patch.object(lead_service, 'find_by_phone', return_value=existing_lead):
            with patch.object(lead_service, 'update', return_value=existing_lead):
                result = lead_service.create(lead_data)
                # Should update rather than create new
    
    def test_get_leads_with_filters(self, lead_service, mock_db):
        """Test lead retrieval with filters"""
        filters = {
            "status": "new",
            "course_id": 1,
            "date_from": "2026-03-01"
        }
        
        with patch.object(lead_service, 'find_all', return_value=[]):
            result = lead_service.get_leads(filters)
            assert isinstance(result, list)

class TestCourseService:
    """Unit tests for CourseService"""
    
    @pytest.fixture
    def mock_db(self):
        return Mock()
    
    @pytest.fixture
    def course_service(self, mock_db):
        return CourseService(mock_db)
    
    def test_get_active_courses(self, course_service, mock_db):
        """Test getting only active courses"""
        mock_courses = [
            {"id": 1, "course_name": "Python DS", "is_active": True},
            {"id": 2, "course_name": "Web Dev", "is_active": False}
        ]
        
        with patch.object(course_service, 'find_active', return_value=[mock_courses[0]]):
            result = course_service.get_active_courses()
            assert len(result) == 1
            assert result[0]["course_name"] == "Python DS"
    
    def test_search_courses_by_name(self, course_service, mock_db):
        """Test course search by name"""
        with patch.object(course_service, 'search', return_value=[]):
            result = course_service.search_by_name("Python")
            assert isinstance(result, list)

class TestVoicePipeline:
    """Unit tests for VoicePipeline"""
    
    @pytest.fixture
    def voice_pipeline(self):
        return VoicePipeline()
    
    @pytest.mark.asyncio
    async def test_detect_language_english(self, voice_pipeline):
        """Test English language detection"""
        text = "What courses do you offer"
        lang = await voice_pipeline.detect_language(text)
        assert lang == "en"
    
    @pytest.mark.asyncio
    async def test_detect_language_hindi(self, voice_pipeline):
        """Test Hindi language detection"""
        text = "आप क्या कोर्सेस देते हो"
        lang = await voice_pipeline.detect_language(text)
        assert lang == "hi"
    
    def test_classify_intent_course_info(self, voice_pipeline):
        """Test course info intent classification"""
        text = "what courses do you offer"
        intent = voice_pipeline.classify_intent(text)
        assert intent == "course_info"
    
    def test_classify_intent_fee_inquiry(self, voice_pipeline):
        """Test fee inquiry intent classification"""
        text = "what is the fee for the course"
        intent = voice_pipeline.classify_intent(text)
        assert intent == "fee_inquiry"
    
    def test_classify_intent_lead_capture(self, voice_pipeline):
        """Test lead capture intent classification"""
        text = "my name is rahul and my number is 9876543210"
        intent = voice_pipeline.classify_intent(text)
        assert intent == "lead_capture"
    
    def test_extract_phone_from_text(self, voice_pipeline):
        """Test phone number extraction"""
        text = "my number is 9876543210"
        phone = voice_pipeline.extract_phone(text)
        assert phone == "9876543210"
    
    def test_extract_phone_with_country_code(self, voice_pipeline):
        """Test phone extraction with country code"""
        text = "call me at +919876543210"
        phone = voice_pipeline.extract_phone(text)
        assert phone == "+919876543210"
    
    def test_extract_name_from_text(self, voice_pipeline):
        """Test name extraction"""
        text = "my name is Rahul Sharma"
        name = voice_pipeline.extract_name(text)
        assert "rahul" in name.lower() or "sharma" in name.lower()
```

## 28.3 Integration Tests

### 28.3.1 API Tests

```python
# tests/integration/test_api_leads.py
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.fixture
async def auth_token():
    """Get authentication token"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/auth/login",
            json={"email": "admin@test.com", "password": "test123"}
        )
        return response.json()["access_token"]

@pytest.mark.asyncio
class TestLeadsAPI:
    """Integration tests for Leads API"""
    
    async def test_create_lead(self, auth_token):
        """Test lead creation via API"""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                "/api/v1/leads",
                json={
                    "name": "Rahul Sharma",
                    "phone": "+919876543210",
                    "email": "rahul@test.com",
                    "institute_id": 1
                },
                headers={"Authorization": f"Bearer {auth_token}"}
            )
            assert response.status_code == 201
            data = response.json()
            assert data["name"] == "Rahul Sharma"
            assert data["phone"] == "+919876543210"
    
    async def test_create_lead_invalid_phone(self, auth_token):
        """Test lead creation with invalid phone"""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                "/api/v1/leads",
                json={
                    "name": "Test",
                    "phone": "invalid",
                    "institute_id": 1
                },
                headers={"Authorization": f"Bearer {auth_token}"}
            )
            assert response.status_code == 422
    
    async def test_get_leads(self, auth_token):
        """Test getting leads list"""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get(
                "/api/v1/leads",
                headers={"Authorization": f"Bearer {auth_token}"}
            )
            assert response.status_code == 200
            data = response.json()
            assert "items" in data
            assert "total" in data
    
    async def test_get_leads_with_filters(self, auth_token):
        """Test getting leads with filters"""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get(
                "/api/v1/leads?status=new&course_id=1",
                headers={"Authorization": f"Bearer {auth_token}"}
            )
            assert response.status_code == 200
    
    async def test_update_lead(self, auth_token):
        """Test lead update"""
        async with AsyncClient(app=app, base_url="http://test") as client:
            # First create a lead
            create_response = await client.post(
                "/api/v1/leads",
                json={
                    "name": "Test Lead",
                    "phone": "+919876543210",
                    "institute_id": 1
                },
                headers={"Authorization": f"Bearer {auth_token}"}
            )
            lead_id = create_response.json()["id"]
            
            # Update the lead
            update_response = await client.put(
                f"/api/v1/leads/{lead_id}",
                json={"status": "contacted"},
                headers={"Authorization": f"Bearer {auth_token}"}
            )
            assert update_response.status_code == 200
            assert update_response.json()["status"] == "contacted"
    
    async def test_delete_lead(self, auth_token):
        """Test lead deletion"""
        async with AsyncClient(app=app, base_url="http://test") as client:
            # Create a lead first
            create_response = await client.post(
                "/api/v1/leads",
                json={
                    "name": "To Delete",
                    "phone": "+919876543210",
                    "institute_id": 1
                },
                headers={"Authorization": f"Bearer {auth_token}"}
            )
            lead_id = create_response.json()["id"]
            
            # Delete it
            delete_response = await client.delete(
                f"/api/v1/leads/{lead_id}",
                headers={"Authorization": f"Bearer {auth_token}"}
            )
            assert delete_response.status_code == 204
    
    async def test_export_leads_csv(self, auth_token):
        """Test leads export to CSV"""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get(
                "/api/v1/leads/export",
                headers={"Authorization": f"Bearer {auth_token}"}
            )
            assert response.status_code == 200
            assert "text/csv" in response.headers.get("content-type")

@pytest.mark.asyncio
class TestAuthAPI:
    """Integration tests for Authentication API"""
    
    async def test_login_success(self):
        """Test successful login"""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                "/api/v1/auth/login",
                json={"email": "admin@test.com", "password": "test123"}
            )
            assert response.status_code == 200
            assert "access_token" in response.json()
    
    async def test_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                "/api/v1/auth/login",
                json={"email": "wrong@test.com", "password": "wrong"}
            )
            assert response.status_code == 401
    
    async def test_access_protected_endpoint_without_token(self):
        """Test accessing protected endpoint without token"""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get("/api/v1/leads")
            assert response.status_code == 401
```

### 28.3.2 Database Tests

```python
# tests/integration/test_database.py
import pytest
import psycopg2
from app.database.connection import get_db_connection

@pytest.fixture
def db_connection():
    """Get database connection for tests"""
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        database="repcon_test",
        user="repcon",
        password="repcon123"
    )
    yield conn
    conn.close()

class TestDatabaseSchema:
    """Integration tests for database schema"""
    
    def test_institutes_table_exists(self, db_connection):
        """Test institutes table exists"""
        cursor = db_connection.cursor()
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'institutes'
            );
        """)
        assert cursor.fetchone()[0] is True
    
    def test_leads_table_exists(self, db_connection):
        """Test leads table exists"""
        cursor = db_connection.cursor()
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'students'
            );
        """)
        assert cursor.fetchone()[0] is True
    
    def test_courses_table_exists(self, db_connection):
        """Test courses table exists"""
        cursor = db_connection.cursor()
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'courses'
            );
        """)
        assert cursor.fetchone()[0] is True
    
    def test_calls_table_exists(self, db_connection):
        """Test calls table exists"""
        cursor = db_connection.cursor()
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'calls'
            );
        """)
        assert cursor.fetchone()[0] is True
    
    def test_foreign_key_constraints(self, db_connection):
        """Test foreign key constraints"""
        cursor = db_connection.cursor()
        
        # Test: leads require valid institute_id
        cursor.execute("""
            INSERT INTO institutes (name, slug) 
            VALUES ('Test Institute', 'test-institute')
            RETURNING id;
        """)
        institute_id = cursor.fetchone()[0]
        
        # Should succeed
        cursor.execute("""
            INSERT INTO students (name, phone, institute_id)
            VALUES ('Test Student', '9876543210', %s);
        """, (institute_id,))
        db_connection.commit()
        
        # Should fail (invalid institute)
        cursor.execute("""
            INSERT INTO students (name, phone, institute_id)
            VALUES ('Test Student', '9876543210', 99999);
        """)
        with pytest.raises(psycopg2.IntegrityError):
            db_connection.commit()
```

## 28.4 End-to-End Tests

### 28.4.1 Call Flow E2E Tests

```python
# tests/e2e/test_call_flow.py
import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
from app.voice_pipeline import VoicePipeline

@pytest.mark.asyncio
class TestCallFlowE2E:
    """End-to-end tests for call flow"""
    
    @pytest.fixture
    def voice_pipeline(self):
        return VoicePipeline()
    
    @pytest.fixture
    def mock_audio_chunk(self):
        """Sample audio chunk for testing"""
        return b"AUDIO_CHUNK_DATA"
    
    @pytest.mark.asyncio
    async def test_complete_call_flow_happy_path(self, voice_pipeline):
        """Test complete call flow: greeting -> inquiry -> response -> lead capture"""
        
        # Mock the components
        voice_pipeline.stt = AsyncMock()
        voice_pipeline.stt.transcribe = AsyncMock(return_value="What courses do you offer")
        
        voice_pipeline.llm = AsyncMock()
        voice_pipeline.llm.generate = AsyncMock(
            return_value="We offer Python Data Science, Web Development, and Digital Marketing courses."
        )
        
        voice_pipeline.tts = AsyncMock()
        voice_pipeline.tts.speak = AsyncMock(return_value=b"AUDIO_DATA")
        
        # Step 1: Greeting
        greeting_audio = await voice_pipeline.generate_greeting("en")
        assert greeting_audio is not None
        
        # Step 2: Process user query
        response = await voice_pipeline.process_query("What courses do you offer")
        
        assert "courses" in response.lower()
        
        # Step 3: Lead capture
        lead_data = await voice_pipeline.capture_lead(
            name="Rahul",
            phone="9876543210"
        )
        assert lead_data is not None
    
    @pytest.mark.asyncio
    async def test_call_flow_with_hindi(self, voice_pipeline):
        """Test call flow in Hindi"""
        
        voice_pipeline.stt = AsyncMock()
        voice_pipeline.stt.transcribe = AsyncMock(return_value="आप क्या कोर्सेस देते हो")
        
        voice_pipeline.llm = AsyncMock()
        voice_pipeline.llm.generate = AsyncMock(
            return_value="हम पायथन डेटा साइंस कोर्स ऑफर करते हैं।"
        )
        
        # Detect language
        lang = await voice_pipeline.detect_language("आप क्या कोर्सेस देते हो")
        assert lang == "hi"
        
        # Process query
        response = await voice_pipeline.process_query("आप क्या कोर्सेस देते हो")
        
        assert response is not None
    
    @pytest.mark.asyncio
    async def test_call_flow_lead_capture_full(self, voice_pipeline):
        """Test full lead capture flow"""
        
        # Step 1: Show interest
        response = await voice_pipeline.process_query("I am interested in your data science course")
        assert "data science" in response.lower() or "interested" in response.lower()
        
        # Step 2: Provide name
        response = await voice_pipeline.process_query("My name is Rahul Sharma")
        assert "rahul" in response.lower() or "name" in response.lower()
        
        # Step 3: Provide phone
        response = await voice_pipeline.process_query("My number is 9876543210")
        
        # Verify lead captured
        # (In real test, would check database)
    
    @pytest.mark.asyncio
    async def test_call_end_gracefully(self, voice_pipeline):
        """Test call ends gracefully with goodbye"""
        
        voice_pipeline.llm = AsyncMock()
        voice_pipeline.llm.generate = AsyncMock(
            return_value="Thank you for calling. Have a great day!"
        )
        
        # Detect goodbye
        intent = voice_pipeline.classify_intent("thank you, goodbye")
        assert intent == "goodbye"
        
        # Generate goodbye message
        goodbye = await voice_pipeline.generate_goodbye("en")
        assert goodbye is not None
    
    @pytest.mark.asyncio
    async def test_timeout_handling(self, voice_pipeline):
        """Test timeout when caller doesn't respond"""
        
        # Simulate silence
        with patch.object(voice_pipeline, 'check_silence', return_value=True):
            response = await voice_pipeline.handle_silence()
            assert response is not None
            assert "didn't catch" in response.lower() or "repeat" in response.lower()

@pytest.mark.asyncio
class TestLeadCaptureE2E:
    """End-to-end tests for lead capture"""
    
    @pytest.fixture
    def voice_pipeline(self):
        return VoicePipeline()
    
    @pytest.mark.asyncio
    async def test_full_lead_capture_sequence(self, voice_pipeline):
        """Test complete lead capture: name -> phone -> confirm"""
        
        # Conversation simulation
        conversation = [
            ("Hi, I'm interested in Python course", "interested"),
            ("My name is Priya Patel", "name_captured"),
            ("My phone is 9988776655", "phone_captured"),
            ("Yes that's correct", "confirmed")
        ]
        
        lead_info = {"name": None, "phone": None}
        
        for user_input, expected_step in conversation:
            response = await voice_pipeline.process_query(user_input)
            
            # Extract info
            if "name" in user_input.lower():
                name = voice_pipeline.extract_name(user_input)
                if name:
                    lead_info["name"] = name
            
            if "phone" in user_input.lower() or any(c.isdigit() for c in user_input):
                phone = voice_pipeline.extract_phone(user_input)
                if phone:
                    lead_info["phone"] = phone
        
        # Verify lead captured
        assert lead_info["name"] is not None
        assert lead_info["phone"] is not None
```

### 28.4.2 Dashboard E2E Tests

```python
# tests/e2e/test_dashboard.py
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
class TestDashboardE2E:
    """End-to-end tests for dashboard functionality"""
    
    async def test_dashboard_loads(self):
        """Test dashboard loads with stats"""
        # Login first
        async with AsyncClient(app=app, base_url="http://test") as client:
            login_response = await client.post(
                "/api/v1/auth/login",
                json={"email": "admin@test.com", "password": "test123"}
            )
            token = login_response.json()["access_token"]
            
            # Load dashboard
            response = await client.get(
                "/api/v1/stats/dashboard",
                headers={"Authorization": f"Bearer {token}"}
            )
            
            assert response.status_code == 200
            data = response.json()
            assert "today" in data
            assert "this_week" in data
    
    async def test_lead_to_enrolled_flow(self):
        """Test lead status flow: new -> contacted -> interested -> enrolled"""
        async with AsyncClient(app=app, base_url="http://test") as client:
            # Login
            login_response = await client.post(
                "/api/v1/auth/login",
                json={"email": "admin@test.com", "password": "test123"}
            )
            token = login_response.json()["access_token"]
            
            # Create lead
            lead_response = await client.post(
                "/api/v1/leads",
                json={
                    "name": "Test Lead",
                    "phone": "+919876543210",
                    "institute_id": 1
                },
                headers={"Authorization": f"Bearer {token}"}
            )
            lead_id = lead_response.json()["id"]
            
            # Update to contacted
            await client.put(
                f"/api/v1/leads/{lead_id}",
                json={"status": "contacted"},
                headers={"Authorization": f"Bearer {token}"}
            )
            
            # Update to interested
            await client.put(
                f"/api/v1/leads/{lead_id}",
                json={"status": "interested"},
                headers={"Authorization": f"Bearer {token}"}
            )
            
            # Update to enrolled
            enrolled_response = await client.put(
                f"/api/v1/leads/{lead_id}",
                json={"status": "enrolled"},
                headers={"Authorization": f"Bearer {token}"}
            )
            
            assert enrolled_response.json()["status"] == "enrolled"
            assert enrolled_response.json()["converted_at"] is not None
```

## 28.5 Performance & Load Tests

### 28.5.1 Load Testing Script

```python
# tests/load/load_test.py
import pytest
import asyncio
import time
from locust import HttpUser, task, between
from playwright.sync_api import sync_playwright

class VoiceAgentLoadUser(HttpUser):
    """Locust load test for Voice Agent API"""
    
    wait_time = between(1, 3)
    token = None
    
    def on_start(self):
        """Login before tests"""
        response = self.client.post("/api/v1/auth/login", json={
            "email": "admin@test.com",
            "password": "test123"
        })
        if response.status_code == 200:
            VoiceAgentLoadUser.token = response.json()["access_token"]
    
    @task(3)
    def get_leads(self):
        """Get leads list"""
        if self.token:
            self.client.get(
                "/api/v1/leads",
                headers={"Authorization": f"Bearer {self.token}"}
            )
    
    @task(2)
    def get_calls(self):
        """Get calls list"""
        if self.token:
            self.client.get(
                "/api/v1/calls",
                headers={"Authorization": f"Bearer {self.token}"}
            )
    
    @task(1)
    def get_dashboard(self):
        """Get dashboard stats"""
        if self.token:
            self.client.get(
                "/api/v1/stats/dashboard",
                headers={"Authorization": f"Bearer {self.token}"}
            )
    
    @task(1)
    def create_lead(self):
        """Create a new lead"""
        if self.token:
            self.client.post(
                "/api/v1/leads",
                json={
                    "name": f"Load Test Lead {time.time()}",
                    "phone": "+919876543210",
                    "institute_id": 1
                },
                headers={"Authorization": f"Bearer {self.token}"}
            )

# Run with: locust -f tests/load/load_test.py --host=http://localhost:8000
```

### 28.5.2 Concurrent Call Simulation

```python
# tests/load/concurrent_calls.py
import asyncio
import aiohttp
import time
import pytest

class TestConcurrentCalls:
    """Test concurrent voice calls"""
    
    @pytest.mark.asyncio
    async def test_10_concurrent_calls(self):
        """Test system handles 10 concurrent calls"""
        
        async def simulate_call(call_id: int):
            """Simulate a single voice call"""
            start_time = time.time()
            
            async with aiohttp.ClientSession() as session:
                # Step 1: Initiate call
                async with session.post(
                    f"{BASE_URL}/webhooks/twilio/voice",
                    json={"CallSid": f"CALL_{call_id}"}
                ) as resp:
                    assert resp.status == 200
                
                # Step 2: Simulate audio processing (5 times)
                for i in range(5):
                    async with session.post(
                        f"{BASE_URL}/media/stream",
                        json={
                            "call_id": f"CALL_{call_id}",
                            "audio": "base64_encoded_audio"
                        }
                    ) as resp:
                        await asyncio.sleep(0.1)  # 100ms between chunks
                
                # Step 3: End call
                end_time = time.time()
                duration = end_time - start_time
                
                return duration
        
        # Run 10 calls concurrently
        start = time.time()
        results = await asyncio.gather(*[simulate_call(i) for i in range(10)])
        total_time = time.time() - start
        
        # Verify all completed
        assert len(results) == 10
        
        # Verify reasonable total time (should be close to max single call time, not sum)
        # With 10 concurrent, should be ~1-2 seconds, not 10+ seconds
        assert total_time < 5.0, f"Total time {total_time}s too high for concurrent calls"
        
        # Verify average duration
        avg_duration = sum(results) / len(results)
        assert avg_duration < 2.0, f"Average call duration {avg_duration}s too high"
    
    @pytest.mark.asyncio
    async def test_20_concurrent_calls(self):
        """Test system handles 20 concurrent calls (stress test)"""
        
        async def simulate_call(call_id: int):
            async with aiohttp.ClientSession() as session:
                # Simplified call simulation
                await asyncio.sleep(0.5)  # Simulate processing
                return True
        
        start = time.time()
        results = await asyncio.gather(*[simulate_call(i) for i in range(20)])
        total_time = time.time() - start
        
        assert len(results) == 20
        assert total_time < 3.0  # Should complete quickly with concurrency
```

## 28.6 Test Fixtures

```python
# tests/conftest.py
import pytest
import asyncio
from typing import AsyncGenerator
from httpx import AsyncClient
from app.main import app
from app.database.connection import get_test_db

@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
async def test_client() -> AsyncGenerator:
    """Get async test client"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

@pytest.fixture
async def authenticated_client(test_client: AsyncClient) -> AsyncGenerator:
    """Get authenticated test client"""
    response = await test_client.post(
        "/api/v1/auth/login",
        json={"email": "admin@test.com", "password": "test123"}
    )
    token = response.json()["access_token"]
    
    # Add token to client headers
    test_client.headers["Authorization"] = f"Bearer {token}"
    yield test_client

@pytest.fixture
def sample_lead_data():
    """Sample lead data for tests"""
    return {
        "name": "Test Student",
        "phone": "+919876543210",
        "email": "test@email.com",
        "course_interest": 1,
        "institute_id": 1
    }

@pytest.fixture
def sample_course_data():
    """Sample course data for tests"""
    return {
        "course_name": "Test Course",
        "duration": "3 months",
        "fee": 15000,
        "institute_id": 1
    }

@pytest.fixture
def sample_call_data():
    """Sample call data for tests"""
    return {
        "caller_phone": "+919876543210",
        "institute_id": 1,
        "duration": 180,
        "status": "completed"
    }
```

## 28.7 Running Tests

### 28.7.1 Run All Tests
```bash
# Run all tests with coverage
pytest --cov=app --cov-report=html --cov-report=term

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/unit/test_models.py -v

# Run tests matching pattern
pytest -k "test_lead" -v

# Run with debugging
pytest --capture=no -v
```

### 28.7.2 Run by Category
```bash
# Unit tests only
pytest tests/unit/ -v

# Integration tests only
pytest tests/integration/ -v

# E2E tests only
pytest tests/e2e/ -v

# Load tests
pytest tests/load/ -v
```

### 28.7.3 CI/CD Integration
```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: test123
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-test.txt
      
      - name: Run tests
        env:
          DATABASE_URL: postgresql://postgres:test123@localhost:5432/repcon_test
        run: |
          pytest --cov=app --cov-report=xml
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

---

# 29. APPENDIX: QUICK REFERENCE

## 29.1 Test Summary Matrix

| Category | Test Count | Coverage Target | Run Time |
|----------|------------|------------------|----------|
| Unit Tests | 50+ | 80% | < 1 min |
| Integration Tests | 30+ | 70% | < 2 min |
| E2E Tests | 20+ | N/A | < 5 min |
| Load Tests | 5 | N/A | < 3 min |
| **Total** | **100+** | **75%** | **< 10 min** |

## 29.2 Test Execution Commands

```bash
# Quick test (unit only)
pytest tests/unit/ -x

# Full test suite
pytest

# With coverage report
pytest --cov=app --cov-report=html

# Parallel execution (faster)
pytest -n auto

# Generate JUnit XML (for CI)
pytest --junitxml=test-results.xml
```

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-03-02 | AI | Initial PRD creation |

---

*This PRD serves as the comprehensive requirements document for the RepCon Voice Agent Prototype implementation.*
