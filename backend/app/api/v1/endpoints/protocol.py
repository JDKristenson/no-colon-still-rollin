from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.api.v1.endpoints.auth import get_current_user
from datetime import date

router = APIRouter()

@router.get("/today")
async def get_today_protocol(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # TODO: Implement protocol generation
    return {
        "date": date.today().isoformat(),
        "foods": [],
        "protein_target": current_user.current_weight_lbs * 0.7 if current_user.current_weight_lbs else 0,
        "total_macros": {
            "net_carbs": 0,
            "protein": 0,
            "fat": 0,
            "calories": 0,
        }
    }

