from pydantic import BaseModel
from typing import Optional, Dict

class DashboardResponse(BaseModel):
    user: Dict
    nutrition: Dict
    workout: Dict
    soreness: Dict
    metrics: Dict
    date: str

