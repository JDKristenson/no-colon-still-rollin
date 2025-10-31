#!/usr/bin/env python3
"""
Interactive script to help find and set up Supabase connection string
"""

print("=" * 60)
print("🔍 Supabase Connection String Finder")
print("=" * 60)
print()
print("Let's find your connection string. Follow these steps:")
print()
print("1. Open your browser and go to:")
print("   https://supabase.com/dashboard/project/wpyntnmjncdizglqedyl")
print()
print("2. In the left sidebar, click 'Settings' (gear icon)")
print()
print("3. Click 'Database' (under Project Settings)")
print()
print("4. Scroll down to 'Connection string' section")
print()
print("5. You'll see tabs: 'URI', 'JDBC', 'Connection pooling'")
print()
print("6. Click the 'Connection pooling' tab")
print()
print("7. Select 'Transaction' mode (not Session)")
print()
print("8. Copy the string that looks like:")
print("   postgresql://postgres.xxxxx:[YOUR-PASSWORD]@aws-0-us-east-1.pooler.supabase.com:6543/postgres")
print()
print("-" * 60)
print()

connection_string = input("Paste your connection string here (or press Enter to skip): ").strip()

if not connection_string:
    print()
    print("No connection string provided. You can:")
    print("1. Run this script again and paste it when ready")
    print("2. Manually edit backend/.env and add DATABASE_URL")
    print()
    exit(0)

# Validate it looks like a connection string
if not connection_string.startswith("postgresql://"):
    print()
    print("⚠️  Warning: That doesn't look like a PostgreSQL connection string")
    print("   It should start with: postgresql://")
    print()
    confirm = input("Use it anyway? (y/n): ").strip().lower()
    if confirm != 'y':
        exit(0)

# Create/update .env file
import os
from pathlib import Path

env_path = Path("backend/.env")
env_example = Path(".env.example")

if not env_path.exists() and env_example.exists():
    # Copy from example
    with open(env_example, 'r') as f:
        content = f.read()
    with open(env_path, 'w') as f:
        f.write(content)

# Read existing .env or create new
if env_path.exists():
    with open(env_path, 'r') as f:
        lines = f.readlines()
    
    # Update DATABASE_URL if it exists
    updated = False
    new_lines = []
    for line in lines:
        if line.startswith("DATABASE_URL"):
            new_lines.append(f"DATABASE_URL={connection_string}\n")
            updated = True
        else:
            new_lines.append(line)
    
    if not updated:
        new_lines.append(f"\nDATABASE_URL={connection_string}\n")
    
    with open(env_path, 'w') as f:
        f.writelines(new_lines)
else:
    # Create new .env
    with open(env_path, 'w') as f:
        f.write(f"DATABASE_URL={connection_string}\n")
        f.write("SECRET_KEY=your-secret-key-change-in-production\n")
        f.write("CORS_ORIGINS=http://localhost:5173\n")

print()
print("✅ Connection string saved to backend/.env")
print()
print("Next: Run the setup script:")
print("  ./setup.sh")
print()
print("Or manually:")
print("  cd backend")
print("  source venv/bin/activate")
print("  pip install -r requirements.txt")
print("  alembic upgrade head")
print("  python scripts/seed_database.py")

