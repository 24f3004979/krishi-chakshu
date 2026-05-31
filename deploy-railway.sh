#!/bin/bash
# Quick deployment script for Railway.app
# Usage: bash deploy-railway.sh

set -e

echo "🚀 Krishi Chakshu - Railway Deployment"
echo "========================================"

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI not found. Installing..."
    npm install -g @railway/cli
fi

# Check if git is initialized
if [ ! -d .git ]; then
    echo "❌ Git not initialized. Run: git init"
    exit 1
fi

# Ensure files are committed
if [ -n "$(git status --porcelain)" ]; then
    echo "📝 Committing changes..."
    git add .
    git commit -m "Deploy to Railway"
fi

echo "🔐 Logging into Railway..."
railway login

echo "🎯 Initializing Railway project..."
railway init

echo "📤 Deploying to Railway..."
railway up

echo ""
echo "✅ Deployment started!"
echo "📊 Check status: railway logs"
echo "🌐 Your app will be live at: railway project link"
echo ""
echo "To set environment variables:"
echo "  railway variables set FLASK_ENV=production"
echo "  railway variables set FLASK_DEBUG=0"
