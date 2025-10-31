from sqlalchemy import Column, Integer, String, Float, Text, JSON, ARRAY
from app.core.database import Base

class Food(Base):
    __tablename__ = "foods"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    active_compounds = Column(JSON)
    
    # Nutritional data per 100g
    net_carbs_per_100g = Column(Float)
    protein_per_100g = Column(Float)
    fat_per_100g = Column(Float)
    fiber_per_100g = Column(Float)
    
    # Cancer-fighting properties
    cancer_types = Column(ARRAY(String))
    mechanisms = Column(ARRAY(String))
    evidence_level = Column(String)  # "strong", "moderate", "preliminary"
    
    # Dosing information
    min_daily_amount_grams = Column(Float)
    max_daily_amount_grams = Column(Float)
    recommended_amount_grams = Column(Float)
    
    # Safety and interactions
    contraindications = Column(Text)
    food_drug_interactions = Column(JSON)

