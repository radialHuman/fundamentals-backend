#!/bin/bash
echo "Stopping and removing all containers..."
docker-compose down

echo "Removing custom network..."
docker network rm backend-network 2>/dev/null || true

echo "Cleaning up unused images..."
docker image prune -f

echo "Shutdown complete!"