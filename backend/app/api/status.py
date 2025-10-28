"""Status and dashboard API endpoints"""
from fastapi import APIRouter, HTTPException
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "core"))

from database import Database
from app.schemas.status import UserStatusResponse, WeightSummary, ComplianceSummary

router = APIRouter()

@router.get("/", response_model=UserStatusResponse)
def get_user_status(user_id: int = 1):
    """Get complete user status for dashboard"""
    try:
        db = Database()

        # Get user
        user = db.get_user(user_id=user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Weight summary
        weight_history = db.get_weight_history(user_id, limit=2)
        recent_change = None
        trend = "stable"

        if len(weight_history) >= 2:
            recent_change = weight_history[0]['weight_lbs'] - weight_history[1]['weight_lbs']
            if recent_change > 0.5:
                trend = "up"
            elif recent_change < -0.5:
                trend = "down"

        weight_summary = WeightSummary(
            current_weight_lbs=user['current_weight_lbs'],
            target_weight_lbs=user.get('target_weight_lbs'),
            recent_change_lbs=recent_change,
            trend=trend
        )

        # Compliance summary
        compliance_7day = db.get_compliance_history(user_id, days=7)
        compliance_30day = db.get_compliance_history(user_id, days=30)

        avg_7day = 0
        avg_30day = 0
        current_streak = 0
        total_days = len(compliance_30day)

        if compliance_7day:
            avg_7day = sum(r['adherence_percentage'] for r in compliance_7day) / len(compliance_7day)

        if compliance_30day:
            avg_30day = sum(r['adherence_percentage'] for r in compliance_30day) / len(compliance_30day)

            # Calculate current streak (80%+ adherence)
            for record in compliance_30day:
                if record['adherence_percentage'] >= 80:
                    current_streak += 1
                else:
                    break

        compliance_summary = ComplianceSummary(
            current_streak_days=current_streak,
            average_adherence_7day=round(avg_7day, 1),
            average_adherence_30day=round(avg_30day, 1),
            total_days_tracked=total_days
        )

        # System stats
        cursor = db.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM foods")
        total_foods = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM research_studies")
        total_studies = cursor.fetchone()[0]

        db.close()

        return UserStatusResponse(
            user_id=user['id'],
            name=user['name'],
            cancer_type=user['cancer_type'],
            weight=weight_summary,
            compliance=compliance_summary,
            total_foods_in_database=total_foods,
            total_research_studies=total_studies
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
