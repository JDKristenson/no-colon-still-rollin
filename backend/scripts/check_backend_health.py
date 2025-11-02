#!/usr/bin/env python3
"""Check backend health and diagnose common issues"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def check_imports():
    """Check if all critical imports work"""
    print("Checking imports...")
    try:
        from app.models.genetic_marker import GeneticMarker, CTDNATestResult, DetectedMarker
        print("  ✅ Genetic marker models")
    except Exception as e:
        print(f"  ❌ Genetic marker models: {e}")
        return False
    
    try:
        from app.core.signatera_parser import parse_signatera_excel
        print("  ✅ Signatera parser")
    except Exception as e:
        print(f"  ❌ Signatera parser: {e}")
        return False
    
    try:
        from app.api.v1.endpoints import genetics
        print("  ✅ Genetics endpoint")
    except Exception as e:
        print(f"  ❌ Genetics endpoint: {e}")
        return False
    
    try:
        from app.api.v1.api import api_router
        print("  ✅ API router")
    except Exception as e:
        print(f"  ❌ API router: {e}")
        return False
    
    try:
        from app.main import app
        print("  ✅ FastAPI app")
    except Exception as e:
        print(f"  ❌ FastAPI app: {e}")
        return False
    
    return True

def check_database_tables():
    """Check if database tables exist"""
    print("\nChecking database tables...")
    try:
        from app.core.database import engine
        from sqlalchemy import inspect
        
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        required_tables = [
            'genetic_markers',
            'ctdna_test_results', 
            'detected_markers',
            'users',
            'foods',
            'daily_protocols'
        ]
        
        for table in required_tables:
            if table in tables:
                print(f"  ✅ {table}")
            else:
                print(f"  ❌ {table} - MISSING")
                return False
        
        return True
    except Exception as e:
        print(f"  ❌ Database check failed: {e}")
        return False

def check_config():
    """Check configuration"""
    print("\nChecking configuration...")
    try:
        from app.core.config import settings
        
        print(f"  Database URL: {'✅ Set' if settings.DATABASE_URL else '❌ Missing'}")
        print(f"  Secret Key: {'✅ Set' if settings.SECRET_KEY != 'your-secret-key-change-in-production' else '⚠️  Default'}")
        print(f"  CORS Origins: {settings.CORS_ORIGINS}")
        
        cors_origins = settings.get_cors_origins()
        print(f"  Parsed CORS: {cors_origins}")
        
        if "*" in cors_origins:
            print("  ✅ CORS allows all origins")
        else:
            print(f"  ⚠️  CORS restricted to: {cors_origins}")
        
        return True
    except Exception as e:
        print(f"  ❌ Config check failed: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Backend Health Check\n")
    print("=" * 50)
    
    all_ok = True
    all_ok &= check_imports()
    all_ok &= check_config()
    all_ok &= check_database_tables()
    
    print("\n" + "=" * 50)
    if all_ok:
        print("✅ All checks passed!")
        sys.exit(0)
    else:
        print("❌ Some checks failed - see errors above")
        sys.exit(1)

