from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.core.database import get_db
from app.models.user import User
from app.models.compliance import ComplianceRecord
from app.models.soreness import SorenessRecord
from app.api.v1.endpoints.auth import get_current_user
from datetime import date, timedelta
from app.algorithms.workout_rotation import get_current_soreness_state

router = APIRouter()

@router.get("/message")
async def get_coaching_message(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get personalized coaching message based on current state"""
    today = date.today()
    
    # Get compliance stats
    compliance = db.query(ComplianceRecord).filter(
        and_(
            ComplianceRecord.user_id == current_user.id,
            ComplianceRecord.date == today
        )
    ).first()
    
    # Get soreness state
    soreness_state = get_current_soreness_state(current_user.id, db)
    sore_count = sum(1 for intensity in soreness_state.values() if intensity >= 5)
    
    # Build personalized message
    messages = []
    
    # Streak message
    if compliance and compliance.current_streak_days:
        if compliance.current_streak_days >= 7:
            messages.append(f"🔥 {compliance.current_streak_days} day streak! You're crushing it!")
        elif compliance.current_streak_days >= 3:
            messages.append(f"💪 {compliance.current_streak_days} days strong - keep it going!")
    
    # Soreness message
    if sore_count == 0:
        messages.append("⚠️ No muscle groups are sore. Time to train and rebuild that glutamine competition!")
    elif sore_count >= 3:
        messages.append(f"✓ Great soreness coverage ({sore_count} groups). Maintaining that competition!")
    elif sore_count == 1:
        messages.append("⚠️ Only one muscle group sore. Consider training more groups soon.")
    
    # Adherence message
    if compliance:
        if compliance.combined_adherence_score and compliance.combined_adherence_score >= 90:
            messages.append("🎯 Perfect adherence today! Cancer's feeling the pressure.")
        elif compliance.combined_adherence_score and compliance.combined_adherence_score >= 70:
            messages.append("👍 Good progress today. Keep pushing forward!")
        elif compliance.nutrition_adherence_percentage and compliance.nutrition_adherence_percentage < 50:
            messages.append("📋 Let's get those protocol foods in. Every meal matters!")
    
    if not messages:
        messages.append("💪 Let's make today count. One meal, one workout, one day at a time.")
    
    return {
        "message": " ".join(messages),
        "streak_days": compliance.current_streak_days if compliance else 0,
        "soreness_coverage": sore_count,
        "adherence_score": compliance.combined_adherence_score if compliance else 0,
    }

@router.get("/weekly-focus")
async def get_weekly_focus(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get this week's focus message"""
    today = date.today()
    week_start = today - timedelta(days=today.weekday())
    
    # Get compliance for the week
    week_compliance = db.query(ComplianceRecord).filter(
        and_(
            ComplianceRecord.user_id == current_user.id,
            ComplianceRecord.date >= week_start,
            ComplianceRecord.date <= today
        )
    ).all()
    
    avg_adherence = 0
    if week_compliance:
        scores = [c.combined_adherence_score for c in week_compliance if c.combined_adherence_score]
        avg_adherence = sum(scores) / len(scores) if scores else 0
    
    # Determine weekly focus
    if avg_adherence >= 85:
        focus = "This week: Maintain your momentum. You're building a winning streak!"
    elif avg_adherence >= 70:
        focus = "This week: Focus on consistency. Small daily actions create big results."
    else:
        focus = "This week: Let's rebuild. Focus on one meal and one workout at a time."
    
    return {
        "focus_message": focus,
        "week_start": week_start.isoformat(),
        "average_adherence": round(avg_adherence, 1),
        "days_tracked": len(week_compliance),
    }

