from sqlalchemy import Column, Integer, Float, Date, DateTime, Integer as Int, ForeignKey, Text, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class WeightRecord(Base):
    __tablename__ = "weight_records"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(Date, nullable=False, index=True)
    weight_lbs = Column(Float, nullable=False)
    
    # Health metrics
    energy_level = Column(Int)  # 1-10
    sleep_quality = Column(Int)  # 1-10
    digestion_quality = Column(Int)  # 1-10
    overall_feeling = Column(Int)  # 1-10
    
    notes = Column(Text)
    followed_protocol = Column(Boolean)
    
    recorded_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", backref="weight_records")

