from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.models.protocol import DailyProtocol
from app.models.workout import WorkoutLog
from app.models.weight import WeightRecord
from app.models.compliance import ComplianceRecord
from app.api.v1.endpoints.auth import get_current_user
from datetime import date, timedelta
import csv
import io
import json

router = APIRouter()

@router.get("/data")
async def export_data(
    format: str = "json",
    days: int = 90,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Export user data in JSON or CSV format"""
    start_date = date.today() - timedelta(days=days)
    
    # Gather all data
    protocols = db.query(DailyProtocol).filter(
        DailyProtocol.user_id == current_user.id,
        DailyProtocol.date >= start_date
    ).all()
    
    workouts = db.query(WorkoutLog).filter(
        WorkoutLog.user_id == current_user.id,
        WorkoutLog.date >= start_date
    ).all()
    
    weights = db.query(WeightRecord).filter(
        WeightRecord.user_id == current_user.id,
        WeightRecord.date >= start_date
    ).all()
    
    compliance = db.query(ComplianceRecord).filter(
        ComplianceRecord.user_id == current_user.id,
        ComplianceRecord.date >= start_date
    ).all()
    
    data = {
        "user": {
            "name": current_user.name,
            "email": current_user.email,
            "current_weight_lbs": current_user.current_weight_lbs,
        },
        "protocols": [
            {
                "date": p.date.isoformat(),
                "foods": p.foods,
                "macros": {
                    "net_carbs": p.total_net_carbs,
                    "protein": p.total_protein,
                    "fat": p.total_fat,
                    "calories": p.total_calories,
                },
                "keto_score": p.keto_score,
            }
            for p in protocols
        ],
        "workouts": [
            {
                "date": w.date.isoformat(),
                "completed": w.completed,
                "duration_minutes": w.actual_duration_minutes,
                "rpe": w.perceived_exertion,
            }
            for w in workouts
        ],
        "weights": [
            {
                "date": w.date.isoformat(),
                "weight_lbs": w.weight_lbs,
                "energy_level": w.energy_level,
                "sleep_quality": w.sleep_quality,
            }
            for w in weights
        ],
        "compliance": [
            {
                "date": c.date.isoformat(),
                "nutrition_adherence": c.nutrition_adherence_percentage,
                "workout_completed": c.workout_completed,
                "combined_score": c.combined_adherence_score,
            }
            for c in compliance
        ],
    }
    
    if format == "csv":
        # Convert to CSV
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write headers
        writer.writerow(["Type", "Date", "Data"])
        
        # Write data
        for p in protocols:
            writer.writerow(["Protocol", p.date.isoformat(), json.dumps(p.foods)])
        
        for w in workouts:
            writer.writerow(["Workout", w.date.isoformat(), str(w.completed)])
        
        for w in weights:
            writer.writerow(["Weight", w.date.isoformat(), str(w.weight_lbs)])
        
        for c in compliance:
            writer.writerow(["Compliance", c.date.isoformat(), str(c.combined_adherence_score)])
        
        return Response(
            content=output.getvalue(),
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename=nocolon_export_{date.today().isoformat()}.csv"}
        )
    
    # JSON format
    return data

@router.get("/complete-report")
async def export_complete_report(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate complete health report (JSON format - PDF would require additional library)"""
    # Get comprehensive data
    from app.api.v1.endpoints.dashboard import get_dashboard
    dashboard_data = await get_dashboard(current_user, db)
    
    # Get trends
    from app.api.v1.endpoints.weight import get_weight_trend
    weight_trend = await get_weight_trend(90, current_user, db)
    
    # Get compliance stats
    from app.api.v1.endpoints.compliance import get_compliance_stats
    compliance_stats = await get_compliance_stats(current_user, db)
    
    report = {
        "generated_at": date.today().isoformat(),
        "user": dashboard_data["user"],
        "summary": {
            "current_weight": dashboard_data["user"]["current_weight_lbs"],
            "weight_change": weight_trend.get("change_lbs", 0),
            "glutamine_score": dashboard_data["metrics"]["glutamine_competition_score"],
            "current_streak": compliance_stats["current_streak"],
            "7_day_adherence": compliance_stats["7_day_combined_avg"],
        },
        "dashboard": dashboard_data,
        "weight_trend": weight_trend,
        "compliance": compliance_stats,
    }
    
    return report

