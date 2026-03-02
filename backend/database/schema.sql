-- RepCon Voice Agent Database Schema
-- PostgreSQL 15+

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- ============================================
-- INSTITUTES TABLE
-- ============================================
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

-- Indexes
CREATE INDEX idx_institutes_slug ON institutes(slug);
CREATE INDEX idx_institutes_is_active ON institutes(is_active);

-- ============================================
-- USERS TABLE
-- ============================================
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

-- Indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_institute_id ON users(institute_id);
CREATE INDEX idx_users_role ON users(role);

-- ============================================
-- VOICE CONFIGS TABLE
-- ============================================
CREATE TABLE voice_configs (
    id SERIAL PRIMARY KEY,
    institute_id INTEGER REFERENCES institutes(id) ON DELETE CASCADE UNIQUE,
    greeting_message TEXT DEFAULT 'Hello! Welcome to our institute. How can I help you today?',
    goodbye_message TEXT DEFAULT 'Thank you for calling. Have a great day!',
    timeout_message TEXT DEFAULT 'Sorry, I didnt catch that. Could you please repeat?',
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

-- ============================================
-- COURSES TABLE
-- ============================================
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

-- Indexes
CREATE INDEX idx_courses_institute_id ON courses(institute_id);
CREATE INDEX idx_courses_is_active ON courses(is_active);
CREATE INDEX idx_courses_mode ON courses(mode);

-- ============================================
-- STUDENTS (LEADS) TABLE
-- ============================================
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

-- Indexes
CREATE INDEX idx_students_institute_id ON students(institute_id);
CREATE INDEX idx_students_phone ON students(phone);
CREATE INDEX idx_students_status ON students(status);
CREATE INDEX idx_students_course_interest ON students(course_interest);
CREATE INDEX idx_students_created_at ON students(created_at);
CREATE INDEX idx_students_source ON students(source);

-- ============================================
-- CALLS TABLE
-- ============================================
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

-- Indexes
CREATE INDEX idx_calls_institute_id ON calls(institute_id);
CREATE INDEX idx_calls_student_id ON calls(student_id);
CREATE INDEX idx_calls_caller_phone ON calls(caller_phone);
CREATE INDEX idx_calls_status ON calls(status);
CREATE INDEX idx_calls_started_at ON calls(started_at);
CREATE INDEX idx_calls_twilio_sid ON calls(twilio_call_sid);

-- ============================================
-- STUDENT ACTIVITIES TABLE
-- ============================================
CREATE TABLE student_activities (
    id SERIAL PRIMARY KEY,
    student_id INTEGER REFERENCES students(id) ON DELETE CASCADE,
    activity_type VARCHAR(50) NOT NULL,
    description TEXT,
    metadata JSONB,
    performed_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_student_activities_student_id ON student_activities(student_id);
CREATE INDEX idx_student_activities_type ON student_activities(activity_type);
CREATE INDEX idx_student_activities_created_at ON student_activities(created_at);

-- ============================================
-- CALL TRANSCRIPTS TABLE
-- ============================================
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

-- Indexes
CREATE INDEX idx_call_transcripts_call_id ON call_transcripts(call_id);

-- ============================================
-- DAILY STATS TABLE
-- ============================================
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

-- Indexes
CREATE INDEX idx_daily_stats_institute_date ON daily_stats(institute_id, date);

-- ============================================
-- SETTINGS TABLE
-- ============================================
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

-- Indexes
CREATE INDEX idx_settings_institute_id ON settings(institute_id);

-- ============================================
-- AUDIT LOGS TABLE
-- ============================================
CREATE TABLE audit_logs (
    id SERIAL PRIMARY KEY,
    institute_id INTEGER REFERENCES institutes(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    action VARCHAR(100) NOT NULL,
    entity_type VARCHAR(50),
    entity_id INTEGER,
    old_value JSONB,
    new_value JSONB,
    ip_address VARCHAR(45),
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_audit_logs_institute_id ON audit_logs(institute_id);
CREATE INDEX idx_audit_logs_user_id ON audit_logs(user_id);
CREATE INDEX idx_audit_logs_action ON audit_logs(action);
CREATE INDEX idx_audit_logs_created_at ON audit_logs(created_at);

-- ============================================
-- TRIGGERS
-- ============================================

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply updated_at trigger to all tables
CREATE TRIGGER update_institutes_updated_at BEFORE UPDATE ON institutes
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_voice_configs_updated_at BEFORE UPDATE ON voice_configs
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_courses_updated_at BEFORE UPDATE ON courses
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_students_updated_at BEFORE UPDATE ON students
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_calls_updated_at BEFORE UPDATE ON calls
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_settings_updated_at BEFORE UPDATE ON settings
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================
-- SEED DATA
-- ============================================

-- Insert sample institute
INSERT INTO institutes (name, slug, phone_number, email, address, timezone)
VALUES ('TechVision Academy', 'techvision-academy', '+91-9876543210', 'info@techvisionacademy.com', '123 Tech Park, Hyderabad, Telangana', 'Asia/Kolkata');

-- Insert admin user (password: admin123)
INSERT INTO users (institute_id, email, password_hash, full_name, role)
VALUES (1, 'admin@techvision.com', crypt('admin123', gen_salt('bf')), 'Admin User', 'admin');

-- Insert voice config
INSERT INTO voice_configs (institute_id, greeting_message, goodbye_message, language, voice_id, max_call_duration)
VALUES (1, 'Hello! Welcome to TechVision Academy. How can I help you today?', 'Thank you for calling TechVision Academy. Have a great day!', 'en', 'af_sarah', 300);

-- Insert sample courses
INSERT INTO courses (institute_id, course_name, course_code, description, duration, fee, job_roles, mode, is_active, display_order)
VALUES 
(1, 'Python Data Science', 'PY-DS-01', 'Master data science with Python including ML and AI', '6 months', 35000, ARRAY['Data Scientist', 'ML Engineer', 'Data Analyst'], 'online', true, 1),
(1, 'Full Stack Web Development', 'FS-WD-01', 'Become a full-stack developer with React and Node.js', '6 months', 40000, ARRAY['Full Stack Developer', 'Web Developer', 'Frontend Developer'], 'online', true, 2),
(1, 'Digital Marketing', 'DM-01', 'Learn SEO, SEM, social media marketing', '3 months', 20000, ARRAY['Digital Marketer', 'SEO Specialist', 'Social Media Manager'], 'online', true, 3),
(1, 'Cloud Computing with AWS', 'AWS-01', 'AWS cloud practitioner and developer certification', '4 months', 30000, ARRAY['Cloud Engineer', 'DevOps Engineer', 'AWS Developer'], 'online', true, 4),
(1, 'Mobile App Development', 'MAD-01', 'Build iOS and Android apps with Flutter', '5 months', 35000, ARRAY['Mobile Developer', 'App Developer', 'Flutter Developer'], 'online', true, 5),
(1, 'Artificial Intelligence & Machine Learning', 'AI-ML-01', 'Deep dive into AI and ML algorithms', '8 months', 50000, ARRAY['AI Engineer', 'ML Engineer', 'Research Scientist'], 'online', true, 6),
(1, 'Cybersecurity', 'CS-01', 'Learn ethical hacking and network security', '6 months', 40000, ARRAY['Security Analyst', 'Ethical Hacker', 'Network Security'], 'online', true, 7),
(1, 'UI/UX Design', 'UI-UX-01', 'Design user interfaces and experiences', '4 months', 25000, ARRAY['UI Designer', 'UX Designer', 'Product Designer'], 'online', true, 8);

-- Insert sample leads
INSERT INTO students (institute_id, name, phone, email, course_interest, status, source)
VALUES 
(1, 'Rahul Sharma', '+919876543210', 'rahul.sharma@email.com', 1, 'new', 'voice_agent'),
(1, 'Priya Patel', '+919876543211', 'priya.patel@email.com', 2, 'contacted', 'voice_agent'),
(1, 'Amit Kumar', '+919876543212', 'amit.kumar@email.com', 3, 'interested', 'voice_agent'),
(1, 'Sneha Reddy', '+919876543213', 'sneha.reddy@email.com', 1, 'enrolled', 'voice_agent'),
(1, 'Vikram Singh', '+919876543214', 'vikram.singh@email.com', 4, 'new', 'voice_agent'),
(1, 'Anjali Gupta', '+919876543215', 'anjali.gupta@email.com', 2, 'contacted', 'voice_agent'),
(1, 'Raj Malhotra', '+919876543216', 'raj.malhotra@email.com', 5, 'interested', 'voice_agent'),
(1, 'Kavya Nair', '+919876543217', 'kavya.nair@email.com', 6, 'new', 'voice_agent'),
(1, 'Suresh Yadav', '+919876543218', 'suresh.yadav@email.com', 3, 'lost', 'voice_agent'),
(1, 'Meera Shah', '+919876543219', 'meera.shah@email.com', 7, 'new', 'voice_agent');

-- Insert sample calls
INSERT INTO calls (institute_id, caller_phone, status, duration, transcript_language, started_at, answered_at, ended_at)
VALUES 
(1, '+919876543210', 'completed', 180, 'en', CURRENT_TIMESTAMP - INTERVAL '2 hours', CURRENT_TIMESTAMP - INTERVAL '2 hours', CURRENT_TIMESTAMP - INTERVAL '1 hour 57 minutes'),
(1, '+919876543211', 'completed', 240, 'en', CURRENT_TIMESTAMP - INTERVAL '1 day', CURRENT_TIMESTAMP - INTERVAL '1 day', CURRENT_TIMESTAMP - INTERVAL '23 hours 56 minutes'),
(1, '+919876543212', 'completed', 300, 'hi', CURRENT_TIMESTAMP - INTERVAL '2 days', CURRENT_TIMESTAMP - INTERVAL '2 days', CURRENT_TIMESTAMP - INTERVAL '1 day 23 hours 55 minutes'),
(1, '+919876543213', 'missed', 0, 'en', CURRENT_TIMESTAMP - INTERVAL '3 days', NULL, NULL),
(1, '+919876543214', 'completed', 120, 'en', CURRENT_TIMESTAMP - INTERVAL '4 hours', CURRENT_TIMESTAMP - INTERVAL '4 hours', CURRENT_TIMESTAMP - INTERVAL '3 hours 58 minutes');

-- Insert sample daily stats
INSERT INTO daily_stats (institute_id, date, total_calls, answered_calls, missed_calls, total_duration, new_leads, converted_leads)
VALUES 
(1, CURRENT_DATE, 15, 12, 3, 4500, 5, 1),
(1, CURRENT_DATE - 1, 18, 15, 3, 5400, 7, 2),
(1, CURRENT_DATE - 2, 20, 17, 3, 6000, 8, 1),
(1, CURRENT_DATE - 3, 12, 10, 2, 3600, 4, 1),
(1, CURRENT_DATE - 4, 25, 22, 3, 7500, 10, 3);

-- Grant permissions
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO repcon;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO repcon;
