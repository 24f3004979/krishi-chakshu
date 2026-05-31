#!/bin/bash
# Docker build and test script
# Usage: bash deploy-docker.sh

set -e

echo "🐳 Building Docker image..."
docker build -t krishi-chakshu .

echo ""
echo "✅ Docker image built successfully!"
echo ""
echo "To run locally:"
echo "  docker run -p 5000:5000 krishi-chakshu"
echo ""
echo "To push to Docker Hub:"
echo "  docker tag krishi-chakshu YOUR_USERNAME/krishi-chakshu"
echo "  docker push YOUR_USERNAME/krishi-chakshu"
echo ""
echo "Testing locally..."
docker run -p 5000:5000 --rm -d --name krishi-test krishi-chakshu

sleep 3

echo "Testing endpoint..."
curl -s http://localhost:5000 | head -20 || echo "❌ Connection failed"

echo ""
echo "Stopping test container..."
docker stop krishi-test

echo "✅ Docker deployment ready!"
