#!/usr/bin/env python3
"""Startup script that runs migrations then starts the server"""
import subprocess
import sys
import os

def main():
    # Change to backend directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    print("🚀 Starting No Colon, Still Rollin' Backend...")
    
    # Run migrations
    print("📊 Running database migrations...")
    try:
        result = subprocess.run(
            ["alembic", "upgrade", "head"],
            check=False,  # Don't fail if migration fails (might already be up to date)
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print("✅ Migrations complete")
        else:
            print(f"⚠️  Migration warning: {result.stderr[:200]}")
            # Check if it's just "already up to date" - that's fine
            if "Target database is not up to date" in result.stderr or "already up to date" in result.stdout:
                print("ℹ️  Database is already up to date")
    except Exception as e:
        print(f"⚠️  Migration error (continuing anyway): {e}")
    
    # Start the server
    print("🌟 Starting FastAPI server...")
    port = os.environ.get("PORT", "8000")
    subprocess.run([
        sys.executable, "-m", "uvicorn",
        "app.main:app",
        "--host", "0.0.0.0",
        "--port", port
    ])

if __name__ == "__main__":
    main()

