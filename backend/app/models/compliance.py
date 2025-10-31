from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Boolean, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class ComplianceRecord(Base):
    __tablename__ = "compliance_records"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(Date, nullable=False, index=True)
    
    # Nutrition
    nutrition_foods_consumed = Column(String)  # JSON array of food names
    nutrition_adherence_percentage = Column(Float)
    
    # Workout
    workout_completed = Column(Boolean, default=False)
    workout_duration_minutes = Column(Integer)
    
    # Combined
    combined_adherence_score = Column(Float)
    is_perfect_day = Column(Boolean, default=False)
    
    # Streak
    current_streak_days = Column(Integer, default=0)
    
    # Glutamine
    glutamine_competition_score = Column(Float)
    
    recorded_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", backref="compliance_records")

