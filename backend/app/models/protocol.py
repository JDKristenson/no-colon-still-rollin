from sqlalchemy import Column, Integer, String, Float, Date, JSON, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class DailyProtocol(Base):
    __tablename__ = "daily_protocols"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(Date, nullable=False, index=True)
    weight_lbs = Column(Float)
    
    foods = Column(JSON)  # Array of ProtocolFood data
    
    # Macros
    total_net_carbs = Column(Float)
    total_protein = Column(Float)
    total_fat = Column(Float)
    total_calories = Column(Float)
    
    # Protein adjusted for glutamine competition
    protein_target = Column(Float)
    protein_reasoning = Column(Text)
    
    # Keto check
    keto_compatible = Column(Boolean)
    keto_score = Column(Float)  # 0-100
    
    # Glutamine
    estimated_glutamine_competition_score = Column(Float)
    
    generated_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", backref="protocols")

