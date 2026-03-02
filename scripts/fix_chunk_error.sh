#!/bin/bash
# RepCon Voice Agent - Fix ChunkLoadError

echo "=== Fixing ChunkLoadError ==="

# Stop containers
docker-compose down

# Remove node_modules and dist to force clean build
rm -rf frontend/node_modules frontend/dist

# Rebuild everything
docker-compose build --no-cache

# Start fresh
docker-compose up -d

echo "=== Waiting for services ==="
sleep 30

# Check status
docker-compose ps

echo ""
echo "=== Fix Applied ==="
echo "Frontend should be accessible at http://localhost:3000"
