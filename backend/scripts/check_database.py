#!/usr/bin/env python3
"""Check database connection and tables"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine, inspect, text
from app.core.config import settings

def check_database():
    print("🔍 Checking database connection...")
    print(f"Database URL: {settings.DATABASE_URL[:50]}...")  # Show first 50 chars
    
    try:
        engine = create_engine(settings.DATABASE_URL)
        with engine.connect() as conn:
            # Test connection
            result = conn.execute(text("SELECT 1"))
            print("✅ Database connection successful!")
            
            # Check if tables exist
            inspector = inspect(engine)
            tables = inspector.get_table_names()
            print(f"\n📊 Found {len(tables)} tables:")
            for table in tables:
                print(f"  - {table}")
            
            # Check users table specifically
            if 'users' in tables:
                print("\n✅ 'users' table exists!")
                # Check if table has data
                result = conn.execute(text("SELECT COUNT(*) FROM users"))
                count = result.scalar()
                print(f"   Users in database: {count}")
            else:
                print("\n❌ 'users' table does NOT exist!")
                print("   Run migrations: alembic upgrade head")
                return False
                
            return True
            
    except Exception as e:
        print(f"\n❌ Database error: {e}")
        return False

if __name__ == "__main__":
    success = check_database()
    sys.exit(0 if success else 1)

