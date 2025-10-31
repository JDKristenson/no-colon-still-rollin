#!/usr/bin/env python3
"""
Construct Supabase connection string from known information
"""
import re

print("=" * 60)
print("🔧 Construct Supabase Connection String")
print("=" * 60)
print()
print("Since the connection string section isn't visible, let's build it manually.")
print()

# Project reference is known
project_ref = "wpyntnmjncdizglqedyl"

print(f"✅ Project Reference: {project_ref}")
print()

# Get password
print("What's your Supabase database password?")
print("(The one you set when creating the project)")
password = input("Password: ").strip()

if not password:
    print("❌ Password required. Exiting.")
    exit(1)

# Try common regions
regions = [
    ("us-east-1", "US East (N. Virginia)"),
    ("us-west-1", "US West (N. California)"),
    ("eu-west-1", "EU West (Ireland)"),
    ("ap-southeast-1", "Asia Pacific (Singapore)"),
    ("ap-northeast-1", "Asia Pacific (Tokyo)"),
]

print()
print("What region is your project in?")
for i, (code, name) in enumerate(regions, 1):
    print(f"  {i}. {name} ({code})")
print("  Or type the region code directly")
print()

region_choice = input("Region [1-5 or code]: ").strip()

if region_choice.isdigit() and 1 <= int(region_choice) <= len(regions):
    region = regions[int(region_choice) - 1][0]
else:
    region = region_choice if region_choice else "us-east-1"

print()
print(f"✅ Using region: {region}")
print()

# Construct connection strings
direct_conn = f"postgresql://postgres.{project_ref}:{password}@db.{project_ref}.supabase.co:5432/postgres"
pooler_conn = f"postgresql://postgres.{project_ref}:{password}@aws-0-{region}.pooler.supabase.com:6543/postgres"

print("=" * 60)
print("📋 Connection Strings Generated:")
print("=" * 60)
print()
print("TRANSACTION POOLER (Recommended for serverless):")
print(pooler_conn)
print()
print("DIRECT CONNECTION:")
print(direct_conn)
print()

# Save to .env
import os
from pathlib import Path

env_path = Path("backend/.env")
env_example = Path(".env.example")

if not env_path.exists() and env_example.exists():
    with open(env_example, 'r') as f:
        content = f.read()
    with open(env_path, 'w') as f:
        f.write(content)

# Read and update .env
if env_path.exists():
    with open(env_path, 'r') as f:
        lines = f.readlines()
    
    updated = False
    new_lines = []
    for line in lines:
        if line.startswith("DATABASE_URL"):
            new_lines.append(f"DATABASE_URL={pooler_conn}\n")
            updated = True
        else:
            new_lines.append(line)
    
    if not updated:
        new_lines.append(f"\nDATABASE_URL={pooler_conn}\n")
    
    with open(env_path, 'w') as f:
        f.writelines(new_lines)
else:
    with open(env_path, 'w') as f:
        f.write(f"DATABASE_URL={pooler_conn}\n")
        f.write("SECRET_KEY=your-secret-key-change-in-production\n")
        f.write("CORS_ORIGINS=http://localhost:5173\n")

print("✅ Saved Transaction Pooler connection to backend/.env")
print()

# Test connection
print("🧪 Testing connection...")
print()

try:
    import sys
    sys.path.insert(0, 'backend')
    from app.core.database import engine
    
    conn = engine.connect()
    print("✅ Connection successful!")
    conn.close()
    print()
    print("Ready to run migrations!")
    print()
    print("Next steps:")
    print("  cd backend")
    print("  source venv/bin/activate")
    print("  alembic upgrade head")
    print("  python scripts/seed_database.py")
except ImportError:
    print("⚠️  Can't test yet - need to install dependencies first")
    print("Run: cd backend && pip install -r requirements.txt")
except Exception as e:
    print(f"⚠️  Connection test failed: {e}")
    print()
    print("This might mean:")
    print("  1. Wrong password")
    print("  2. Wrong region")
    print("  3. Need to install dependencies")
    print()
    print("Try the DIRECT connection instead:")
    print(f"  DATABASE_URL={direct_conn}")

