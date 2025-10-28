"""Compliance tracking API endpoints"""
from fastapi import APIRouter, HTTPException
from typing import List
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "core"))

from database import Database
from app.schemas.compliance import (
    ComplianceRecordRequest,
    ComplianceRecordResponse,
    ComplianceHistoryResponse
)

router = APIRouter()

@router.post("/", response_model=ComplianceRecordResponse)
def record_compliance(request: ComplianceRecordRequest):
    """Record daily compliance"""
    try:
        db = Database()

        compliance_id = db.record_compliance({
            'user_id': request.user_id,
            'protocol_id': request.protocol_id,
            'date': request.date,
            'foods_consumed': request.foods_consumed,
            'adherence_percentage': request.adherence_percentage,
            'missed_foods': request.missed_foods,
            'notes': request.notes
        })

        # Get the record we just created
        history = db.get_compliance_history(request.user_id, days=1)
        db.close()

        if not history:
            raise HTTPException(status_code=500, detail="Failed to create compliance record")

        record = history[0]

        return ComplianceRecordResponse(
            id=record['id'],
            user_id=record['user_id'],
            protocol_id=record['protocol_id'],
            date=record['date'],
            adherence_percentage=record['adherence_percentage'],
            missed_foods=record['missed_foods'],
            notes=record['notes'],
            recorded_at=record['recorded_at']
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history", response_model=List[ComplianceHistoryResponse])
def get_compliance_history(user_id: int = 1, days: int = 30):
    """Get compliance history"""
    try:
        db = Database()
        history = db.get_compliance_history(user_id, days=days)
        db.close()

        return [
            ComplianceHistoryResponse(
                date=record['date'],
                adherence_percentage=record['adherence_percentage'],
                missed_foods=record['missed_foods'],
                notes=record['notes']
            )
            for record in history
        ]

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats")
def get_compliance_stats(user_id: int = 1):
    """Get compliance statistics"""
    try:
        db = Database()
        history = db.get_compliance_history(user_id, days=30)
        db.close()

        if not history:
            return {
                "total_days": 0,
                "average_adherence": 0,
                "current_streak": 0,
                "best_streak": 0
            }

        # Calculate stats
        total_days = len(history)
        average_adherence = sum(r['adherence_percentage'] for r in history) / total_days

        # Calculate current streak (80%+ adherence)
        current_streak = 0
        for record in history:
            if record['adherence_percentage'] >= 80:
                current_streak += 1
            else:
                break

        # Calculate best streak
        best_streak = 0
        temp_streak = 0
        for record in reversed(history):
            if record['adherence_percentage'] >= 80:
                temp_streak += 1
                best_streak = max(best_streak, temp_streak)
            else:
                temp_streak = 0

        return {
            "total_days": total_days,
            "average_adherence": round(average_adherence, 1),
            "current_streak": current_streak,
            "best_streak": best_streak
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
