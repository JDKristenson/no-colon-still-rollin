from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from app.models.soreness import SorenessRecord
from app.models.workout import WorkoutLog, Exercise, MuscleGroup
from app.models.user import User
from datetime import date, timedelta
from typing import List, Dict, Optional

MUSCLE_GROUPS = ["chest", "back", "shoulders", "legs", "core", "arms"]

def get_current_soreness_state(user_id: int, db: Session) -> Dict[str, int]:
    """Get current soreness intensity for all muscle groups"""
    today = date.today()
    soreness_state = {}
    
    for muscle_group in MUSCLE_GROUPS:
        record = db.query(SorenessRecord).filter(
            and_(
                SorenessRecord.user_id == user_id,
                SorenessRecord.muscle_group == muscle_group,
                SorenessRecord.date == today
            )
        ).order_by(SorenessRecord.logged_at.desc()).first()
        
        soreness_state[muscle_group] = record.soreness_intensity if record else 0
    
    return soreness_state

def hours_since_last_workout(user_id: int, muscle_group: str, db: Session) -> Optional[int]:
    """Calculate hours since last workout targeting this muscle group"""
    workout = db.query(WorkoutLog).join(WorkoutLog).filter(
        and_(
            WorkoutLog.user_id == user_id,
            WorkoutLog.completed == True,
            func.jsonb_path_exists(
                func.jsonb_build_object('target_muscle_groups', '[]'),
                f'$.target_muscle_groups[*] ? (@ == "{muscle_group}")'
            )
        )
    ).order_by(WorkoutLog.date.desc()).first()
    
    if workout:
        today = date.today()
        days_diff = (today - workout.date).days
        return days_diff * 24
    
    return None

def predict_soreness_duration(user_id: int, muscle_group: str, workout_intensity: int, db: Session) -> int:
    """
    Predict how long muscle soreness will last based on workout intensity
    Typical ranges: 24-72 hours
    """
    base_duration_hours = 48
    
    # Adjust based on intensity
    if workout_intensity >= 8:
        base_duration_hours = 72
    elif workout_intensity <= 4:
        base_duration_hours = 24
    
    # Get user's historical recovery rate (simplified for now)
    # In production, would calculate based on past workouts
    user_recovery_rate = 1.0
    
    adjusted_duration = int(base_duration_hours * user_recovery_rate)
    return adjusted_duration

def generate_optimal_workout(user_id: int, db: Session) -> Dict:
    """
    Determines which muscle group(s) to train today to maintain continuous soreness
    
    Logic:
    1. Identify muscle groups that are no longer sore (priority targets)
    2. Check which groups are recovering but not overtrained
    3. Ensure we don't train groups that are still very sore
    4. Maintain rotation to prevent gaps in coverage
    5. Respect recovery times (48-72 hours between same muscle group)
    """
    current_soreness = get_current_soreness_state(user_id, db)
    user = db.query(User).filter(User.id == user_id).first()
    
    # Priority 1: Groups that have fully recovered (no soreness coverage gap)
    recovered_groups = [
        mg for mg in MUSCLE_GROUPS
        if current_soreness.get(mg, 0) == 0
    ]
    
    # Priority 2: Groups with minimal soreness (fading, need re-stimulation)
    fading_groups = [
        mg for mg in MUSCLE_GROUPS
        if 0 < current_soreness.get(mg, 0) <= 3
    ]
    
    # Priority 3: Rotation schedule (maintain balance)
    # Check when each group was last trained
    group_last_trained = {}
    for mg in MUSCLE_GROUPS:
        hours = hours_since_last_workout(user_id, mg, db)
        group_last_trained[mg] = hours if hours else 999
    
    # Select 1-2 muscle groups (depending on available time)
    target_groups = []
    
    # First priority: recovered groups that haven't been trained recently
    if recovered_groups:
        # Sort by time since last workout (oldest first)
        recovered_groups.sort(key=lambda mg: group_last_trained.get(mg, 999))
        target_groups.append(recovered_groups[0])
    
    # Second priority: fading groups if we need another target
    if len(target_groups) < 2 and fading_groups:
        # Don't select same group as already selected
        available_fading = [mg for mg in fading_groups if mg not in target_groups]
        if available_fading:
            available_fading.sort(key=lambda mg: group_last_trained.get(mg, 999))
            target_groups.append(available_fading[0])
    
    # Fallback: if all groups are sore, select least sore group for maintenance
    if not target_groups:
        least_sore = min(MUSCLE_GROUPS, key=lambda mg: current_soreness.get(mg, 0))
        if current_soreness.get(least_sore, 0) < 8:  # Not overtraining
            target_groups.append(least_sore)
    
    # If still no target, use rotation schedule
    if not target_groups:
        # Simple rotation: pick group that hasn't been trained in longest time
        target_groups.append(min(MUSCLE_GROUPS, key=lambda mg: group_last_trained.get(mg, 0)))
    
    # Limit to 1-2 groups based on available time
    if user and user.workout_time_available:
        if user.workout_time_available < 45:
            target_groups = target_groups[:1]  # One group for shorter workouts
        else:
            target_groups = target_groups[:2]  # Two groups for longer workouts
    
    # Get exercises for target groups
    exercises = []
    for muscle_group in target_groups:
        group_exercises = db.query(Exercise).filter(
            Exercise.muscle_group_primary == muscle_group
        ).limit(3).all()
        
        for ex in group_exercises:
            exercises.append({
                "id": ex.id,
                "name": ex.name,
                "description": ex.description,
                "sets": ex.default_sets,
                "reps": ex.default_reps,
                "weight_lbs": ex.default_weight_lbs,
                "duration_seconds": ex.default_duration_seconds,
                "form_cues": ex.form_cues,
                "equipment_required": ex.equipment_required,
            })
    
    # Generate coaching message
    coaching_message = generate_coaching_message(target_groups, current_soreness)
    
    return {
        "target_muscle_groups": target_groups,
        "exercises": exercises,
        "workout_type": "strength" if len(target_groups) <= 2 else "mixed",
        "estimated_duration_minutes": calculate_duration(exercises),
        "coaching_message": coaching_message,
        "soreness_maintenance_goals": [
            {
                "muscle_group": mg,
                "current_soreness": current_soreness.get(mg, 0),
                "target_soreness": 6  # Goal is moderate soreness
            }
            for mg in target_groups
        ]
    }

def generate_coaching_message(target_groups: List[str], current_soreness: Dict[str, int]) -> str:
    """Generate personalized coaching message based on workout goals"""
    if len(target_groups) == 1:
        group = target_groups[0]
        current = current_soreness.get(group, 0)
        
        if current == 0:
            return f"Let's get {group} back in the rotation. Time to build some soreness and maintain that glutamine competition. You got this! 💪"
        elif current <= 3:
            return f"{group.capitalize()} is fading - perfect time to re-stimulate. Let's keep that continuous soreness coverage going."
    else:
        return f"Today we're targeting {', '.join(target_groups)}. Focus on controlled intensity - we want soreness, not overtraining. Maintain the rotation!"
    
    return "Let's maintain your soreness rotation and keep competing for that glutamine! 💪"

def calculate_duration(exercises: List[Dict]) -> int:
    """Calculate estimated workout duration in minutes"""
    if not exercises:
        return 30
    
    # Rough estimate: 2 min per exercise (includes rest)
    base_time = len(exercises) * 2
    
    # Add warm-up and cool-down
    return base_time + 10  # 5 min warm-up + 5 min cool-down

