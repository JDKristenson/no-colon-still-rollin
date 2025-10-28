"""Medication log API endpoints"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "core"))

from database import Database

router = APIRouter()


class MedicationCreate(BaseModel):
    user_id: int = 1
    name: str
    generic_name: Optional[str] = None
    dosage: str
    frequency: str


class MedicationLog(BaseModel):
    user_id: int = 1
    medication_id: int
    dosage: Optional[str] = None
    taken: bool = True
    notes: Optional[str] = ""


@router.post("/add")
def add_medication(medication: MedicationCreate):
    """Add a new medication"""
    try:
        db = Database()
        med_id = db.add_medication(medication.dict())
        db.close()

        return {
            "message": "Medication added successfully",
            "medication_id": med_id
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/list")
def list_medications(user_id: int = 1):
    """Get all medications for a user"""
    try:
        db = Database()
        medications = db.get_user_medications(user_id)
        db.close()

        return medications

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/log")
def log_medication_dose(log: MedicationLog):
    """Log a medication dose"""
    try:
        db = Database()
        log_id = db.log_medication(log.dict())
        db.close()

        return {
            "message": "Medication logged successfully",
            "log_id": log_id
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/log/history")
def get_medication_history(user_id: int = 1, date: Optional[str] = None, limit: int = 100):
    """Get medication log history"""
    try:
        db = Database()
        logs = db.get_medication_log(user_id, date, limit)
        db.close()

        return logs

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/log/today")
def get_today_medications(user_id: int = 1):
    """Get today's medication log"""
    try:
        today = datetime.now().date().isoformat()
        db = Database()
        logs = db.get_medication_log(user_id, today)
        db.close()

        return logs

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
