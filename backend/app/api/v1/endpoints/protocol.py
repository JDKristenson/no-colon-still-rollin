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
from typing import List, Dict, Optional
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
        # Get active markers for response
        active_markers = []
        try:
            from app.algorithms.glutamine import get_active_markers
            active_markers = get_active_markers(current_user.id, db)
        except Exception:
            pass
        
        prioritization_notes = []
        if active_markers:
            active_target_ids = [m.target_id for m in active_markers]
            prioritization_notes.append(f"Protocol prioritized for {len(active_target_ids)} active mutation(s)")
            for marker in active_markers:
                prioritization_notes.append(f"Targeting: {marker.chromosome}:{marker.position} ({marker.ref_base}→{marker.mut_base})")
        
        return {
            "id": existing_protocol.id,
            "date": existing_protocol.date.isoformat(),
            "weight_lbs": existing_protocol.weight_lbs,
            "foods": existing_protocol.foods,
            "total_net_carbs": existing_protocol.total_net_carbs,
            "total_protein": existing_protocol.total_protein,
            "total_fat": existing_protocol.total_fat,
            "total_calories": existing_protocol.total_calories,
            "total_macros": {
                "net_carbs": existing_protocol.total_net_carbs,
                "protein": existing_protocol.total_protein,
                "fat": existing_protocol.total_fat,
                "calories": existing_protocol.total_calories,
            },
            "protein_target": existing_protocol.protein_target,
            "protein_reasoning": existing_protocol.protein_reasoning,
            "keto_compatible": existing_protocol.keto_compatible,
            "keto_score": existing_protocol.keto_score,
            "estimated_glutamine_competition_score": existing_protocol.estimated_glutamine_competition_score,
            "active_markers": [
                {
                    "target_id": m.target_id,
                    "chromosome": m.chromosome,
                    "position": m.position,
                    "variant": f"{m.ref_base}→{m.mut_base}"
                }
                for m in active_markers
            ],
            "marker_prioritization_notes": prioritization_notes,
        }
    
    # Generate new protocol
    return await generate_protocol(current_user, today, db)

@router.post("/generate")
async def generate_protocol_endpoint(
    target_date: Optional[date] = None,
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
    
    # Get active markers for prioritization (gracefully handle if tables don't exist)
    active_markers = []
    active_target_ids = []
    try:
        from app.algorithms.glutamine import get_active_markers
        active_markers = get_active_markers(user.id, db)
        active_target_ids = [m.target_id for m in active_markers] if active_markers else []
    except Exception as e:
        # If genetic marker tables don't exist yet, continue without marker prioritization
        import logging
        logger = logging.getLogger(__name__)
        logger.warning(f"Could not load active markers (migration may be needed): {e}")
        active_markers = []
        active_target_ids = []
    
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
    
    # Calculate food relevance scores based on active markers
    food_scores = []
    for food in foods:
        relevance_score = 1.0  # Base score
        
        # If food has targeted_markers field and matches active markers, boost relevance
        if hasattr(food, 'targeted_markers') and food.targeted_markers:
            food_targets = food.targeted_markers if isinstance(food.targeted_markers, list) else []
            matching_targets = set(food_targets) & set(active_target_ids)
            if matching_targets:
                # Boost by 20% per matching marker, max 40% boost
                boost = min(0.40, len(matching_targets) * 0.20)
                relevance_score = 1.0 + boost
        
        food_scores.append((food, relevance_score))
    
    # Sort foods by relevance (highest first)
    food_scores.sort(key=lambda x: x[1], reverse=True)
    
    for food, relevance_score in food_scores:
        # Use recommended amount, with boost for high-relevance foods
        base_amount = food.recommended_amount_grams
        amount_grams = base_amount * (1.2 if relevance_score > 1.0 else 1.0)
        
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
    
    # Calculate glutamine competition score (with active markers if available)
    try:
        glutamine_score = calculate_glutamine_score(user.id, db, active_markers if active_markers else None)
    except Exception as e:
        # Fallback if marker tables don't exist
        import logging
        logger = logging.getLogger(__name__)
        logger.warning(f"Could not calculate glutamine score with markers: {e}")
        glutamine_score = calculate_glutamine_score(user.id, db, None)
    
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
        protein_target=protein_data.get("target_grams") or 150,
        protein_reasoning=protein_data["reasoning"],
        keto_compatible=keto_compatible,
        keto_score=round(keto_score, 1),
        estimated_glutamine_competition_score=glutamine_score,
    )
    
    db.add(protocol)
    db.commit()
    db.refresh(protocol)
    
    # Build prioritization notes
    prioritization_notes = []
    if active_target_ids:
        prioritization_notes.append(f"Protocol prioritized for {len(active_target_ids)} active mutation(s)")
        for target_id in active_target_ids:
            marker = next((m for m in active_markers if m.target_id == target_id), None)
            if marker:
                prioritization_notes.append(f"Targeting: {marker.chromosome}:{marker.position} ({marker.ref_base}→{marker.mut_base})")
    
    return {
        "id": protocol.id,
        "date": protocol.date.isoformat(),
        "weight_lbs": protocol.weight_lbs,
        "foods": protocol.foods,
        "total_net_carbs": protocol.total_net_carbs,
        "total_protein": protocol.total_protein,
        "total_fat": protocol.total_fat,
        "total_calories": protocol.total_calories,
        "total_macros": {
            "net_carbs": protocol.total_net_carbs,
            "protein": protocol.total_protein,
            "fat": protocol.total_fat,
            "calories": protocol.total_calories,
        },
        "protein_target": protocol.protein_target,
        "protein_reasoning": protocol.protein_reasoning,
        "keto_compatible": protocol.keto_compatible,
        "keto_score": protocol.keto_score,
        "estimated_glutamine_competition_score": protocol.estimated_glutamine_competition_score,
        "active_markers": [
            {
                "target_id": m.target_id,
                "chromosome": m.chromosome,
                "position": m.position,
                "variant": f"{m.ref_base}→{m.mut_base}"
            }
            for m in active_markers
        ],
        "marker_prioritization_notes": prioritization_notes,
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

@router.get("/grocery-list")
async def get_grocery_list(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate grocery list from today's protocol"""
    today = date.today()
    
    # Get today's protocol
    protocol = db.query(DailyProtocol).filter(
        DailyProtocol.user_id == current_user.id,
        DailyProtocol.date == today
    ).first()
    
    if not protocol:
        raise HTTPException(
            status_code=404,
            detail="No protocol found for today. Generate a protocol first."
        )
    
    # Build grocery list from foods
    grocery_items = []
    for food in protocol.foods:
        grocery_items.append({
            "name": food.get("name"),
            "amount": f"{food.get('amount_grams', 0)}g",
            "category": "Produce" if any(x in food.get("name", "").lower() for x in ["turmeric", "ginger", "broccoli", "cauliflower"]) else "Supplements/Other",
            "notes": food.get("preparation_notes") or food.get("reason", ""),
        })
    
    # Group by category
    grouped_items = {}
    for item in grocery_items:
        category = item["category"]
        if category not in grouped_items:
            grouped_items[category] = []
        grouped_items[category].append(item)
    
    return {
        "date": protocol.date.isoformat(),
        "items": grocery_items,
        "grouped": grouped_items,
        "total_items": len(grocery_items),
    }
