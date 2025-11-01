#!/bin/bash
# Automated deployment script

echo "🚀 Starting deployment process..."

# Check for Railway CLI
if ! command -v railway &> /dev/null; then
    echo "📦 Installing Railway CLI..."
    curl -fsSL https://railway.app/install.sh | sh
fi

# Check for Vercel CLI
if ! command -v vercel &> /dev/null; then
    echo "📦 Installing Vercel CLI..."
    npm install -g vercel
fi

echo "✅ CLI tools ready"
