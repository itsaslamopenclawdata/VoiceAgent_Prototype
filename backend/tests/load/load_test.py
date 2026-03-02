"""
RepCon Voice Agent - Load Tests
"""
from locust import HttpUser, task, between, events
import random


class VoiceAgentUser(HttpUser):
    """Locust load test user"""
    
    wait_time = between(1, 3)
    token = None
    institute_id = 1
    
    def on_start(self):
        """Login before tests"""
        response = self.client.post(
            "/api/v1/auth/login",
            data={
                "username": "admin@techvision.com",
                "password": "admin123"
            }
        )
        if response.status_code == 200:
            VoiceAgentUser.token = response.json()["access_token"]
    
    @task(5)
    def get_leads(self):
        """Get leads list"""
        if self.token:
            self.client.get(
                f"/api/v1/leads/?institute_id={self.institute_id}",
                headers={"Authorization": f"Bearer {self.token}"}
            )
    
    @task(3)
    def get_calls(self):
        """Get calls list"""
        if self.token:
            self.client.get(
                f"/api/v1/calls/?institute_id={self.institute_id}",
                headers={"Authorization": f"Bearer {self.token}"}
            )
    
    @task(2)
    def get_courses(self):
        """Get courses list"""
        if self.token:
            self.client.get(
                f"/api/v1/courses/?institute_id={self.institute_id}",
                headers={"Authorization": f"Bearer {self.token}"}
            )
    
    @task(2)
    def get_dashboard(self):
        """Get dashboard stats"""
        if self.token:
            self.client.get(
                f"/api/v1/stats/dashboard?institute_id={self.institute_id}",
                headers={"Authorization": f"Bearer {self.token}"}
            )
    
    @task(1)
    def create_lead(self):
        """Create a new lead"""
        if self.token:
            phone = f"+919{random.randint(100000000, 999999999)}"
            self.client.post(
                "/api/v1/leads/",
                headers={"Authorization": f"Bearer {self.token}"},
                json={
                    "name": f"Load Test {random.randint(1000, 9999)}",
                    "phone": phone,
                    "institute_id": self.institute_id
                }
            )
    
    @task(1)
    def health_check(self):
        """Check health endpoint"""
        self.client.get("/health")


class VoiceAgentAPILoad(HttpUser):
    """API-only load test"""
    
    wait_time = between(0.5, 1.5)
    
    @task(10)
    def health(self):
        """Health check"""
        self.client.get("/health")
    
    @task(5)
    def ready(self):
        """Readiness check"""
        self.client.get("/ready")


# Run with:
# locust -f tests/load/load_test.py --host=http://localhost:8000 --users=100 --spawn-rate=10
