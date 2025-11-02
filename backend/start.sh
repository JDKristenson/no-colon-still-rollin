#!/bin/bash
set -e

echo "🚀 Starting No Colon, Still Rollin' Backend..."

# Change to backend directory
cd "$(dirname "$0")"

# Run migrations if needed (idempotent)
echo "📊 Running database migrations..."
alembic upgrade head || {
    echo "⚠️  Migration warning (may already be up to date)"
}

# Start the server
echo "🌟 Starting FastAPI server..."
exec python3 -m uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}

