"""Status and dashboard schemas"""
from pydantic import BaseModel
from typing import Optional, List

class WeightSummary(BaseModel):
    """Weight summary"""
    current_weight_lbs: float
    target_weight_lbs: Optional[float]
    recent_change_lbs: Optional[float]
    trend: str  # "up", "down", "stable"

class ComplianceSummary(BaseModel):
    """Compliance summary"""
    current_streak_days: int
    average_adherence_7day: float
    average_adherence_30day: float
    total_days_tracked: int

class UserStatusResponse(BaseModel):
    """Complete user status"""
    user_id: int
    name: str
    cancer_type: str

    # Weight
    weight: WeightSummary

    # Compliance
    compliance: ComplianceSummary

    # System stats
    total_foods_in_database: int
    total_research_studies: int
