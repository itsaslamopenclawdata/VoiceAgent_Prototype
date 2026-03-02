#!/bin/bash
# RepCon Voice Agent - Development Script

set -e

# Start development environment
echo "Starting RepCon Voice Agent development environment..."

# Create .env from example if not exists
if [ ! -f backend/.env ]; then
    cp backend/.env.example backend/.env
    echo "Created .env from example. Please configure it."
fi

# Start Docker services
docker-compose up -d

# Wait for database
echo "Waiting for database..."
sleep 5

# Show status
echo ""
echo "=== Services ==="
docker-compose ps

echo ""
echo "=== Access Points ==="
echo "API: http://localhost:8000"
echo "API Docs: http://localhost:8000/docs"
echo "Frontend: http://localhost:3000"

echo ""
echo "To view logs: docker-compose logs -f"
echo "To stop: docker-compose down"
