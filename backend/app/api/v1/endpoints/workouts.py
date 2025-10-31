from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.models.workout import WorkoutPlan, WorkoutLog, Exercise
from app.api.v1.endpoints.auth import get_current_user
from app.algorithms.workout_rotation import generate_optimal_workout
from datetime import date
from typing import List, Optional
from pydantic import BaseModel

router = APIRouter()

class WorkoutLogRequest(BaseModel):
    workout_plan_id: Optional[int] = None
    completed: bool
    actual_duration_minutes: Optional[int] = None
    exercises_completed: Optional[List[dict]] = None
    perceived_exertion: Optional[int] = None
    post_workout_soreness_prediction: Optional[dict] = None
    notes: Optional[str] = None

@router.get("/today")
async def get_today_workout(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get today's workout plan, generating if needed"""
    today = date.today()
    
    # Check if workout plan already exists
    existing_plan = db.query(WorkoutPlan).filter(
        WorkoutPlan.user_id == current_user.id,
        WorkoutPlan.date == today
    ).first()
    
    if existing_plan:
        return {
            "id": existing_plan.id,
            "date": existing_plan.date.isoformat(),
            "workout_type": existing_plan.workout_type,
            "target_muscle_groups": existing_plan.target_muscle_groups,
            "exercises": existing_plan.exercises,
            "estimated_duration_minutes": existing_plan.estimated_duration_minutes,
            "coaching_message": existing_plan.coaching_message,
            "weekly_focus": existing_plan.weekly_focus,
        }
    
    # Generate new workout plan
    workout_data = generate_optimal_workout(current_user.id, db)
    
    # Create workout plan record
    workout_plan = WorkoutPlan(
        user_id=current_user.id,
        date=today,
        workout_type=workout_data["workout_type"],
        target_muscle_groups=workout_data["target_muscle_groups"],
        exercises=workout_data["exercises"],
        estimated_duration_minutes=workout_data["estimated_duration_minutes"],
        coaching_message=workout_data["coaching_message"],
        soreness_maintenance_goals=workout_data["soreness_maintenance_goals"],
    )
    db.add(workout_plan)
    db.commit()
    db.refresh(workout_plan)
    
    return {
        "id": workout_plan.id,
        "date": workout_plan.date.isoformat(),
        "workout_type": workout_plan.workout_type,
        "target_muscle_groups": workout_plan.target_muscle_groups,
        "exercises": workout_plan.exercises,
        "estimated_duration_minutes": workout_plan.estimated_duration_minutes,
        "coaching_message": workout_plan.coaching_message,
        "weekly_focus": workout_plan.weekly_focus,
    }

@router.get("/next-muscle-group")
async def get_next_muscle_group(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get which muscle group should be trained next"""
    workout_data = generate_optimal_workout(current_user.id, db)
    return {
        "target_groups": workout_data["target_muscle_groups"],
        "priority": "high" if len(workout_data["target_muscle_groups"]) > 0 else "maintenance"
    }

@router.get("/history")
async def get_workout_history(
    limit: int = 30,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get workout history"""
    workouts = db.query(WorkoutLog).filter(
        WorkoutLog.user_id == current_user.id
    ).order_by(WorkoutLog.date.desc()).limit(limit).all()
    
    return [
        {
            "id": w.id,
            "date": w.date.isoformat(),
            "completed": w.completed,
            "duration_minutes": w.actual_duration_minutes,
            "perceived_exertion": w.perceived_exertion,
            "exercises_completed": w.exercises_completed,
        }
        for w in workouts
    ]

@router.post("/log")
async def log_workout(
    workout_data: WorkoutLogRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Log a completed workout"""
    today = date.today()
    
    workout_log = WorkoutLog(
        user_id=current_user.id,
        workout_plan_id=workout_data.workout_plan_id,
        date=today,
        completed=workout_data.completed,
        actual_duration_minutes=workout_data.actual_duration_minutes,
        exercises_completed=workout_data.exercises_completed or [],
        perceived_exertion=workout_data.perceived_exertion,
        post_workout_soreness_prediction=workout_data.post_workout_soreness_prediction or {},
        notes=workout_data.notes,
    )
    
    db.add(workout_log)
    db.commit()
    db.refresh(workout_log)
    
    return {
        "id": workout_log.id,
        "message": "Workout logged successfully",
        "date": workout_log.date.isoformat()
    }

@router.get("/exercises")
async def get_exercises(
    muscle_group: Optional[str] = None,
    equipment: Optional[str] = None,
    is_baseball_specific: Optional[bool] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get exercise library, optionally filtered"""
    query = db.query(Exercise)
    
    if muscle_group:
        query = query.filter(Exercise.muscle_group_primary == muscle_group)
    
    if is_baseball_specific is not None:
        query = query.filter(Exercise.is_baseball_specific == is_baseball_specific)
    
    exercises = query.all()
    
    # Filter by equipment if specified (client-side for simplicity)
    if equipment:
        exercises = [e for e in exercises if equipment in (e.equipment_required or [])]
    
    return [
        {
            "id": e.id,
            "name": e.name,
            "description": e.description,
            "muscle_group_primary": e.muscle_group_primary,
            "muscle_groups_secondary": e.muscle_groups_secondary,
            "equipment_required": e.equipment_required,
            "difficulty_level": e.difficulty_level,
            "is_baseball_specific": e.is_baseball_specific,
            "form_cues": e.form_cues,
            "video_url": e.video_url,
            "default_sets": e.default_sets,
            "default_reps": e.default_reps,
            "default_duration_seconds": e.default_duration_seconds,
            "default_weight_lbs": e.default_weight_lbs,
        }
        for e in exercises
    ]

@router.get("/exercises/{exercise_id}")
async def get_exercise_detail(
    exercise_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get detailed exercise information"""
    exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    
    return {
        "id": exercise.id,
        "name": exercise.name,
        "description": exercise.description,
        "muscle_group_primary": exercise.muscle_group_primary,
        "muscle_groups_secondary": exercise.muscle_groups_secondary,
        "equipment_required": exercise.equipment_required,
        "difficulty_level": exercise.difficulty_level,
        "is_baseball_specific": exercise.is_baseball_specific,
        "form_cues": exercise.form_cues,
        "video_url": exercise.video_url,
        "default_sets": exercise.default_sets,
        "default_reps": exercise.default_reps,
        "default_duration_seconds": exercise.default_duration_seconds,
        "default_weight_lbs": exercise.default_weight_lbs,
    }
