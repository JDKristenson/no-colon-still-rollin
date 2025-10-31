from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.api.v1.endpoints.auth import get_current_user
from datetime import date

router = APIRouter()

@router.get("/today")
async def get_today_workout(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # TODO: Implement workout generation
    return {
        "date": date.today().isoformat(),
        "workout_type": "strength",
        "target_muscle_groups": [],
        "exercises": [],
        "estimated_duration_minutes": 30,
    }

