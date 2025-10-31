#!/usr/bin/env python3
"""
Seed database with initial data
"""
import sys
import os
import json
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine
from app.models import *
from app.core.security import get_password_hash

def seed_foods(db: Session):
    """Seed foods from JSON file"""
    seed_path = Path(__file__).parent.parent.parent / "database" / "seeds" / "foods.json"
    
    if not seed_path.exists():
        print(f"Foods seed file not found at {seed_path}")
        return
    
    with open(seed_path, 'r') as f:
        foods_data = json.load(f)
    
    for food_data in foods_data:
        existing = db.query(Food).filter(Food.name == food_data["name"]).first()
        if not existing:
            food = Food(**food_data)
            db.add(food)
            print(f"Added food: {food.name}")
        else:
            print(f"Food already exists: {food_data['name']}")
    
    db.commit()

def seed_muscle_groups(db: Session):
    """Seed muscle groups"""
    seed_path = Path(__file__).parent.parent.parent / "database" / "seeds" / "muscle_groups.json"
    
    if not seed_path.exists():
        print(f"Muscle groups seed file not found at {seed_path}")
        return
    
    with open(seed_path, 'r') as f:
        groups_data = json.load(f)
    
    for group_data in groups_data:
        existing = db.query(MuscleGroup).filter(MuscleGroup.name == group_data["name"]).first()
        if not existing:
            group = MuscleGroup(**group_data)
            db.add(group)
            print(f"Added muscle group: {group.name}")
    
    db.commit()

def seed_exercises(db: Session):
    """Seed exercises from JSON file"""
    seed_path = Path(__file__).parent.parent.parent / "database" / "seeds" / "exercises.json"
    
    if not seed_path.exists():
        print(f"Exercises seed file not found at {seed_path}")
        return
    
    with open(seed_path, 'r') as f:
        exercises_data = json.load(f)
    
    for ex_data in exercises_data:
        existing = db.query(Exercise).filter(Exercise.name == ex_data["name"]).first()
        if not existing:
            exercise = Exercise(**ex_data)
            db.add(exercise)
            print(f"Added exercise: {exercise.name}")
    
    db.commit()

def seed_admin_user(db: Session):
    """Seed admin/test user"""
    email = "jesse@example.com"
    existing = db.query(User).filter(User.email == email).first()
    
    if not existing:
        user = User(
            email=email,
            hashed_password=get_password_hash("password123"),
            name="Jesse Mills",
            date_of_birth=None,
            cancer_type="colon",
            height_inches=71,  # 5'11"
            current_weight_lbs=180,
            workout_time_available=45,
            equipment_available=["treadmill", "stationary_bike", "dumbbells", "bench"],
            athletic_background="Elite athlete (baseball, Boston Marathon)",
        )
        db.add(user)
        db.commit()
        print(f"Created user: {user.email}")
    else:
        print(f"User already exists: {email}")

def main():
    """Run all seeding functions"""
    print("Starting database seeding...")
    
    # Create tables
    from app.models import Base
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        seed_muscle_groups(db)
        seed_foods(db)
        seed_exercises(db)
        seed_admin_user(db)
        print("\n✅ Database seeding completed!")
    except Exception as e:
        print(f"\n❌ Error seeding database: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    main()

