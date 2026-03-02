"""
RepCon Voice Agent - Integration Tests - API
"""
import pytest
from httpx import AsyncClient
from app.main import app


@pytest.mark.asyncio
class TestAuthAPI:
    """Integration tests for Authentication API"""
    
    async def test_login_success(self):
        """Test successful login"""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                "/api/v1/auth/login",
                data={
                    "username": "admin@techvision.com",
                    "password": "admin123"
                }
            )
            assert response.status_code == 200
            assert "access_token" in response.json()
    
    async def test_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                "/api/v1/auth/login",
                data={
                    "username": "wrong@test.com",
                    "password": "wrong"
                }
            )
            assert response.status_code == 401


@pytest.mark.asyncio
class TestLeadsAPI:
    """Integration tests for Leads API"""
    
    async def test_get_leads(self):
        """Test getting leads list"""
        async with AsyncClient(app=app, base_url="http://test") as client:
            # Login first
            login_response = await client.post(
                "/api/v1/auth/login",
                data={"username": "admin@techvision.com", "password": "admin123"}
            )
            token = login_response.json()["access_token"]
            
            # Get leads
            response = await client.get(
                "/api/v1/leads/?institute_id=1",
                headers={"Authorization": f"Bearer {token}"}
            )
            assert response.status_code == 200
            assert "items" in response.json()
    
    async def test_create_lead(self):
        """Test creating a new lead"""
        async with AsyncClient(app=app, base_url="http://test") as client:
            login_response = await client.post(
                "/api/v1/auth/login",
                data={"username": "admin@techvision.com", "password": "admin123"}
            )
            token = login_response.json()["access_token"]
            
            response = await client.post(
                "/api/v1/leads/",
                headers={"Authorization": f"Bearer {token}"},
                json={
                    "name": "Test Lead",
                    "phone": "+919999999999",
                    "institute_id": 1
                }
            )
            assert response.status_code == 200


@pytest.mark.asyncio
class TestCallsAPI:
    """Integration tests for Calls API"""
    
    async def test_get_calls(self):
        """Test getting calls list"""
        async with AsyncClient(app=app, base_url="http://test") as client:
            login_response = await client.post(
                "/api/v1/auth/login",
                data={"username": "admin@techvision.com", "password": "admin123"}
            )
            token = login_response.json()["access_token"]
            
            response = await client.get(
                "/api/v1/calls/?institute_id=1",
                headers={"Authorization": f"Bearer {token}"}
            )
            assert response.status_code == 200


@pytest.mark.asyncio
class TestCoursesAPI:
    """Integration tests for Courses API"""
    
    async def test_get_courses(self):
        """Test getting courses list"""
        async with AsyncClient(app=app, base_url="http://test") as client:
            login_response = await client.post(
                "/api/v1/auth/login",
                data={"username": "admin@techvision.com", "password": "admin123"}
            )
            token = login_response.json()["access_token"]
            
            response = await client.get(
                "/api/v1/courses/?institute_id=1",
                headers={"Authorization": f"Bearer {token}"}
            )
            assert response.status_code == 200
            assert "items" in response.json()


@pytest.mark.asyncio
class TestStatsAPI:
    """Integration tests for Stats API"""
    
    async def test_dashboard_stats(self):
        """Test getting dashboard stats"""
        async with AsyncClient(app=app, base_url="http://test") as client:
            login_response = await client.post(
                "/api/v1/auth/login",
                data={"username": "admin@techvision.com", "password": "admin123"}
            )
            token = login_response.json()["access_token"]
            
            response = await client.get(
                "/api/v1/stats/dashboard?institute_id=1",
                headers={"Authorization": f"Bearer {token}"}
            )
            assert response.status_code == 200
            assert "today" in response.json()
