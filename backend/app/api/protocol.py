"""Protocol API endpoints"""
from fastapi import APIRouter, HTTPException
from datetime import date as date_module
import sys
from pathlib import Path

# Add core modules to path
sys.path.insert(0, str(Path(__file__).parent.parent / "core"))

from database import Database
from protocol_generator import ProtocolGenerator
from app.schemas.protocol import (
    DailyProtocolResponse,
    ProtocolFoodResponse,
    GenerateProtocolRequest
)

router = APIRouter()

@router.post("/generate", response_model=DailyProtocolResponse)
def generate_protocol(request: GenerateProtocolRequest):
    """Generate a new daily protocol"""
    try:
        generator = ProtocolGenerator()

        # Get user
        user = generator.db.get_user(user_id=request.user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Use provided weight or stored weight
        weight = request.weight_lbs if request.weight_lbs else user['current_weight_lbs']
        target_date = request.target_date if request.target_date else date_module.today().isoformat()

        # Generate protocol
        protocol = generator.generate_daily_protocol(
            user_name=user['name'],
            weight_lbs=weight,
            target_date=target_date
        )

        # Convert to response format
        protocol_foods = [
            ProtocolFoodResponse(
                name=food['name'],
                amount_grams=food['amount_grams'],
                servings_per_day=food['servings_per_day'],
                grams_per_serving=food['grams_per_serving'],
                timing=food['timing'],
                timing_notes=food['timing_notes'],
                preparation=food['preparation'],
                preparation_notes=food['preparation_notes'],
                net_carbs=food['net_carbs'],
                protein=food['protein'],
                fat=food['fat'],
                reason=food['reason'],
                mechanisms=food['mechanisms'],
                safety_notes=food['safety_notes']
            )
            for food in protocol['foods']
        ]

        return DailyProtocolResponse(
            date=protocol['date'],
            user_id=protocol['user_id'],
            weight_lbs=protocol['weight_lbs'],
            foods=protocol_foods,
            total_net_carbs=protocol['total_net_carbs'],
            total_protein=protocol['total_protein'],
            total_fat=protocol['total_fat'],
            total_calories=protocol['total_calories'],
            keto_compatible=protocol['keto_compatible'],
            keto_score=protocol['keto_score']
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/today", response_model=DailyProtocolResponse)
def get_today_protocol(user_id: int = 1):
    """Get today's protocol"""
    try:
        db = Database()
        user = db.get_user(user_id=user_id)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        today = date_module.today().isoformat()
        protocol = db.get_protocol_for_date(user_id, today)

        if not protocol:
            raise HTTPException(
                status_code=404,
                detail=f"No protocol found for {today}. Generate one first."
            )

        # Convert foods from JSON
        import json
        foods_data = json.loads(protocol['foods']) if isinstance(protocol['foods'], str) else protocol['foods']

        protocol_foods = [
            ProtocolFoodResponse(**food)
            for food in foods_data
        ]

        db.close()

        return DailyProtocolResponse(
            date=protocol['date'],
            user_id=protocol['user_id'],
            weight_lbs=protocol['weight_lbs'],
            foods=protocol_foods,
            total_net_carbs=protocol['total_net_carbs'],
            total_protein=protocol['total_protein'],
            total_fat=protocol['total_fat'],
            total_calories=protocol['total_calories'],
            keto_compatible=True,
            keto_score=100.0
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/date/{date}", response_model=DailyProtocolResponse)
def get_protocol_by_date(date: str, user_id: int = 1):
    """Get protocol for a specific date"""
    try:
        db = Database()
        user = db.get_user(user_id=user_id)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        protocol = db.get_protocol_for_date(user_id, date)

        if not protocol:
            raise HTTPException(
                status_code=404,
                detail=f"No protocol found for {date}"
            )

        # Convert foods from JSON
        import json
        foods_data = json.loads(protocol['foods']) if isinstance(protocol['foods'], str) else protocol['foods']

        protocol_foods = [
            ProtocolFoodResponse(**food)
            for food in foods_data
        ]

        db.close()

        return DailyProtocolResponse(
            date=protocol['date'],
            user_id=protocol['user_id'],
            weight_lbs=protocol['weight_lbs'],
            foods=protocol_foods,
            total_net_carbs=protocol['total_net_carbs'],
            total_protein=protocol['total_protein'],
            total_fat=protocol['total_fat'],
            total_calories=protocol['total_calories'],
            keto_compatible=True,
            keto_score=100.0
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
