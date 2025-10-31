from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.api.v1.endpoints.auth import get_current_user
from app.schemas.dashboard import DashboardResponse
from datetime import date
from app.algorithms.glutamine import calculate_glutamine_score

router = APIRouter()

@router.get("", response_model=DashboardResponse)
async def get_dashboard(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Get today's protocol (placeholder - will be implemented)
    # Get today's workout (placeholder)
    # Get current soreness state (placeholder)
    # Get compliance stats (placeholder)
    
    # Calculate glutamine score (placeholder)
    glutamine_score = calculate_glutamine_score(
        user_id=current_user.id,
        db=db
    )
    
    return {
        "user": {
            "id": current_user.id,
            "name": current_user.name,
            "current_weight_lbs": current_user.current_weight_lbs,
        },
        "nutrition": {
            "today_protocol": None,  # Will be populated
            "adherence_percentage": 0,
            "streak_days": 0,
        },
        "workout": {
            "today_workout": None,
            "completed": False,
            "adherence_percentage": 0,
            "streak_days": 0,
        },
        "soreness": {
            "current_state": {},
            "coverage_percentage": 0,
        },
        "metrics": {
            "glutamine_competition_score": glutamine_score,
            "combined_adherence": 0,
            "current_streak": 0,
        },
        "date": date.today().isoformat(),
    }

