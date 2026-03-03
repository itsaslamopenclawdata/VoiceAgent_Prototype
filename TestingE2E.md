# RepCon Voice Agent - End-to-End Testing Guide

## Overview

This document provides comprehensive end-to-end testing procedures for the RepCon Voice Agent system.

**System Architecture:**
- **Frontend**: React + Vite (Port 3000)
- **Backend**: FastAPI (Port 8000)
- **Database**: PostgreSQL 15 (Port 5432)
- **Cache**: Redis 7 (Port 6379)
- **STT**: faster-whisper (local)
- **TTS**: Kokoro (local)
- **LLM**: Ollama (localhost:11434)

---

## Prerequisites

### 1. Docker Services Must Be Running

```bash
cd /home/itsaslamautomations/.openclaw/workspace/VoiceAgent_Prototype
docker-compose up -d
```

### 2. Verify Services Are Healthy

```bash
# Check container status
docker ps

# Expected running containers:
# - repcon_db (postgres:15-alpine)
# - repcon_redis (redis:7-alpine)
# - repcon_backend
# - repcon_frontend
```

### 3. Service Health Checks

```bash
# PostgreSQL
docker exec repcon_db pg_isready -U repcon

# Redis
docker exec repcon_redis redis-cli ping
# Expected: PONG

# Backend API
curl http://localhost:8000/health
# Expected: {"status":"healthy","service":"RepCon Voice Agent"}

# Frontend
curl http://localhost:3000
# Expected: HTML response
```

---

## Test Suite

### Phase 1: Infrastructure Tests

#### Test 1.1: Database Connectivity

**Purpose**: Verify PostgreSQL is accessible and initialized

**Steps**:
1. Check PostgreSQL container:
   ```bash
   docker exec repcon_db psql -U repcon -d repcon -c "\dt"
   ```
2. Expected output: Tables list (institute, student, call, course, etc.)

**Verification**:
- [ ] PostgreSQL container running
- [ ] Database `repcon` exists
- [ ] Tables created (institute, student, call, course)

---

#### Test 1.2: Redis Connectivity

**Purpose**: Verify Redis is accessible

**Steps**:
1. Test Redis connection:
   ```bash
   docker exec repcon_redis redis-cli set test_key "hello"
   docker exec repcon_redis redis-cli get test_key
   ```
2. Expected: `hello`

**Verification**:
- [ ] Redis container running
- [ ] Can read/write keys

---

#### Test 1.3: Backend API Health

**Purpose**: Verify FastAPI is running

**Steps**:
1. Test health endpoint:
   ```bash
   curl http://localhost:8000/health
   curl http://localhost:8000/ready
   curl http://localhost:8000/
   ```
2. Expected responses:
   - `/health`: `{"status":"healthy","service":"RepCon Voice Agent"}`
   - `/ready`: `{"status":"ready","version":"1.0.0"}`
   - `/`: Service info with docs link

**Verification**:
- [ ] Backend responding on port 8000
- [ ] All health endpoints return 200

---

#### Test 1.4: Frontend Health

**Purpose**: Verify React frontend is running

**Steps**:
1. Test frontend:
   ```bash
   curl -I http://localhost:3000
   ```
2. Expected: HTTP 200 with HTML content

**Verification**:
- [ ] Frontend responding on port 3000
- [ ] Static assets loading

---

### Phase 2: Authentication Tests

#### Test 2.1: User Registration

**Purpose**: Test user can register

**Steps**:
1. Send POST request:
   ```bash
   curl -X POST http://localhost:8000/api/v1/auth/register \
     -H "Content-Type: application/json" \
     -d '{
       "email": "test@example.com",
       "password": "testpass123",
       "full_name": "Test User",
       "institute_name": "Test Institute"
     }'
   ```
2. Expected: JWT token and user data

**Verification**:
- [ ] Registration successful
- [ ] JWT token returned
- [ ] User in database

---

#### Test 2.2: User Login

**Purpose**: Test user can login

**Steps**:
1. Send POST request:
   ```bash
   curl -X POST http://localhost:8000/api/v1/auth/login \
     -H "Content-Type: application/json" \
     -d '{
       "email": "test@example.com",
       "password": "testpass123"
     }'
   ```
2. Expected: JWT token

**Verification**:
- [ ] Login successful
- [ ] JWT token returned

---

### Phase 3: Course Management Tests

#### Test 3.1: Create Course

**Purpose**: Test course creation

**Steps**:
1. Get JWT token (from login)
2. Create course:
   ```bash
   curl -X POST http://localhost:8000/api/v1/courses/ \
     -H "Authorization: Bearer <JWT_TOKEN>" \
     -H "Content-Type: application/json" \
     -d '{
       "course_name": "Python Data Science",
       "description": "Complete Python and Data Science course",
       "fee": 25000,
       "duration_months": 6,
       "duration_hours": 120,
       "is_active": true
     }'
   ```
2. Expected: Course data with ID

**Verification**:
- [ ] Course created successfully
- [ ] Course in database

---

#### Test 3.2: List Courses

**Purpose**: Test course listing

**Steps**:
1. List courses:
   ```bash
   curl -X GET "http://localhost:8000/api/v1/courses/?institute_id=1" \
     -H "Authorization: Bearer <JWT_TOKEN>"
   ```
2. Expected: List of courses

**Verification**:
- [ ] Courses returned
- [ ] Pagination works

---

#### Test 3.3: Update Course

**Purpose**: Test course update

**Steps**:
1. Update course:
   ```bash
   curl -X PUT http://localhost:8000/api/v1/courses/1 \
     -H "Authorization: Bearer <JWT_TOKEN>" \
     -H "Content-Type: application/json" \
     -d '{
       "fee": 30000
     }'
   ```
2. Expected: Updated course data

---

#### Test 3.4: Delete Course

**Purpose**: Test course deletion

**Steps**:
1. Delete course:
   ```bash
   curl -X DELETE http://localhost:8000/api/v1/courses/1 \
     -H "Authorization: Bearer <JWT_TOKEN>"
   ```
2. Expected: Success message

---

### Phase 4: Lead Management Tests

#### Test 4.1: Create Lead

**Purpose**: Test lead creation via API

**Steps**:
1. Create lead:
   ```bash
   curl -X POST "http://localhost:8000/api/v1/leads/?institute_id=1&name=John Doe&phone=+919999999999&email=john@example.com" \
     -H "Authorization: Bearer <JWT_TOKEN>"
   ```
2. Expected: Lead ID returned

**Verification**:
- [ ] Lead created in database

---

#### Test 4.2: List Leads

**Purpose**: Test lead listing

**Steps**:
1. List leads:
   ```bash
   curl -X GET "http://localhost:8000/api/v1/leads/?institute_id=1" \
     -H "Authorization: Bearer <JWT_TOKEN>"
   ```
2. Expected: List of leads with pagination

**Verification**:
- [ ] Leads returned
- [ ] Filters work

---

#### Test 4.3: Update Lead Status

**Purpose**: Test lead status update

**Steps**:
1. Update lead:
   ```bash
   curl -X PUT http://localhost:8000/api/v1/leads/1 \
     -H "Authorization: Bearer <JWT_TOKEN>" \
     -H "Content-Type: application/json" \
     -d '{
       "status": "contacted",
       "priority": "high"
     }'
   ```

---

#### Test 4.4: Export Leads to CSV

**Purpose**: Test CSV export

**Steps**:
1. Export:
   ```bash
   curl -X GET "http://localhost:8000/api/v1/leads/export/csv?institute_id=1" \
     -H "Authorization: Bearer <JWT_TOKEN>"
   ```
2. Expected: CSV data

---

### Phase 5: Call Management Tests

#### Test 5.1: List Calls

**Purpose**: Test call listing

**Steps**:
1. List calls:
   ```bash
   curl -X GET "http://localhost:8000/api/v1/calls/?institute_id=1" \
     -H "Authorization: Bearer <JWT_TOKEN>"
   ```
2. Expected: List of calls

---

#### Test 5.2: Get Call Details

**Purpose**: Test call detail retrieval

**Steps**:
1. Get call:
   ```bash
   curl -X GET http://localhost:8000/api/v1/calls/1 \
     -H "Authorization: Bearer <JWT_TOKEN>"
   ```
2. Expected: Call details with transcript

---

#### Test 5.3: Get Call Transcript

**Purpose**: Test transcript retrieval

**Steps**:
1. Get transcript:
   ```bash
   curl -X GET http://localhost:8000/api/v1/calls/1/transcript \
     -H "Authorization: Bearer <JWT_TOKEN>"
   ```
2. Expected: Transcript and language

---

### Phase 6: Voice Pipeline Tests (Core)

#### Test 6.1: STT Service - Transcription

**Purpose**: Test Speech-to-Text functionality

**Steps**:
1. Prepare test audio file (WAV format, 16-bit, mono)
2. Test transcription (requires actual audio):
   ```python
   import requests
   
   with open('test_audio.wav', 'rb') as f:
       response = requests.post(
           'http://localhost:8000/api/v1/voice/transcribe',
           files={'audio': f},
           headers={'Authorization': 'Bearer <JWT>'}
       )
   print(response.json())
   ```
3. Expected: Transcribed text

**Verification**:
- [ ] Audio processed
- [ ] Text returned
- [ ] Language detected

---

#### Test 6.2: TTS Service - Synthesis

**Purpose**: Test Text-to-Speech functionality

**Steps**:
1. Test synthesis:
   ```bash
   curl -X POST http://localhost:8000/api/v1/voice/synthesize \
     -H "Authorization: Bearer <JWT>" \
     -H "Content-Type: application/json" \
     -d '{
       "text": "Hello! Welcome to TechVision Academy.",
       "voice_id": "af_sarah",
       "language": "en"
     }'
   ```
2. Expected: Base64 encoded audio

**Verification**:
- [ ] Audio generated
- [ ] Correct voice
- [ ] Base64 returned

---

#### Test 6.3: LLM Service - Response Generation

**Purpose**: Test LLM integration

**Steps**:
1. Test generation:
   ```bash
   curl -X POST http://localhost:8000/api/v1/voice/chat \
     -H "Authorization: Bearer <JWT>" \
     -H "Content-Type: application/json" \
     -d '{
       "message": "What courses do you offer?",
       "language": "en",
       "context": {
         "courses": [
           {"course_name": "Python", "fee": 25000, "duration": "6 months"}
         ]
       }
     }'
   ```
2. Expected: AI response text

**Verification**:
- [ ] Ollama connected
- [ ] Response generated
- [ ] Context used

---

#### Test 6.4: Full Voice Pipeline

**Purpose**: Test complete voice agent flow

**Steps**:
1. Test full pipeline:
   ```bash
   curl -X POST http://localhost:8000/api/v1/voice/process \
     -H "Authorization: Bearer <JWT>" \
     -H "Content-Type": multipart/form-data" \
     -F "audio=@test_audio.wav" \
     -F "institute_id=1"
   ```
2. Expected: Response with audio, text, and intent

**Verification**:
- [ ] STT → LLM → TTS flow works
- [ ] Intent classified correctly
- [ ] Lead captured if provided

---

### Phase 7: Multi-Language Tests

#### Test 7.1: Hindi Voice Pipeline

**Purpose**: Test Hindi language support

**Steps**:
1. Test with Hindi audio or text:
   ```bash
   curl -X POST http://localhost:8000/api/v1/voice/chat \
     -H "Authorization: Bearer <JWT>" \
     -H "Content-Type: application/json" \
     -d '{
       "message": "आप कोनसे कोर्सेस ऑफर करते हो?",
       "language": "hi"
     }'
   ```

**Supported Languages**:
- English (en)
- Hindi (hi)
- Telugu (te)
- Tamil (ta)
- Urdu (ur)
- Kannada (kn)

---

#### Test 7.2: Voice Selection by Language

**Purpose**: Verify correct voice for each language

**Steps**:
1. Test each language:
   ```bash
   # Hindi
   curl -X POST http://localhost:8000/api/v1/voice/synthesize \
     -H "Authorization: Bearer <JWT>" \
     -d '{"text": "नमस्ते", "language": "hi"}'
   
   # Telugu
   curl -X POST http://localhost:8000/api/v1/voice/synthesize \
     -H "Authorization: Bearer <JWT>" \
     -d '{"text": " నమస్కారం", "language": "te"}'
   ```

---

### Phase 8: Settings & Configuration Tests

#### Test 8.1: Get Institute Settings

**Purpose**: Test settings retrieval

**Steps**:
1. Get settings:
   ```bash
   curl -X GET http://localhost:8000/api/v1/settings/ \
     -H "Authorization: Bearer <JWT>" \
     -G -d "institute_id=1"
   ```

---

#### Test 8.2: Update Institute Settings

**Purpose**: Test settings update

**Steps**:
1. Update settings:
   ```bash
   curl -X PUT http://localhost:8000/api/v1/settings/ \
     -H "Authorization: Bearer <JWT>" \
     -H "Content-Type: application/json" \
     -d '{
       "institute_id": 1,
       "voice_enabled": true,
       "language_preference": "en"
     }'
   ```

---

### Phase 9: Statistics & Reporting Tests

#### Test 9.1: Get Dashboard Stats

**Purpose**: Test statistics retrieval

**Steps**:
1. Get stats:
   ```bash
   curl -X GET http://localhost:8000/api/v1/stats/dashboard?institute_id=1 \
     -H "Authorization: Bearer <JWT>"
   ```
2. Expected: Total calls, leads, conversion rate

---

#### Test 9.2: Get Call Analytics

**Purpose**: Test call analytics

**Steps**:
1. Get analytics:
   ```bash
   curl -X GET http://localhost:8000/api/v1/stats/calls?institute_id=1&period=7d \
     -H "Authorization: Bearer <JWT>"
   ```

---

### Phase 10: Webhook Tests

#### Test 10.1: Webhook Configuration

**Purpose**: Test webhook setup

**Steps**:
1. Configure webhook:
   ```bash
   curl -X POST http://localhost:8000/api/v1/webhooks/ \
     -H "Authorization: Bearer <JWT>" \
     -H "Content-Type: application/json" \
     -d '{
       "institute_id": 1,
       "url": "https://example.com/webhook",
       "events": ["call_completed", "lead_created"]
     }'
   ```

---

## Test Data

### Sample Course Data

```json
{
  "course_name": "Python Data Science",
  "description": "Complete Data Science with Python",
  "fee": 25000,
  "duration_months": 6,
  "duration_hours": 120,
  "is_active": true
}
```

### Sample Lead Data

```json
{
  "name": "John Doe",
  "phone": "+919999999999",
  "email": "john@example.com",
  "course_interest": 1,
  "source": "voice_agent"
}
```

### Sample Audio Test

Create a test WAV file:
```bash
# Generate 1 second of tone
ffmpeg -f lavfi -i "sine=frequency=440:duration=1" -ar 16000 -ac 1 test_tone.wav
```

---

## Expected Results Summary

| Phase | Test | Expected Outcome |
|-------|------|------------------|
| 1 | Infrastructure | All 4 services healthy |
| 2 | Auth | Registration & login work |
| 3 | Courses | CRUD operations work |
| 4 | Leads | CRUD + export work |
| 5 | Calls | List & transcript work |
| 6 | Voice Pipeline | STT→LLM→TTS works |
| 7 | Languages | 6 languages supported |
| 8 | Settings | Configurable |
| 9 | Stats | Analytics returned |
| 10 | Webhooks | Events trigger |

---

## Troubleshooting

### Services Not Starting

```bash
# Check logs
docker-compose logs -f

# Restart services
docker-compose restart
```

### Database Connection Issues

```bash
# Check database
docker exec repcon_db psql -U repcon -d repcon -c "SELECT 1"

# Reset database
docker-compose down -v
docker-compose up -d
```

### Ollama Not Responding

```bash
# Check Ollama
curl http://localhost:11434/api/tags

# Restart Ollama
sudo systemctl restart ollama
```

---

## CI/CD Integration

To run tests in CI:

```bash
# Start services
docker-compose up -d

# Wait for readiness
sleep 10

# Run API tests
pytest backend/tests/ -v

# Run load tests
pytest backend/tests/load/ -v
```

---

*Last Updated: March 3, 2026*
*Version: 1.0.0*
