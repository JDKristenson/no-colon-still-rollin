"""Weight tracking schemas"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class WeightRecordRequest(BaseModel):
    """Request to record weight"""
    user_id: int = Field(default=1)
    weight_lbs: float = Field(..., gt=0, description="Weight in pounds")
    followed_protocol: bool = Field(default=True, description="Naked, morning, before food/water")
    notes: str = Field(default="", max_length=500)

class WeightRecordResponse(BaseModel):
    """Weight record"""
    id: int
    user_id: int
    date: str
    weight_lbs: float
    followed_protocol: bool
    notes: str

class WeightTrendResponse(BaseModel):
    """Weight trend data point"""
    date: str
    weight_lbs: float
    change_from_previous: Optional[float] = None
