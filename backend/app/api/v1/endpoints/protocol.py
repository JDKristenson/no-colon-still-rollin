from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.models.food import Food
from app.models.protocol import DailyProtocol
from app.models.soreness import SorenessRecord
from app.api.v1.endpoints.auth import get_current_user
from app.algorithms.protein_target import calculate_protein_target
from app.algorithms.glutamine import calculate_glutamine_score
from datetime import date, timedelta
from typing import List, Dict
import json

router = APIRouter()

def load_foods_from_seed(db: Session):
    """Load foods from seed data if not in database"""
    foods = db.query(Food).all()
    if len(foods) == 0:
        # Load from seed file
        import os
        seed_path = os.path.join(os.path.dirname(__file__), "../../../../database/seeds/foods.json")
        if os.path.exists(seed_path):
            with open(seed_path, 'r') as f:
                food_data = json.load(f)
                for fd in food_data:
                    food = Food(**fd)
                    db.add(food)
                db.commit()

@router.get("/today")
async def get_today_protocol(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get today's nutrition protocol, generating if needed"""
    today = date.today()
    
    # Load foods if needed
    load_foods_from_seed(db)
    
    # Check if protocol already exists
    existing_protocol = db.query(DailyProtocol).filter(
        DailyProtocol.user_id == current_user.id,
        DailyProtocol.date == today
    ).first()
    
    if existing_protocol:
        return {
            "id": existing_protocol.id,
            "date": existing_protocol.date.isoformat(),
            "weight_lbs": existing_protocol.weight_lbs,
            "foods": existing_protocol.foods,
            "total_net_carbs": existing_protocol.total_net_carbs,
            "total_protein": existing_protocol.total_protein,
            "total_fat": existing_protocol.total_fat,
            "total_calories": existing_protocol.total_calories,
            "protein_target": existing_protocol.protein_target,
            "protein_reasoning": existing_protocol.protein_reasoning,
            "keto_compatible": existing_protocol.keto_compatible,
            "keto_score": existing_protocol.keto_score,
            "estimated_glutamine_competition_score": existing_protocol.estimated_glutamine_competition_score,
        }
    
    # Generate new protocol
    return await generate_protocol(current_user, today, db)

@router.post("/generate")
async def generate_protocol(
    target_date: date = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate a new nutrition protocol"""
    if target_date is None:
        target_date = date.today()
    
    return await generate_protocol(current_user, target_date, db)

async def generate_protocol(user: User, target_date: date, db: Session) -> Dict:
    """Generate nutrition protocol with all foods and calculations"""
    load_foods_from_seed(db)
    
    # Get all foods
    foods = db.query(Food).all()
    
    if not foods:
        raise HTTPException(status_code=500, detail="No foods found in database")
    
    # Get current soreness state for protein adjustment
    from app.algorithms.workout_rotation import get_current_soreness_state
    soreness_state = get_current_soreness_state(user.id, db)
    
    # Calculate protein target
    protein_data = calculate_protein_target(
        user.id,
        soreness_state,
        "moderate",  # Default intensity
        db
    )
    
    # Build protocol foods
    protocol_foods = []
    total_net_carbs = 0
    total_protein = 0
    total_fat = 0
    total_calories = 0
    
    weight_lbs = user.current_weight_lbs or 180  # Default if not set
    
    for food in foods:
        # Use recommended amount (can be weight-adjusted in future)
        amount_grams = food.recommended_amount_grams
        
        # Calculate macros for this amount
        food_carbs = (food.net_carbs_per_100g / 100) * amount_grams
        food_protein = (food.protein_per_100g / 100) * amount_grams
        food_fat = (food.fat_per_100g / 100) * amount_grams
        food_calories = (food_carbs * 4) + (food_protein * 4) + (food_fat * 9)
        
        total_net_carbs += food_carbs
        total_protein += food_protein
        total_fat += food_fat
        total_calories += food_calories
        
        protocol_foods.append({
            "name": food.name,
            "amount_grams": amount_grams,
            "timing": "Throughout day",
            "timing_notes": f"Take {food.name.lower()} as recommended",
            "preparation": "As directed",
            "preparation_notes": food.contraindications or "",
            "reason": f"{food.name} fights cancer through: {', '.join(food.mechanisms or [])}",
            "mechanisms": food.mechanisms or [],
            "safety_notes": food.contraindications,
            "net_carbs": round(food_carbs, 1),
            "protein": round(food_protein, 1),
            "fat": round(food_fat, 1),
            "fiber": round((food.fiber_per_100g / 100) * amount_grams, 1),
        })
    
    # Check keto compatibility
    keto_compatible = total_net_carbs < 50
    keto_score = max(0, 100 - (total_net_carbs * 2))  # Simple scoring
    
    # Calculate glutamine competition score
    glutamine_score = calculate_glutamine_score(user.id, db)
    
    # Create protocol record
    protocol = DailyProtocol(
        user_id=user.id,
        date=target_date,
        weight_lbs=weight_lbs,
        foods=protocol_foods,
        total_net_carbs=round(total_net_carbs, 1),
        total_protein=round(total_protein, 1),
        total_fat=round(total_fat, 1),
        total_calories=round(total_calories, 1),
        protein_target=protein_data["target_grams"],
        protein_reasoning=protein_data["reasoning"],
        keto_compatible=keto_compatible,
        keto_score=round(keto_score, 1),
        estimated_glutamine_competition_score=glutamine_score,
    )
    
    db.add(protocol)
    db.commit()
    db.refresh(protocol)
    
    return {
        "id": protocol.id,
        "date": protocol.date.isoformat(),
        "weight_lbs": protocol.weight_lbs,
        "foods": protocol.foods,
        "total_net_carbs": protocol.total_net_carbs,
        "total_protein": protocol.total_protein,
        "total_fat": protocol.total_fat,
        "total_calories": protocol.total_calories,
        "protein_target": protocol.protein_target,
        "protein_reasoning": protocol.protein_reasoning,
        "keto_compatible": protocol.keto_compatible,
        "keto_score": protocol.keto_score,
        "estimated_glutamine_competition_score": protocol.estimated_glutamine_competition_score,
    }

@router.get("/history")
async def get_protocol_history(
    limit: int = 30,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get protocol history"""
    protocols = db.query(DailyProtocol).filter(
        DailyProtocol.user_id == current_user.id
    ).order_by(DailyProtocol.date.desc()).limit(limit).all()
    
    return [
        {
            "id": p.id,
            "date": p.date.isoformat(),
            "weight_lbs": p.weight_lbs,
            "total_net_carbs": p.total_net_carbs,
            "total_protein": p.total_protein,
            "keto_score": p.keto_score,
        }
        for p in protocols
    ]
