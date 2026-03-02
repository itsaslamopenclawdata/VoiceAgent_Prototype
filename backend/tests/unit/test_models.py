"""
RepCon Voice Agent - Unit Tests - Models
"""
import pytest
from datetime import datetime
from app.models.models import (
    Institute, User, VoiceConfig, Course, 
    Student, Call, StudentActivity, CallTranscript,
    DailyStats, Setting, AuditLog
)


class TestInstitute:
    """Tests for Institute model"""
    
    def test_institute_creation(self):
        """Test institute can be created"""
        institute = Institute(
            name="Test Institute",
            slug="test-institute",
            phone_number="+919876543210",
            email="test@institute.com"
        )
        assert institute.name == "Test Institute"
        assert institute.slug == "test-institute"
        assert institute.is_active is True
    
    def test_institute_defaults(self):
        """Test institute default values"""
        institute = Institute(
            name="Test",
            slug="test"
        )
        assert institute.timezone == "Asia/Kolkata"
        assert institute.is_active is True


class TestUser:
    """Tests for User model"""
    
    def test_user_creation(self):
        """Test user can be created"""
        user = User(
            email="user@test.com",
            password_hash="hashed_password",
            full_name="Test User",
            role="admin"
        )
        assert user.email == "user@test.com"
        assert user.role == "admin"
        assert user.is_active is True
    
    def test_user_default_role(self):
        """Test user default role"""
        user = User(
            email="test@test.com",
            password_hash="hash"
        )
        assert user.role == "admin"


class TestCourse:
    """Tests for Course model"""
    
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
    
    def test_course_job_roles(self):
        """Test job roles as array"""
        course = Course(
            course_name="Test",
            duration="3 months",
            fee=10000,
            job_roles=["Data Analyst", "ML Engineer"],
            institute_id=1
        )
        assert len(course.job_roles) == 2
        assert "Data Analyst" in course.job_roles


class TestStudent:
    """Tests for Student (Lead) model"""
    
    def test_student_creation(self):
        """Test student can be created"""
        student = Student(
            name="Rahul Sharma",
            phone="+919876543210",
            institute_id=1
        )
        assert student.name == "Rahul Sharma"
        assert student.phone == "+919876543210"
        assert student.status == "new"
    
    def test_student_status_default(self):
        """Test student default status"""
        student = Student(
            name="Test",
            phone="9876543210",
            institute_id=1
        )
        assert student.status == "new"
        assert student.priority == "normal"
        assert student.source == "voice_agent"


class TestCall:
    """Tests for Call model"""
    
    def test_call_creation(self):
        """Test call can be created"""
        call = Call(
            caller_phone="+919876543210",
            institute_id=1,
            status="in_progress"
        )
        assert call.caller_phone == "+919876543210"
        assert call.status == "in_progress"
        assert call.direction == "inbound"
    
    def test_call_duration_calculation(self):
        """Test call duration"""
        call = Call(
            caller_phone="+919876543210",
            institute_id=1,
            started_at=datetime(2026, 3, 2, 10, 0, 0),
            ended_at=datetime(2026, 3, 2, 10, 5, 0)
        )
        assert call.duration == 300  # 5 minutes
