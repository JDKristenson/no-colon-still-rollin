"""Foods database schemas"""
from pydantic import BaseModel
from typing import List, Optional

class ActiveCompound(BaseModel):
    """Active compound in a food"""
    name: str
    amount_per_100g: float
    mechanism: str

class FoodResponse(BaseModel):
    """Food in the database"""
    id: int
    name: str
    common_names: List[str]
    active_compounds: List[ActiveCompound]

    # Nutrition per 100g
    net_carbs_per_100g: float
    protein_per_100g: float
    fat_per_100g: float
    fiber_per_100g: float

    # Cancer-fighting properties
    cancer_types: List[str]
    mechanisms: List[str]

    # Preparation
    best_preparation: str
    preparation_notes: str

    # Safety
    max_daily_amount_grams: float
    side_effects: List[str]
    contraindications: List[str]

    # Evidence
    evidence_level: str
    pubmed_ids: List[str]

class FoodListResponse(BaseModel):
    """List of foods"""
    foods: List[FoodResponse]
    total: int
