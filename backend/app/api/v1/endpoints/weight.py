from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.models.weight import WeightRecord
from app.api.v1.endpoints.auth import get_current_user
from datetime import date, timedelta
from typing import List, Optional
from pydantic import BaseModel

router = APIRouter()

class WeightLogRequest(BaseModel):
    weight_lbs: float
    energy_level: Optional[int] = None
    sleep_quality: Optional[int] = None
    digestion_quality: Optional[int] = None
    overall_feeling: Optional[int] = None
    notes: Optional[str] = None
    followed_protocol: Optional[bool] = None

@router.get("/history")
async def get_weight_history(
    limit: int = 90,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get weight history"""
    records = db.query(WeightRecord).filter(
        WeightRecord.user_id == current_user.id
    ).order_by(WeightRecord.date.desc()).limit(limit).all()
    
    return [
        {
            "id": r.id,
            "date": r.date.isoformat(),
            "weight_lbs": r.weight_lbs,
            "energy_level": r.energy_level,
            "sleep_quality": r.sleep_quality,
            "digestion_quality": r.digestion_quality,
            "overall_feeling": r.overall_feeling,
            "notes": r.notes,
            "followed_protocol": r.followed_protocol,
        }
        for r in records
    ]

@router.post("/log")
async def log_weight(
    weight_data: WeightLogRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Log weight and health metrics"""
    today = date.today()
    
    # Check if record already exists for today
    existing = db.query(WeightRecord).filter(
        WeightRecord.user_id == current_user.id,
        WeightRecord.date == today
    ).first()
    
    if existing:
        # Update existing record
        existing.weight_lbs = weight_data.weight_lbs
        existing.energy_level = weight_data.energy_level
        existing.sleep_quality = weight_data.sleep_quality
        existing.digestion_quality = weight_data.digestion_quality
        existing.overall_feeling = weight_data.overall_feeling
        existing.notes = weight_data.notes
        existing.followed_protocol = weight_data.followed_protocol
        db.commit()
        db.refresh(existing)
        record = existing
    else:
        # Create new record
        record = WeightRecord(
            user_id=current_user.id,
            date=today,
            weight_lbs=weight_data.weight_lbs,
            energy_level=weight_data.energy_level,
            sleep_quality=weight_data.sleep_quality,
            digestion_quality=weight_data.digestion_quality,
            overall_feeling=weight_data.overall_feeling,
            notes=weight_data.notes,
            followed_protocol=weight_data.followed_protocol,
        )
        db.add(record)
        db.commit()
        db.refresh(record)
    
    # Update user's current weight
    current_user.current_weight_lbs = int(weight_data.weight_lbs)
    db.commit()
    
    return {
        "id": record.id,
        "message": "Weight logged successfully",
        "date": record.date.isoformat(),
        "weight_lbs": record.weight_lbs,
    }

@router.get("/trend")
async def get_weight_trend(
    days: int = 30,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get weight trend data for charting"""
    end_date = date.today()
    start_date = end_date - timedelta(days=days)
    
    records = db.query(WeightRecord).filter(
        WeightRecord.user_id == current_user.id,
        WeightRecord.date >= start_date,
        WeightRecord.date <= end_date
    ).order_by(WeightRecord.date.asc()).all()
    
    if not records:
        return {
            "dates": [],
            "weights": [],
            "trend": "no_data",
            "change_lbs": 0,
        }
    
    dates = [r.date.isoformat() for r in records]
    weights = [r.weight_lbs for r in records]
    
    # Calculate trend
    first_weight = weights[0]
    last_weight = weights[-1]
    change_lbs = last_weight - first_weight
    
    if change_lbs > 2:
        trend = "increasing"
    elif change_lbs < -2:
        trend = "decreasing"
    else:
        trend = "stable"
    
    return {
        "dates": dates,
        "weights": weights,
        "trend": trend,
        "change_lbs": round(change_lbs, 1),
        "first_weight": first_weight,
        "last_weight": last_weight,
    }

