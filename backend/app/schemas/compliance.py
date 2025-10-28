"""Compliance tracking schemas"""
from pydantic import BaseModel, Field
from typing import List, Dict, Any
from datetime import datetime

class FoodConsumed(BaseModel):
    """Food that was consumed"""
    food: str
    expected_grams: float
    actual_grams: float
    percentage: float

class ComplianceRecordRequest(BaseModel):
    """Request to record compliance"""
    user_id: int = Field(default=1)
    protocol_id: int
    date: str
    foods_consumed: List[Dict[str, Any]]
    adherence_percentage: float = Field(..., ge=0, le=100)
    missed_foods: List[str]
    notes: str = Field(default="", max_length=1000)

class ComplianceRecordResponse(BaseModel):
    """Compliance record"""
    id: int
    user_id: int
    protocol_id: int
    date: str
    adherence_percentage: float
    missed_foods: List[str]
    notes: str
    recorded_at: str

class ComplianceHistoryResponse(BaseModel):
    """Compliance history summary"""
    date: str
    adherence_percentage: float
    missed_foods: List[str]
    notes: str
