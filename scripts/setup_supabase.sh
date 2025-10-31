#!/bin/bash

# Supabase Setup Script
# This script helps set up the database connection and run initial migrations

echo "🚀 Setting up Supabase connection..."

# Check if .env exists
if [ ! -f "backend/.env" ]; then
    echo "❌ backend/.env file not found!"
    echo "📝 Creating from template..."
    cp .env.example backend/.env
    echo "✅ Please edit backend/.env with your Supabase connection string"
    exit 1
fi

# Check if DATABASE_URL is set
source backend/.env
if [ -z "$DATABASE_URL" ]; then
    echo "❌ DATABASE_URL not set in backend/.env"
    echo "💡 Get your connection string from Supabase Dashboard → Settings → Database"
    exit 1
fi

echo "✅ DATABASE_URL found"

# Check if virtual environment exists
if [ ! -d "backend/venv" ]; then
    echo "📦 Creating virtual environment..."
    cd backend
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    cd ..
fi

# Activate virtual environment
source backend/venv/bin/activate

echo "🔄 Running database migrations..."
cd backend
alembic upgrade head

echo "🌱 Seeding database..."
python scripts/seed_database.py

echo "✅ Setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Verify tables in Supabase Dashboard → Table Editor"
echo "2. Deploy backend to Railway/Render"
echo "3. Deploy frontend to Vercel"
echo ""
echo "🔗 See DEPLOYMENT_SUPABASE.md for full instructions"

