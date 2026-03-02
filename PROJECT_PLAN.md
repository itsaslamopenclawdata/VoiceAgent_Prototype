# RepCon - The Voice Agent

## Project Overview

**Project Name:** RepCon - The Voice Agent  
**Purpose:** AI-powered voice agent for small-scale educational institutes to automate inbound inquiries  
**Target Users:** Educational institutes offering courses with telecallers for student enrollment  

---

## Problem Statement

Educational institutes receive numerous inbound calls from prospective students asking about:
- Course details (duration, fees, syllabus)
- Job roles after course completion
- Batch timings and schedules
- Admission process

Currently handled by human telecallers - expensive, inconsistent, not available 24/7.

---

## Solution

An AI Voice Agent that:
1. Answers inbound calls automatically
2. Provides course information from Google Sheets knowledge base
3. Captures student details (name, phone, email, interest)
4. Stores leads in database for follow-up
5. Works 24/7 with consistent responses

---

## Architecture Overview

```
                    ┌─────────────────┐
                    │   Phone Line    │
                    │  (Twilio/Vonage)│
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │   Voice Agent   │
                    │    (RTVI/       │
                    │   VAPI/Silero)  │
                    └────────┬────────┘
                             │
         ┌───────────────────┼───────────────────┐
         │                   │                   │
         ▼                   ▼                   ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│  Google Sheets  │ │   LLM Server    │ │    Database     │
│ (Knowledge Base)│ │  (Open Source)  │ │   (PostgreSQL)  │
└─────────────────┘ └─────────────────┘ └─────────────────┘
```

---

## Tech Stack

### **Frontend**
| Technology | Purpose | License |
|------------|---------|---------|
| React + Vite | UI Framework | MIT |
| Tailwind CSS | Styling | MIT |
| TypeScript | Type Safety | Apache 2.0 |

### **Backend**
| Technology | Purpose | License |
|------------|---------|---------|
| FastAPI | API Framework | MIT |
| Python 3.11 | Language | PSF |
| SQLAlchemy | ORM | MIT |
| Pydantic | Validation | MIT |

### **Voice & AI**
| Technology | Purpose | License |
|------------|---------|---------|
| VAPI | Voice Infrastructure (free tier) | Proprietary |
| **OR** | | |
| RTVI | Real-time Voice AI | MIT |
| **OR** | | |
| Silero VAD + TTS | Voice Activity Detection + TTS | Apache 2.0 |
| **LLM** | | |
| Ollama | Local LLM Server | MIT |
| llama3.2 / mistral | Open Source Models | Llama 3.2 / Apache 2.0 |

### **Database**
| Technology | Purpose | License |
|------------|---------|---------|
| PostgreSQL | Primary Database | PostgreSQL |
| Redis | Caching + Queue | Redis |

### **Infrastructure**
| Technology | Purpose | License |
|------------|---------|---------|
| Docker | Containerization | Apache 2.0 |
| Docker Compose | Orchestration | Apache 2.0 |

---

## Step-by-Step Implementation Plan

### Phase 1: Setup & Infrastructure

#### Step 1.1: Initialize Project
```bash
# Create project structure
mkdir -p RepCon-Voice-Agent/{backend,frontend,docker,docs,scripts}

# Setup Docker environment
cd docker
# Create Dockerfile for backend
# Create Dockerfile for frontend
# Create docker-compose.yml
```

#### Step 1.2: Database Setup
```sql
-- Students table
CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    phone VARCHAR(20) UNIQUE,
    email VARCHAR(255),
    interest_course VARCHAR(255),
    source VARCHAR(50), -- 'voice_agent', 'manual'
    status VARCHAR(50), -- 'new', 'contacted', 'enrolled', 'lost'
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Call logs table
CREATE TABLE call_logs (
    id SERIAL PRIMARY KEY,
    student_id INTEGER REFERENCES students(id),
    phone VARCHAR(20),
    duration INTEGER, -- seconds
    recording_url TEXT,
    transcript TEXT,
    outcome VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Courses table (sync from Google Sheets)
CREATE TABLE courses (
    id SERIAL PRIMARY KEY,
    course_name VARCHAR(255),
    duration VARCHAR(50),
    fee DECIMAL(10,2),
    job_roles TEXT[], -- Array of strings
    syllabus TEXT,
    prerequisites TEXT,
    source_google_sheet_id VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

### Phase 2: Backend Development

#### Step 2.1: FastAPI Backend Setup
```python
# main.py - Entry point
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="RepCon Voice Agent API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
from routers import students, courses, calls, webhooks
app.include_router(students.router, prefix="/api/v1")
app.include_router(courses.router, prefix="/api/v1")
app.include_router(calls.router, prefix="/api/v1")
app.include_router(webhooks.router, prefix="/api/v1")
```

#### Step 2.2: Google Sheets Integration
```python
# services/google_sheets.py
import gspread
from oauth2client.service_account import ServiceAccountCredentials

class GoogleSheetsService:
    def __init__(self, credentials_path: str):
        self.scope = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive'
        ]
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name(
            credentials_path, self.scope
        )
        self.client = gspread.authorize(self.credentials)
    
    def sync_courses(self, spreadsheet_url: str) -> List[dict]:
        """Fetch courses from Google Sheet and sync to database"""
        sheet = self.client.open_by_url(spreadsheet_url)
        worksheet = sheet.get_worksheet(0)
        records = worksheet.get_all_records()
        
        courses = []
        for row in records:
            courses.append({
                'course_name': row.get('Course Name'),
                'duration': row.get('Duration'),
                'fee': row.get('Course Fee'),
                'job_roles': row.get('Job Roles', '').split(','),
                'syllabus': row.get('Syllabus', ''),
                'prerequisites': row.get('Prerequisites', '')
            })
        return courses
```

#### Step 2.3: LLM Integration (Ollama)
```python
# services/llm.py
import requests
from typing import List, Dict

class LLMService:
    def __init__(self, ollama_url: str = "http://localhost:11434"):
        self.ollama_url = ollama_url
        self.model = "llama3.2"
    
    def get_response(self, prompt: str, context: str) -> str:
        """Get response from Ollama"""
        full_prompt = f"""You are a helpful voice assistant for an educational institute.
        Answer questions based ONLY on the provided context.
        
        Context:
        {context}
        
        Question: {prompt}
        
        Be concise and friendly. Format for spoken response (not too formal).
        """
        
        response = requests.post(
            f"{self.ollama_url}/api/generate",
            json={
                "model": self.model,
                "prompt": full_prompt,
                "stream": False
            }
        )
        return response.json().get('response', '')
    
    def build_context(self, courses: List[dict]) -> str:
        """Build context string from course data"""
        context = "Available Courses:\n\n"
        for course in courses:
            context += f"Course: {course['course_name']}\n"
            context += f"Duration: {course['duration']}\n"
            context += f"Fee: ₹{course['fee']}\n"
            context += f"Job Roles: {', '.join(course.get('job_roles', []))}\n"
            context += f"Syllabus: {course.get('syllabus', 'N/A')}\n"
            context += "---\n"
        return context
```

---

### Phase 3: Voice Agent Setup

#### Step 3.1: Voice Provider Integration (VAPI - Free Tier)
```python
# services/voice.py
class VoiceService:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.vapi.ai"
    
    def create_assistant(self, config: dict) -> dict:
        """Create voice assistant with custom instructions"""
        response = requests.post(
            f"{self.base_url}/assistant",
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={
                "name": "RepCon Educational Assistant",
                "model": {
                    "provider": "openai",
                    "model": "gpt-4o-mini",
                    "system_prompt": """You are a helpful voice assistant for an educational institute.
                    Your task is to:
                    1. Greet callers warmly
                    2. Answer questions about courses, fees, duration, job placements
                    3. Ask for caller name, phone number, and email
                    4. Capture their interest in specific courses
                    5. Thank them and end the call professionally
                    
                    Always be polite, patient, and concise.
                    """
                },
                "voice": "rachel",  # Free voice option
                "transcription": {
                    "provider": "deepgram"
                }
            }
        )
        return response.json()
    
    def get_call_details(self, call_id: str) -> dict:
        """Get call recording and transcript"""
        response = requests.get(
            f"{self.base_url}/call/{call_id}",
            headers={"Authorization": f"Bearer {self.api_key}"}
        )
        return response.json()
```

#### Step 3.2: Alternative - Self-Hosted Voice (RTVI)
```javascript
// frontend/src/services/voiceAgent.js
import { RTVIClient } from '@rtvi-ai/rtvi-client-js';

class VoiceAgent {
  constructor() {
    this.client = null;
    this.llmEndpoint = 'http://localhost:8000/api/v1/llm';
  }
  
  async initialize() {
    this.client = new RTVIClient({
      baseUrl: 'ws://localhost:8000',
      config: {
        model: {
          provider: 'ollama',
          model: 'llama3.2',
          url: this.llmEndpoint
        },
        voice: {
          provider: 'silero',
          voice: 'aidar'
        }
      }
    });
    
    await this.client.connect();
  }
  
  async sendMessage(text) {
    return await this.client.sendText(text);
  }
}
```

---

### Phase 4: Frontend Development

#### Step 4.1: Admin Dashboard
```jsx
// frontend/src/App.jsx
import { Routes, Route } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import Students from './pages/Students';
import Courses from './pages/Courses';
import Calls from './pages/Calls';
import Settings from './pages/Settings';

function App() {
  return (
    <div className="min-h-screen bg-gray-100">
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/students" element={<Students />} />
        <Route path="/courses" element={<Courses />} />
        <Route path="/calls" element={<Calls />} />
        <Route path="/settings" element={<Settings />} />
      </Routes>
    </div>
  );
}
```

#### Step 4.2: Student Management Page
```jsx
// frontend/src/pages/Students.jsx
import { useState, useEffect } from 'react';
import { DataTable } from '../components/DataTable';

export default function Students() {
  const [students, setStudents] = useState([]);
  
  useEffect(() => {
    fetchStudents();
  }, []);
  
  const fetchStudents = async () => {
    const response = await fetch('/api/v1/students');
    const data = await response.json();
    setStudents(data);
  };
  
  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Student Enquiries</h1>
      <DataTable 
        data={students} 
        columns={['Name', 'Phone', 'Email', 'Course Interest', 'Status', 'Date']}
      />
    </div>
  );
}
```

---

### Phase 5: Integration & Testing

#### Step 5.1: Webhook Handler
```python
# routers/webhooks.py
from fastapi import APIRouter, Request
from services.voice import VoiceService

router = APIRouter()

@router.post("/webhook/voice")
async def voice_webhook(request: Request):
    """Handle incoming calls and voice events"""
    data = await request.json()
    
    if data.get("event_type") == "call_started":
        # Log call start
        call_id = data.get("call_id")
        # Start recording
        return {"action": "continue"}
    
    elif data.get("event_type") == "transcript":
        # Process transcript
        transcript = data.get("transcript")
        # Store in database
        return {"action": "respond", "text": "Thank you for calling!"}
    
    elif data.get("event_type") == "call_ended":
        # Save call details
        call_id = data.get("call_id")
        duration = data.get("duration")
        # Update database
        return {"status": "completed"}
```

#### Step 5.2: Call Flow Logic
```python
# services/call_flow.py
class CallFlow:
    def __init__(self, llm_service, db_service):
        self.llm = llm_service
        self.db = db_service
    
    async def handle_call(self, transcript: str, student_phone: str) -> str:
        """Process call transcript and generate response"""
        
        # Get courses for context
        courses = self.db.get_courses()
        context = self.llm.build_context(courses)
        
        # Check for student info capture
        if self._needs_capture(transcript):
            # Extract and save student info
            student_data = self._extract_student_info(transcript)
            self.db.save_student(student_data)
        
        # Generate response
        response = self.llm.get_response(transcript, context)
        return response
    
    def _extract_student_info(self, text: str) -> dict:
        """Extract student details from conversation"""
        # Use regex/NLP to extract name, phone, email, interest
        pass
```

---

### Phase 6: Deployment

#### Step 6.1: Docker Configuration
```dockerfile
# docker/Dockerfile.backend
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```yaml
# docker/docker-compose.yml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/repcon
      - REDIS_URL=redis://redis:6379
      - OLLAMA_URL=http://ollama:11434
    depends_on:
      - db
      - redis
      - ollama

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend

  db:
    image: postgres:15
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=repcon
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama

volumes:
  postgres_data:
  redis_data:
  ollama_data:
```

#### Step 6.2: Production Deployment
```bash
# Build and run
cd docker
docker-compose up -d

# Check logs
docker-compose logs -f

# Stop
docker-compose down
```

---

## Google Sheets Structure

### Required Columns
| Column | Example |
|--------|---------|
| Course Name | Python Data Science |
| Duration | 3 months |
| Course Fee | 25000 |
| Job Roles | Data Analyst, ML Engineer, Data Scientist |
| Syllabus | Python, Pandas, NumPy, ML... |
| Prerequisites | Basic Python knowledge |

### Sample Data
```
| Course Name    | Duration | Fee   | Job Roles                    | Syllabus              |
|----------------|----------|-------|-------------------------------|-----------------------|
| Python DS      | 3 months | 25000 | Data Analyst, ML Engineer     | Python, Pandas, ML   |
| Web Dev        | 2 months | 20000 | Frontend Dev, Full Stack      | HTML, CSS, React     |
| Digital Market | 1 month  | 15000 | SEO Specialist, Marketing    | SEO, Ads, Analytics  |
```

---

## Free Tier Limits & Alternatives

| Service | Free Tier | Alternatives |
|---------|-----------|--------------|
| VAPI | 10 mins/month | RTVI (unlimited self-hosted) |
| Twilio | $15 credit | VoIP.ms, Asterisk (self-hosted) |
| Ollama | Unlimited (local) | llama.cpp, text-generation-webui |
| PostgreSQL | - | SQLite (for prototype) |
| Deepgram | 200 mins | Whisper (self-hosted) |

---

## Milestones

| Phase | Task | Duration |
|-------|------|----------|
| 1 | Setup + Docker + DB | 1 day |
| 2 | Backend API + Google Sheets | 2 days |
| 3 | LLM Integration (Ollama) | 1 day |
| 4 | Voice Agent Setup | 2 days |
| 5 | Frontend Dashboard | 2 days |
| 6 | Integration + Testing | 2 days |
| 7 | Deployment | 1 day |

**Total: ~11 days for prototype**

---

## Cost Estimation (Prototype)

| Component | Cost |
|-----------|------|
| Domain (optional) | $0-12/year |
| Hosting (VPS for Docker) | $5-20/month |
| Phone Number (Twilio) | $1/month |
| **Total** | **$6-32/month** |

---

## Next Steps

1. ✅ Project repo created
2. ⬜ Setup development environment
3. ⬜ Implement backend API
4. ⬜ Integrate Google Sheets
5. ⬜ Setup Ollama + LLM
6. ⬜ Integrate voice provider
7. ⬜ Build frontend dashboard
8. ⬜ Deploy with Docker

---

## Repo Structure

```
RepCon-Voice-Agent/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── routers/
│   │   ├── services/
│   │   └── models/
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   ├── package.json
│   └── Dockerfile
├── docker/
│   ├── docker-compose.yml
│   └── Dockerfile
├── docs/
│   └── README.md
└── scripts/
    └── setup.sh
```

---

*Document Version: 1.0*  
*Created: 2026-03-02*
