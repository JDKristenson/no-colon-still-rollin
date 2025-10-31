from sqlalchemy import Column, Integer, String, Float, Date, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class SorenessRecord(Base):
    __tablename__ = "soreness_records"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    muscle_group = Column(String, nullable=False, index=True)  # "chest", "back", etc.
    date = Column(Date, nullable=False, index=True)
    
    soreness_intensity = Column(Integer, nullable=False)  # 0-10
    
    onset_date = Column(Date)
    expected_recovery_date = Column(Date)
    
    source_workout_id = Column(Integer, ForeignKey("workout_logs.id"))
    
    notes = Column(Text)
    
    logged_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", backref="soreness_records")

