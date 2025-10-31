from sqlalchemy import Column, Integer, String, Float, Date, DateTime, JSON, Boolean, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class MuscleGroup(Base):
    __tablename__ = "muscle_groups"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    recovery_time_hours = Column(Integer, default=48)
    description = Column(Text)

class Exercise(Base):
    __tablename__ = "exercises"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    
    muscle_group_primary = Column(String, nullable=False)
    muscle_groups_secondary = Column(JSON, default=list)
    
    equipment_required = Column(JSON, default=list)
    difficulty_level = Column(Integer, default=3)  # 1-5
    is_baseball_specific = Column(Boolean, default=False)
    
    form_cues = Column(JSON, default=list)
    video_url = Column(String)
    
    # Sets/Reps defaults
    default_sets = Column(Integer)
    default_reps = Column(Integer)
    default_duration_seconds = Column(Integer)  # For timed exercises
    default_weight_lbs = Column(Float)

class WorkoutPlan(Base):
    __tablename__ = "workout_plans"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(Date, nullable=False, index=True)
    
    workout_type = Column(String)  # "strength", "cardio", "recovery", "mixed"
    target_muscle_groups = Column(JSON, default=list)
    
    exercises = Column(JSON)  # Array of exercise data with sets/reps/weight
    
    estimated_duration_minutes = Column(Integer)
    
    # Coaching
    coaching_message = Column(Text)
    weekly_focus = Column(Text)
    
    # Soreness goals
    soreness_maintenance_goals = Column(JSON)
    
    generated_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", backref="workout_plans")

class WorkoutLog(Base):
    __tablename__ = "workout_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    workout_plan_id = Column(Integer, ForeignKey("workout_plans.id"))
    date = Column(Date, nullable=False, index=True)
    time = Column(DateTime(timezone=True))
    
    completed = Column(Boolean, default=False)
    actual_duration_minutes = Column(Integer)
    
    exercises_completed = Column(JSON)  # Array of logged exercise data
    
    perceived_exertion = Column(Integer)  # RPE 1-10
    
    post_workout_soreness_prediction = Column(JSON)
    
    notes = Column(Text)
    
    logged_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", backref="workout_logs")

