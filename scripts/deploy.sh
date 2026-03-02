#!/bin/bash
# RepCon Voice Agent - Deployment Script

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}=== RepCon Voice Agent Deployment ===${NC}"

# Check if .env exists
if [ ! -f backend/.env ]; then
    echo -e "${YELLOW}Warning: .env file not found. Copy from .env.example${NC}"
    cp backend/.env.example backend/.env
fi

# Pull latest changes
echo -e "${YELLOW}Pulling latest changes...${NC}"
git pull origin main

# Build images
echo -e "${YELLOW}Building Docker images...${NC}"
docker-compose build

# Start services
echo -e "${YELLOW}Starting services...${NC}"
docker-compose up -d

# Wait for services
echo -e "${YELLOW}Waiting for services...${NC}"
sleep 10

# Check health
echo -e "${YELLOW}Checking health...${NC}"
curl -f http://localhost:8000/health || {
    echo -e "${RED}Health check failed!${NC}"
    docker-compose logs
    exit 1
}

echo -e "${GREEN}Deployment complete!${NC}"
echo -e "API: http://localhost:8000"
echo -e "Docs: http://localhost:8000/docs"
echo -e "Frontend: http://localhost:3000"
