#!/usr/bin/env python3
"""
Deploy migrations to production database
Use this script after deploying backend to ensure migrations are run
"""
import sys
import os
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

from app.core.config import settings
from app.core.database import engine, Base
from app.models import *
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """Create all tables from models"""
    logger.info("Creating database tables...")
    logger.info(f"Database URL: {settings.DATABASE_URL.split('@')[1] if '@' in settings.DATABASE_URL else 'local'}")
    
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Tables created successfully!")
        
        # Also seed data if needed
        import importlib.util
        seed_path = Path(__file__).parent / "seed_database.py"
        if seed_path.exists():
            spec = importlib.util.spec_from_file_location("seed_database", seed_path)
            seed_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(seed_module)
            
            logger.info("Seeding database...")
            from sqlalchemy.orm import Session
            from app.core.database import SessionLocal
            
            db = SessionLocal()
            try:
                seed_module.seed_muscle_groups(db)
                seed_module.seed_foods(db)
                seed_module.seed_exercises(db)
                logger.info("✅ Database seeded!")
            finally:
                db.close()
        else:
            logger.warning("Seed script not found, skipping seeding")
            
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

