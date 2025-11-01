#!/bin/bash
# Automated Deployment Script
# This will deploy backend to Railway and frontend to Vercel

set -e

echo "🚀 No Colon, Still Rollin' - Automated Deployment"
echo "=================================================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check CLI tools
echo -e "${YELLOW}Checking deployment tools...${NC}"

if ! command -v railway &> /dev/null; then
    echo "Installing Railway CLI..."
    curl -fsSL https://railway.app/install.sh | sh
fi

if ! command -v vercel &> /dev/null; then
    echo "Installing Vercel CLI..."
    npm install -g vercel
fi

echo -e "${GREEN}✅ CLI tools ready${NC}"
echo ""

# Deployment configuration
DATABASE_URL="postgresql://postgres.wpyntnmjncdizglqedyl:2022FreshStart@aws-1-us-east-2.pooler.supabase.com:6543/postgres"
SECRET_KEY="0986f53c88aaca014f0fa1c140fd24e7ec5deef9d595652d65c71e7308a7a3e8"

echo -e "${YELLOW}📋 Deployment Steps:${NC}"
echo ""
echo "This script will guide you through deployment."
echo "You'll need to authenticate once for each service."
echo ""

# Railway deployment
echo -e "${YELLOW}1. Deploying Backend to Railway...${NC}"
cd backend

if ! railway whoami &> /dev/null; then
    echo "🔐 Please login to Railway:"
    railway login
fi

echo "🚂 Initializing Railway project..."
railway init --name no-colon-backend || railway link

echo "📦 Setting environment variables..."
railway variables set DATABASE_URL="$DATABASE_URL"
railway variables set SECRET_KEY="$SECRET_KEY"
railway variables set CORS_ORIGINS="https://your-app.vercel.app,http://localhost:5173"

echo "🚀 Deploying backend..."
railway up

echo ""
echo -e "${GREEN}✅ Backend deployed!${NC}"
echo ""
read -p "Copy your Railway URL (e.g., https://xxx.railway.app): " RAILWAY_URL
echo ""

cd ../frontend

# Vercel deployment
echo -e "${YELLOW}2. Deploying Frontend to Vercel...${NC}"

if ! vercel whoami &> /dev/null; then
    echo "🔐 Please login to Vercel:"
    vercel login
fi

echo "🌐 Setting environment variable..."
vercel env add VITE_API_URL production <<< "$RAILWAY_URL"

echo "🚀 Deploying frontend..."
vercel --prod --yes

echo ""
echo -e "${GREEN}✅ Frontend deployed!${NC}"
echo ""
read -p "Copy your Vercel URL (e.g., https://xxx.vercel.app): " VERCEL_URL
echo ""

# Update CORS
echo -e "${YELLOW}3. Connecting services...${NC}"
cd ../backend
railway variables set CORS_ORIGINS="$VERCEL_URL,http://localhost:5173"

echo ""
echo -e "${GREEN}=================================================="
echo "🎉 Deployment Complete!"
echo "==================================================${NC}"
echo ""
echo "✅ Backend: $RAILWAY_URL"
echo "✅ Frontend: $VERCEL_URL"
echo ""
echo "🧪 Test your deployment:"
echo "   1. Visit: $VERCEL_URL"
echo "   2. Register a new user"
echo "   3. Generate a protocol"
echo "   4. Generate a workout"
echo ""
echo -e "${GREEN}🚀 Your system is live and ready to save a life!${NC}"

