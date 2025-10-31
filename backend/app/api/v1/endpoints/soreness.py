from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.core.database import get_db
from app.models.user import User
from app.models.soreness import SorenessRecord
from app.models.compliance import ComplianceRecord
from app.api.v1.endpoints.auth import get_current_user
from app.algorithms.workout_rotation import get_current_soreness_state
from app.algorithms.glutamine import calculate_glutamine_score
from datetime import date, timedelta
from typing import Dict
from pydantic import BaseModel

router = APIRouter()

class SorenessLogRequest(BaseModel):
    muscle_group: str
    intensity: int
    notes: str = ""

@router.get("/current")
async def get_current_soreness(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current soreness state for all muscle groups"""
    soreness_state = get_current_soreness_state(current_user.id, db)
    
    # Calculate coverage percentage
    sore_count = sum(1 for intensity in soreness_state.values() if intensity >= 5)
    coverage_percentage = (sore_count / 6) * 100
    
    # Calculate glutamine competition score
    glutamine_score = calculate_glutamine_score(current_user.id, db)
    
    # Check for gaps
    gap_warning = sore_count == 0
    
    # Build detailed state
    muscle_groups_detail = []
    for muscle_group in ["chest", "back", "shoulders", "legs", "core", "arms"]:
        intensity = soreness_state.get(muscle_group, 0)
        
        # Get recent record for more details
        record = db.query(SorenessRecord).filter(
            and_(
                SorenessRecord.user_id == current_user.id,
                SorenessRecord.muscle_group == muscle_group,
                SorenessRecord.date == date.today()
            )
        ).order_by(SorenessRecord.logged_at.desc()).first()
        
        days_sore = 0
        if record and record.onset_date:
            days_sore = (date.today() - record.onset_date).days
        
        status = "active" if intensity >= 5 else "fading" if intensity > 0 else "recovered"
        
        muscle_groups_detail.append({
            "name": muscle_group,
            "intensity": intensity,
            "days_sore": days_sore,
            "status": status,
        })
    
    return {
        "muscle_groups": {
            mg["name"]: mg["intensity"]
            for mg in muscle_groups_detail
        },
        "coverage_percentage": round(coverage_percentage, 1),
        "glutamine_competition_score": round(glutamine_score, 1),
        "gap_warning": gap_warning,
        "detailed_state": muscle_groups_detail,
    }

@router.post("/log")
async def log_soreness(
    soreness_data: SorenessLogRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Log muscle soreness for a specific muscle group"""
    today = date.today()
    
    # Check if record already exists for today
    existing = db.query(SorenessRecord).filter(
        and_(
            SorenessRecord.user_id == current_user.id,
            SorenessRecord.muscle_group == soreness_data.muscle_group,
            SorenessRecord.date == today
        )
    ).first()
    
    if existing:
        # Update existing record
        existing.soreness_intensity = soreness_data.intensity
        existing.notes = soreness_data.notes
        if soreness_data.intensity > 0 and not existing.onset_date:
            existing.onset_date = today
        
        # Predict recovery date
        from app.algorithms.workout_rotation import predict_soreness_duration
        duration_hours = predict_soreness_duration(
            current_user.id,
            soreness_data.muscle_group,
            soreness_data.intensity,
            db
        )
        existing.expected_recovery_date = today + timedelta(hours=duration_hours)
        
        db.commit()
        db.refresh(existing)
        record = existing
    else:
        # Create new record
        from app.algorithms.workout_rotation import predict_soreness_duration
        duration_hours = predict_soreness_duration(
            current_user.id,
            soreness_data.muscle_group,
            soreness_data.intensity,
            db
        )
        
        record = SorenessRecord(
            user_id=current_user.id,
            muscle_group=soreness_data.muscle_group,
            date=today,
            soreness_intensity=soreness_data.intensity,
            onset_date=today if soreness_data.intensity > 0 else None,
            expected_recovery_date=today + timedelta(hours=duration_hours) if soreness_data.intensity > 0 else None,
            notes=soreness_data.notes,
        )
        db.add(record)
        db.commit()
        db.refresh(record)
    
    # Update compliance record glutamine score
    compliance = db.query(ComplianceRecord).filter(
        and_(
            ComplianceRecord.user_id == current_user.id,
            ComplianceRecord.date == today
        )
    ).first()
    
    if compliance:
        glutamine_score = calculate_glutamine_score(current_user.id, db)
        compliance.glutamine_competition_score = glutamine_score
        db.commit()
    
    return {
        "message": "Soreness logged successfully",
        "muscle_group": soreness_data.muscle_group,
        "intensity": soreness_data.intensity,
        "expected_recovery_date": record.expected_recovery_date.isoformat() if record.expected_recovery_date else None,
    }

@router.get("/competition-score")
async def get_competition_score(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current glutamine competition score"""
    score = calculate_glutamine_score(current_user.id, db)
    soreness_state = get_current_soreness_state(current_user.id, db)
    
    sore_count = sum(1 for intensity in soreness_state.values() if intensity >= 5)
    coverage_percentage = (sore_count / 6) * 100
    
    return {
        "glutamine_competition_score": round(score, 1),
        "coverage_percentage": round(coverage_percentage, 1),
        "sore_muscle_groups_count": sore_count,
        "total_muscle_groups": 6,
    }

@router.get("/coverage-warning")
async def get_coverage_warning(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Check if there's a gap in soreness coverage"""
    soreness_state = get_current_soreness_state(current_user.id, db)
    
    sore_count = sum(1 for intensity in soreness_state.values() if intensity >= 5)
    
    if sore_count == 0:
        return {
            "warning": True,
            "message": "⚠️ No muscle groups are currently sore. Train immediately to maintain glutamine competition!",
            "severity": "high",
            "recommended_action": "Generate and complete a workout today targeting recovered muscle groups.",
        }
    elif sore_count == 1:
        return {
            "warning": True,
            "message": "⚠️ Only one muscle group is sore. Consider training additional groups soon.",
            "severity": "medium",
            "recommended_action": "Train one more muscle group within 24 hours to maintain coverage.",
        }
    else:
        return {
            "warning": False,
            "message": "✓ Good soreness coverage maintained.",
            "severity": "none",
            "recommended_action": None,
        }
