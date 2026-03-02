"""
RepCon Voice Agent - SQLAlchemy Models
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Numeric, Date, ARRAY
from sqlalchemy.orm import relationship

from app.db.session import Base


class Institute(Base):
    """Institute model"""
    __tablename__ = "institutes"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    slug = Column(String(100), unique=True, nullable=False, index=True)
    phone_number = Column(String(20))
    whatsapp_number = Column(String(20))
    email = Column(String(255))
    address = Column(Text)
    logo_url = Column(Text)
    website = Column(String(255))
    google_sheet_url = Column(Text)
    google_sheet_id = Column(String(255))
    timezone = Column(String(50), default="Asia/Kolkata")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    users = relationship("User", back_populates="institute", cascade="all, delete-orphan")
    courses = relationship("Course", back_populates="institute", cascade="all, delete-orphan")
    students = relationship("Student", back_populates="institute", cascade="all, delete-orphan")
    calls = relationship("Call", back_populates="institute", cascade="all, delete-orphan")
    voice_config = relationship("VoiceConfig", back_populates="institute", uselist=False, cascade="all, delete-orphan")


class User(Base):
    """User model"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    institute_id = Column(Integer, ForeignKey("institutes.id", ondelete="CASCADE"))
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255))
    role = Column(String(50), default="admin")
    is_active = Column(Boolean, default=True)
    last_login = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    institute = relationship("Institute", back_populates="users")


class VoiceConfig(Base):
    """Voice configuration model"""
    __tablename__ = "voice_configs"
    
    id = Column(Integer, primary_key=True, index=True)
    institute_id = Column(Integer, ForeignKey("institutes.id", ondelete="CASCADE"), unique=True)
    greeting_message = Column(Text, default="Hello! Welcome to our institute. How can I help you today?")
    goodbye_message = Column(Text, default="Thank you for calling. Have a great day!")
    timeout_message = Column(Text, default="Sorry, I didn't catch that. Could you please repeat?")
    system_prompt = Column(Text)
    language = Column(String(10), default="en")
    voice_id = Column(String(50))
    max_call_duration = Column(Integer, default=300)
    max_silence_duration = Column(Integer, default=5)
    enable_recording = Column(Boolean, default=False)
    enable_transcription = Column(Boolean, default=True)
    enable_voicemail = Column(Boolean, default=True)
    voicemail_action = Column(String(20), default="callback")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    institute = relationship("Institute", back_populates="voice_config")


class Course(Base):
    """Course model"""
    __tablename__ = "courses"
    
    id = Column(Integer, primary_key=True, index=True)
    institute_id = Column(Integer, ForeignKey("institutes.id", ondelete="CASCADE"), index=True)
    course_name = Column(String(255), nullable=False)
    course_code = Column(String(50))
    description = Column(Text)
    duration = Column(String(50), nullable=False)
    duration_days = Column(Integer)
    fee = Column(Numeric(10, 2), nullable=False)
    fee_currency = Column(String(3), default="INR")
    job_roles = Column(ARRAY(String))
    syllabus = Column(Text)
    prerequisites = Column(Text)
    eligibility = Column(Text)
    mode = Column(String(20), default="online")
    start_date = Column(Date)
    batch_time = Column(String(100))
    certificate = Column(Text)
    placement_assistance = Column(Boolean, default=False)
    source_updated = Column(DateTime)
    source_id = Column(String(255))
    is_active = Column(Boolean, default=True, index=True)
    display_order = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    institute = relationship("Institute", back_populates="courses")
    students = relationship("Student", back_populates="course_interest_relation")


class Student(Base):
    """Student/Lead model"""
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, index=True)
    institute_id = Column(Integer, ForeignKey("institutes.id", ondelete="CASCADE"), index=True)
    name = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=False, index=True)
    phone_country_code = Column(String(5), default="+91")
    email = Column(String(255))
    whatsapp_opt_in = Column(Boolean, default=False)
    course_interest = Column(Integer, ForeignKey("courses.id", ondelete="SET NULL"))
    source = Column(String(50), default="voice_agent", index=True)
    status = Column(String(50), default="new", index=True)
    priority = Column(String(20), default="normal")
    assigned_to = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    notes = Column(Text)
    follow_up_date = Column(Date)
    last_contacted_at = Column(DateTime)
    converted_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    institute = relationship("Institute", back_populates="students")
    course_interest_relation = relationship("Course", back_populates="students")
    calls = relationship("Call", back_populates="student")
    activities = relationship("StudentActivity", back_populates="student", cascade="all, delete-orphan")


class Call(Base):
    """Call model"""
    __tablename__ = "calls"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="SET NULL"), index=True)
    institute_id = Column(Integer, ForeignKey("institutes.id", ondelete="CASCADE"), index=True)
    caller_phone = Column(String(20), nullable=False, index=True)
    caller_country_code = Column(String(5), default="+91")
    direction = Column(String(10), default="inbound")
    status = Column(String(20), default="no_answer", index=True)
    duration = Column(Integer)
    wait_time = Column(Integer)
    recording_url = Column(Text)
    recording_duration = Column(Integer)
    transcript = Column(Text)
    transcript_language = Column(String(10))
    summary = Column(Text)
    sentiment = Column(String(20))
    outcome = Column(String(50))
    cost = Column(Numeric(10, 2), default=0)
    twilio_call_sid = Column(String(100), index=True)
    started_at = Column(DateTime, index=True)
    answered_at = Column(DateTime)
    ended_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    student = relationship("Student", back_populates="calls")
    institute = relationship("Institute", back_populates="calls")
    transcripts = relationship("CallTranscript", back_populates="call", cascade="all, delete-orphan")


class StudentActivity(Base):
    """Student activity log model"""
    __tablename__ = "student_activities"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), index=True)
    activity_type = Column(String(50), nullable=False, index=True)
    description = Column(Text)
    metadata = Column(ARRAY(String))
    performed_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    student = relationship("Student", back_populates="activities")


class CallTranscript(Base):
    """Call transcript model"""
    __tablename__ = "call_transcripts"
    
    id = Column(Integer, primary_key=True, index=True)
    call_id = Column(Integer, ForeignKey("calls.id", ondelete="CASCADE"), index=True)
    sequence_number = Column(Integer, nullable=False)
    speaker = Column(String(20), default="unknown")
    text = Column(Text, nullable=False)
    language = Column(String(10))
    start_time = Column(Integer)
    end_time = Column(Integer)
    confidence = Column(Numeric(5, 4))
    audio_url = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    call = relationship("Call", back_populates="transcripts")


class DailyStats(Base):
    """Daily statistics model"""
    __tablename__ = "daily_stats"
    
    id = Column(Integer, primary_key=True, index=True)
    institute_id = Column(Integer, ForeignKey("institutes.id", ondelete="CASCADE"), index=True)
    date = Column(Date, nullable=False, index=True)
    total_calls = Column(Integer, default=0)
    answered_calls = Column(Integer, default=0)
    missed_calls = Column(Integer, default=0)
    total_duration = Column(Integer, default=0)
    new_leads = Column(Integer, default=0)
    converted_leads = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        {"sqlite_autoincrement": True},
    )


class Setting(Base):
    """Settings key-value store"""
    __tablename__ = "settings"
    
    id = Column(Integer, primary_key=True, index=True)
    institute_id = Column(Integer, ForeignKey("institutes.id", ondelete="CASCADE"), index=True)
    key = Column(String(100), nullable=False)
    value = Column(Text)
    description = Column(String(255))
    is_encrypted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (
        {"sqlite_autoincrement": True},
    )


class AuditLog(Base):
    """Audit log for tracking changes"""
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    institute_id = Column(Integer, ForeignKey("institutes.id", ondelete="CASCADE"), index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), index=True)
    action = Column(String(100), nullable=False, index=True)
    entity_type = Column(String(50))
    entity_id = Column(Integer)
    old_value = Column(ARRAY(String))
    new_value = Column(ARRAY(String))
    ip_address = Column(String(45))
    user_agent = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
