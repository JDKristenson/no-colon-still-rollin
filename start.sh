#!/bin/bash

echo "🚀 Starting No Colon Still Rollin'..."

# Start backend server in background
cd backend
echo "📡 Starting backend on port 8000..."
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Wait for backend to start
echo "⏳ Waiting for backend to start..."
sleep 5

# Start frontend dev server
cd ../frontend
echo "🎨 Starting frontend on port 5173..."
npm run dev -- --host 0.0.0.0 --port 5173

# If frontend exits, kill backend
echo "🛑 Shutting down..."
kill $BACKEND_PID 2>/dev/null
