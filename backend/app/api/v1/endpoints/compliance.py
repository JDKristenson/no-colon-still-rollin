from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from app.core.database import get_db
from app.models.user import User
from app.models.compliance import ComplianceRecord
from app.models.protocol import DailyProtocol
from app.models.workout import WorkoutLog
from app.api.v1.endpoints.auth import get_current_user
from app.algorithms.glutamine import calculate_glutamine_score
from datetime import date, timedelta
from typing import List
from pydantic import BaseModel

router = APIRouter()

class NutritionComplianceRequest(BaseModel):
    foods_consumed: List[str]  # List of food names

class WorkoutComplianceRequest(BaseModel):
    completed: bool
    duration_minutes: int = 0

@router.get("/stats")
async def get_compliance_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get compliance statistics"""
    today = date.today()
    seven_days_ago = today - timedelta(days=7)
    
    # Get last 7 days of compliance
    records = db.query(ComplianceRecord).filter(
        and_(
            ComplianceRecord.user_id == current_user.id,
            ComplianceRecord.date >= seven_days_ago,
            ComplianceRecord.date <= today
        )
    ).order_by(ComplianceRecord.date.desc()).all()
    
    if not records:
        return {
            "nutrition_adherence": 0,
            "workout_adherence": 0,
            "combined_adherence": 0,
            "current_streak": 0,
            "7_day_nutrition_avg": 0,
            "7_day_workout_avg": 0,
        }
    
    # Calculate averages
    nutrition_scores = [r.nutrition_adherence_percentage or 0 for r in records]
    workout_scores = [100 if r.workout_completed else 0 for r in records]
    
    nutrition_avg = sum(nutrition_scores) / len(nutrition_scores) if nutrition_scores else 0
    workout_avg = sum(workout_scores) / len(workout_scores) if workout_scores else 0
    
    # Get current streak
    current_streak = 0
    for i in range(len(records)):
        if records[i].combined_adherence_score and records[i].combined_adherence_score >= 90:
            current_streak += 1
        else:
            break
    
    # Today's compliance
    today_record = next((r for r in records if r.date == today), None)
    
    return {
        "nutrition_adherence": today_record.nutrition_adherence_percentage if today_record else 0,
        "workout_adherence": 100 if (today_record and today_record.workout_completed) else 0,
        "combined_adherence": today_record.combined_adherence_score if today_record else 0,
        "current_streak": current_streak,
        "7_day_nutrition_avg": round(nutrition_avg, 1),
        "7_day_workout_avg": round(workout_avg, 1),
        "7_day_combined_avg": round((nutrition_avg + workout_avg) / 2, 1),
    }

@router.post("/nutrition")
async def log_nutrition_compliance(
    compliance_data: NutritionComplianceRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Log nutrition compliance"""
    today = date.today()
    
    # Get today's protocol
    protocol = db.query(DailyProtocol).filter(
        and_(
            DailyProtocol.user_id == current_user.id,
            DailyProtocol.date == today
        )
    ).first()
    
    if not protocol:
        return {"error": "No protocol found for today. Generate protocol first."}
    
    # Calculate adherence
    total_foods = len(protocol.foods) if protocol.foods else 9
    consumed_count = len(compliance_data.foods_consumed)
    adherence_percentage = (consumed_count / total_foods) * 100 if total_foods > 0 else 0
    
    # Get or create compliance record
    compliance = db.query(ComplianceRecord).filter(
        and_(
            ComplianceRecord.user_id == current_user.id,
            ComplianceRecord.date == today
        )
    ).first()
    
    if not compliance:
        compliance = ComplianceRecord(
            user_id=current_user.id,
            date=today,
            nutrition_foods_consumed=str(compliance_data.foods_consumed),
            nutrition_adherence_percentage=adherence_percentage,
        )
        db.add(compliance)
    else:
        compliance.nutrition_foods_consumed = str(compliance_data.foods_consumed)
        compliance.nutrition_adherence_percentage = adherence_percentage
    
    # Update combined adherence
    workout_completed = compliance.workout_completed or False
    combined_score = (adherence_percentage + (100 if workout_completed else 0)) / 2
    compliance.combined_adherence_score = combined_score
    compliance.is_perfect_day = adherence_percentage >= 100 and workout_completed
    
    # Calculate streak
    yesterday = today - timedelta(days=1)
    yesterday_compliance = db.query(ComplianceRecord).filter(
        and_(
            ComplianceRecord.user_id == current_user.id,
            ComplianceRecord.date == yesterday
        )
    ).first()
    
    if yesterday_compliance and yesterday_compliance.combined_adherence_score >= 90:
        compliance.current_streak_days = (yesterday_compliance.current_streak_days or 0) + 1
    elif compliance.combined_adherence_score >= 90:
        compliance.current_streak_days = 1
    else:
        compliance.current_streak_days = 0
    
    # Update glutamine score
    compliance.glutamine_competition_score = calculate_glutamine_score(current_user.id, db)
    
    db.commit()
    db.refresh(compliance)
    
    return {
        "message": "Nutrition compliance logged",
        "adherence_percentage": round(adherence_percentage, 1),
        "combined_adherence": round(combined_score, 1),
        "current_streak": compliance.current_streak_days,
    }

@router.post("/workout")
async def log_workout_compliance(
    compliance_data: WorkoutComplianceRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Log workout compliance"""
    today = date.today()
    
    # Get or create compliance record
    compliance = db.query(ComplianceRecord).filter(
        and_(
            ComplianceRecord.user_id == current_user.id,
            ComplianceRecord.date == today
        )
    ).first()
    
    if not compliance:
        compliance = ComplianceRecord(
            user_id=current_user.id,
            date=today,
            nutrition_adherence_percentage=0,
        )
        db.add(compliance)
    
    compliance.workout_completed = compliance_data.completed
    compliance.workout_duration_minutes = compliance_data.duration_minutes
    
    # Update combined adherence
    nutrition_adherence = compliance.nutrition_adherence_percentage or 0
    combined_score = (nutrition_adherence + (100 if compliance_data.completed else 0)) / 2
    compliance.combined_adherence_score = combined_score
    compliance.is_perfect_day = nutrition_adherence >= 100 and compliance_data.completed
    
    # Calculate streak
    yesterday = today - timedelta(days=1)
    yesterday_compliance = db.query(ComplianceRecord).filter(
        and_(
            ComplianceRecord.user_id == current_user.id,
            ComplianceRecord.date == yesterday
        )
    ).first()
    
    if yesterday_compliance and yesterday_compliance.combined_adherence_score >= 90:
        compliance.current_streak_days = (yesterday_compliance.current_streak_days or 0) + 1
    elif compliance.combined_adherence_score >= 90:
        compliance.current_streak_days = 1
    else:
        compliance.current_streak_days = 0
    
    # Update glutamine score
    compliance.glutamine_competition_score = calculate_glutamine_score(current_user.id, db)
    
    db.commit()
    db.refresh(compliance)
    
    return {
        "message": "Workout compliance logged",
        "completed": compliance_data.completed,
        "combined_adherence": round(combined_score, 1),
        "current_streak": compliance.current_streak_days,
    }

@router.get("/streak")
async def get_streak(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current streak information"""
    today = date.today()
    
    compliance = db.query(ComplianceRecord).filter(
        and_(
            ComplianceRecord.user_id == current_user.id,
            ComplianceRecord.date == today
        )
    ).first()
    
    current_streak = compliance.current_streak_days if compliance else 0
    
    # Calculate longest streak
    all_compliance = db.query(ComplianceRecord).filter(
        ComplianceRecord.user_id == current_user.id
    ).order_by(ComplianceRecord.date.desc()).all()
    
    longest_streak = 0
    current_run = 0
    for c in all_compliance:
        if c.combined_adherence_score and c.combined_adherence_score >= 90:
            current_run += 1
            longest_streak = max(longest_streak, current_run)
        else:
            current_run = 0
    
    return {
        "current_streak_days": current_streak,
        "longest_streak_days": longest_streak,
        "is_perfect_day": compliance.is_perfect_day if compliance else False,
    }
