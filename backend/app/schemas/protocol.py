"""Protocol API schemas"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date

class ProtocolFoodResponse(BaseModel):
    """A food in the daily protocol"""
    name: str
    amount_grams: float
    servings_per_day: int
    grams_per_serving: float
    timing: str
    timing_notes: str
    preparation: str
    preparation_notes: str

    # Macros
    net_carbs: float
    protein: float
    fat: float

    # Why this food
    reason: str
    mechanisms: List[str]
    safety_notes: str

class DailyProtocolResponse(BaseModel):
    """Complete daily protocol"""
    date: str
    user_id: int
    weight_lbs: float

    # Foods
    foods: List[ProtocolFoodResponse]

    # Totals
    total_net_carbs: float
    total_protein: float
    total_fat: float
    total_calories: float

    # Keto compatibility
    keto_compatible: bool
    keto_score: float

class GenerateProtocolRequest(BaseModel):
    """Request to generate a new protocol"""
    user_id: int = Field(default=1, description="User ID (default: Jesse Mills)")
    weight_lbs: Optional[float] = Field(None, description="Current weight in pounds")
    target_date: Optional[str] = Field(None, description="Date for protocol (YYYY-MM-DD)")
