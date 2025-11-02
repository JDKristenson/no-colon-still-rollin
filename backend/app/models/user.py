from sqlalchemy import Column, Integer, String, Date, Boolean, JSON, DateTime, Text
from sqlalchemy.sql import func
from app.core.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    date_of_birth = Column(Date)
    
    # Medical
    cancer_type = Column(String)
    diagnosis_date = Column(Date)
    current_treatment = Column(Text)
    oncologist = Column(String)
    
    # Fitness Profile
    height_inches = Column(Integer)
    current_weight_lbs = Column(Integer)
    target_weight_lbs = Column(Integer)
    workout_time_available = Column(Integer, default=30)  # minutes
    equipment_available = Column(JSON, default=list)
    athletic_background = Column(Text)
    
    # Preferences
    protein_minimization_mode = Column(Boolean, default=True)
    coaching_personality = Column(String, default="supportive")
    reminder_preferences = Column(JSON, default=dict)
    
    # Email verification
    email_verified = Column(Boolean, default=False)
    email_verification_token = Column(String, nullable=True, index=True)
    email_verification_sent_at = Column(DateTime(timezone=True), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_active = Column(Boolean, default=True)

