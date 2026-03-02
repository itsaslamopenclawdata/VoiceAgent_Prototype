#!/bin/bash
# RepCon Voice Agent - Local Test Script
# Run this to test the voice agent without Twilio

echo "=== RepCon Voice Agent - Local Test ==="
echo ""

# Check if containers are running
echo "Checking services..."
curl -s http://localhost:8000/health > /dev/null && echo "✅ Backend: Running" || echo "❌ Backend: Not running"
curl -s http://localhost:3000 > /dev/null && echo "✅ Frontend: Running" || echo "❌ Frontend: Not running"

echo ""
echo "=== API Endpoints ==="
echo "Backend: http://localhost:8000"
echo "API Docs: http://localhost:8000/docs"
echo "Frontend: http://localhost:3000"

echo ""
echo "=== Test Calls (Local) ==="

# Login and get token
echo "1. Logging in..."
TOKEN=$(curl -s -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin@techvision.com&password=admin123" | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4)

if [ -z "$TOKEN" ]; then
  echo "❌ Login failed"
  exit 1
fi

echo "✅ Logged in"

# Test leads endpoint
echo "2. Testing leads endpoint..."
curl -s -H "Authorization: Bearer $TOKEN" "http://localhost:8000/api/v1/leads/?institute_id=1" | head -c 200
echo ""

# Test calls endpoint
echo "3. Testing calls endpoint..."
curl -s -H "Authorization: Bearer $TOKEN" "http://localhost:8000/api/v1/calls/?institute_id=1" | head -c 200
echo ""

# Test courses endpoint
echo "4. Testing courses endpoint..."
curl -s -H "Authorization: Bearer $TOKEN" "http://localhost:8000/api/v1/courses/?institute_id=1" | head -c 200
echo ""

# Test webhook status
echo "5. Testing webhook status (local mode)..."
curl -s "http://localhost:8000/api/v1/webhooks/status"
echo ""

# Create a test call record
echo "6. Creating test call..."
curl -s -X POST "http://localhost:8000/api/v1/webhooks/local/test-call" \
  -H "Content-Type: application/json" \
  -d '{"institute_id": 1, "caller_phone": "+919999999999"}'
echo ""

echo ""
echo "=== Test Complete ==="
echo ""
echo "Open http://localhost:3000 to view the dashboard"
