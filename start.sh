#!/bin/bash

# Install dependencies if needed
if [ ! -d "frontend/node_modules" ]; then
  echo "Installing frontend dependencies..."
  cd frontend && npm install && cd ..
fi

# Start backend server in background
cd backend
echo "Starting backend on port 8000..."
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Wait for backend to start
sleep 5

# Start frontend dev server
cd ../frontend
echo "Starting frontend on port 5173..."
npm run dev -- --host 0.0.0.0 --port 5173

# If frontend exits, kill backend
kill $BACKEND_PID
