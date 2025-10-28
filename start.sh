#!/bin/bash

# Start backend server in background
cd backend
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 &

# Wait for backend to start
sleep 3

# Start frontend dev server
cd ../frontend
npm run dev -- --host 0.0.0.0 --port 5173
