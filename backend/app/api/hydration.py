"""Hydration tracking API endpoints"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "core"))

from database import Database

router = APIRouter()


class HydrationLog(BaseModel):
    user_id: int = 1
    amount_oz: float = 8.0


class HydrationGoal(BaseModel):
    user_id: int = 1
    daily_goal_oz: float


@router.post("/log")
def log_water_intake(log: HydrationLog):
    """Log water intake (default 8oz)"""
    try:
        db = Database()
        log_id = db.log_hydration(log.user_id, log.amount_oz)
        db.close()

        return {
            "message": "Water intake logged successfully",
            "log_id": log_id,
            "amount_oz": log.amount_oz
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/today")
def get_today_hydration(user_id: int = 1):
    """Get today's hydration log and progress"""
    try:
        db = Database()
        today = datetime.now().date().isoformat()

        # Get today's logs
        logs = db.get_hydration_log(user_id, today)

        # Get total and goal
        total = db.get_hydration_total(user_id, today)
        goal = db.get_hydration_goal(user_id)

        db.close()

        return {
            "date": today,
            "logs": logs,
            "total_oz": total,
            "goal_oz": goal,
            "progress_percent": round((total / goal * 100) if goal > 0 else 0, 1),
            "remaining_oz": max(0, goal - total)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history")
def get_hydration_history(user_id: int = 1, date: Optional[str] = None):
    """Get hydration history for a specific date"""
    try:
        db = Database()
        logs = db.get_hydration_log(user_id, date)
        db.close()

        return logs

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/goal")
def get_hydration_goal(user_id: int = 1):
    """Get user's daily hydration goal"""
    try:
        db = Database()
        goal = db.get_hydration_goal(user_id)
        db.close()

        return {"daily_goal_oz": goal}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/goal")
def set_hydration_goal(goal: HydrationGoal):
    """Set user's daily hydration goal"""
    try:
        db = Database()
        success = db.set_hydration_goal(goal.user_id, goal.daily_goal_oz)
        db.close()

        return {
            "message": "Hydration goal updated successfully",
            "daily_goal_oz": goal.daily_goal_oz
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
