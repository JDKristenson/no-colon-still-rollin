from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.core.database import get_db
from app.models.user import User
from app.models.protocol import DailyProtocol
from app.models.workout import WorkoutPlan, WorkoutLog
from app.models.soreness import SorenessRecord
from app.models.compliance import ComplianceRecord
from app.api.v1.endpoints.auth import get_current_user
from app.algorithms.glutamine import calculate_glutamine_score
from app.algorithms.workout_rotation import get_current_soreness_state
from datetime import date, timedelta
from app.schemas.dashboard import DashboardResponse

router = APIRouter()

@router.get("", response_model=DashboardResponse)
async def get_dashboard(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get unified dashboard data with nutrition, workout, and soreness status"""
    today = date.today()
    
    # Get today's protocol
    protocol = db.query(DailyProtocol).filter(
        and_(
            DailyProtocol.user_id == current_user.id,
            DailyProtocol.date == today
        )
    ).first()
    
    # Get today's workout
    workout = db.query(WorkoutPlan).filter(
        and_(
            WorkoutPlan.user_id == current_user.id,
            WorkoutPlan.date == today
        )
    ).first()
    
    # Check if workout completed
    workout_completed = False
    if workout:
        workout_log = db.query(WorkoutLog).filter(
            and_(
                WorkoutLog.user_id == current_user.id,
                WorkoutLog.workout_plan_id == workout.id,
                WorkoutLog.date == today,
                WorkoutLog.completed == True
            )
        ).first()
        workout_completed = workout_log is not None
    
    # Get current soreness state
    soreness_state = get_current_soreness_state(current_user.id, db)
    sore_count = sum(1 for intensity in soreness_state.values() if intensity >= 5)
    coverage_percentage = (sore_count / 6) * 100
    
    # Get compliance stats
    compliance = db.query(ComplianceRecord).filter(
        and_(
            ComplianceRecord.user_id == current_user.id,
            ComplianceRecord.date == today
        )
    ).first()
    
    # Get 7-day adherence
    seven_days_ago = today - timedelta(days=7)
    week_records = db.query(ComplianceRecord).filter(
        and_(
            ComplianceRecord.user_id == current_user.id,
            ComplianceRecord.date >= seven_days_ago,
            ComplianceRecord.date <= today
        )
    ).all()
    
    nutrition_week_avg = 0
    workout_week_avg = 0
    if week_records:
        nutrition_scores = [r.nutrition_adherence_percentage or 0 for r in week_records]
        workout_scores = [100 if r.workout_completed else 0 for r in week_records]
        nutrition_week_avg = sum(nutrition_scores) / len(nutrition_scores) if nutrition_scores else 0
        workout_week_avg = sum(workout_scores) / len(workout_scores) if workout_scores else 0
    
    # Calculate glutamine score
    glutamine_score = calculate_glutamine_score(current_user.id, db)
    
    # Get current streak
    current_streak = compliance.current_streak_days if compliance else 0
    
    return {
        "user": {
            "id": current_user.id,
            "name": current_user.name,
            "current_weight_lbs": current_user.current_weight_lbs,
            "height_inches": current_user.height_inches,
        },
        "nutrition": {
            "today_protocol": {
                "id": protocol.id if protocol else None,
                "date": today.isoformat(),
                "foods": protocol.foods if protocol else [],
                "protein_target": protocol.protein_target if protocol else None,
                "total_macros": {
                    "net_carbs": protocol.total_net_carbs if protocol else 0,
                    "protein": protocol.total_protein if protocol else 0,
                    "fat": protocol.total_fat if protocol else 0,
                    "calories": protocol.total_calories if protocol else 0,
                } if protocol else {
                    "net_carbs": 0,
                    "protein": 0,
                    "fat": 0,
                    "calories": 0,
                },
            } if protocol else None,
            "adherence_percentage": compliance.nutrition_adherence_percentage if compliance else 0,
            "streak_days": current_streak,
            "7_day_avg": round(nutrition_week_avg, 1),
        },
        "workout": {
            "today_workout": {
                "id": workout.id if workout else None,
                "workout_type": workout.workout_type if workout else None,
                "target_muscle_groups": workout.target_muscle_groups if workout else [],
                "exercises": workout.exercises if workout else [],
                "estimated_duration_minutes": workout.estimated_duration_minutes if workout else 0,
                "coaching_message": workout.coaching_message if workout else None,
            } if workout else None,
            "completed": workout_completed,
            "adherence_percentage": round(workout_week_avg, 1),
            "streak_days": current_streak,
        },
        "soreness": {
            "current_state": soreness_state,
            "coverage_percentage": round(coverage_percentage, 1),
            "sore_count": sore_count,
            "gap_warning": sore_count == 0,
        },
        "metrics": {
            "glutamine_competition_score": round(glutamine_score, 1),
            "combined_adherence": compliance.combined_adherence_score if compliance else 0,
            "current_streak": current_streak,
            "is_perfect_day": compliance.is_perfect_day if compliance else False,
        },
        "date": today.isoformat(),
    }
