"""Weight tracking API endpoints"""
from fastapi import APIRouter, HTTPException
from typing import List
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "core"))

from database import Database
from app.schemas.weight import (
    WeightRecordRequest,
    WeightRecordResponse,
    WeightTrendResponse
)

router = APIRouter()

@router.post("/", response_model=WeightRecordResponse)
def record_weight(request: WeightRecordRequest):
    """Record a weight measurement"""
    try:
        db = Database()

        # Add weight record
        db.add_weight_record(
            user_id=request.user_id,
            weight_lbs=request.weight_lbs,
            followed_protocol=request.followed_protocol,
            notes=request.notes
        )

        # Get the record we just created
        history = db.get_weight_history(request.user_id, limit=1)
        db.close()

        if not history:
            raise HTTPException(status_code=500, detail="Failed to create weight record")

        record = history[0]

        return WeightRecordResponse(
            id=record['id'],
            user_id=record['user_id'],
            date=record['date'],
            weight_lbs=record['weight_lbs'],
            followed_protocol=record['followed_protocol'],
            notes=record['notes']
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history", response_model=List[WeightTrendResponse])
def get_weight_history(user_id: int = 1, limit: int = 52):
    """Get weight history (default: last 52 weeks)"""
    try:
        db = Database()
        history = db.get_weight_history(user_id, limit=limit)
        db.close()

        if not history:
            return []

        # Calculate changes
        trends = []
        prev_weight = None

        for record in reversed(history):  # Oldest first
            change = None
            if prev_weight is not None:
                change = record['weight_lbs'] - prev_weight

            trends.append(WeightTrendResponse(
                date=record['date'],
                weight_lbs=record['weight_lbs'],
                change_from_previous=change
            ))

            prev_weight = record['weight_lbs']

        return list(reversed(trends))  # Most recent first

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
