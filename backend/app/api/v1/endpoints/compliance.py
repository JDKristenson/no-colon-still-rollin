from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.api.v1.endpoints.auth import get_current_user

router = APIRouter()

@router.get("/stats")
async def get_compliance_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # TODO: Calculate compliance stats
    return {
        "nutrition_adherence": 0,
        "workout_adherence": 0,
        "combined_adherence": 0,
        "current_streak": 0,
    }

