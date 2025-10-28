"""Foods database API endpoints"""
from fastapi import APIRouter, HTTPException
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "core"))

from database import Database
from app.schemas.foods import FoodResponse, ActiveCompound, FoodListResponse

router = APIRouter()

@router.get("/", response_model=FoodListResponse)
def get_all_foods():
    """Get all foods in the database"""
    try:
        db = Database()
        foods = db.get_all_foods()
        db.close()

        food_responses = [
            FoodResponse(
                id=food['id'],
                name=food['name'],
                common_names=food.get('common_names', []),
                active_compounds=[
                    ActiveCompound(**comp) if isinstance(comp, dict) else comp
                    for comp in food.get('active_compounds', [])
                ],
                net_carbs_per_100g=food['net_carbs_per_100g'],
                protein_per_100g=food['protein_per_100g'],
                fat_per_100g=food['fat_per_100g'],
                fiber_per_100g=food['fiber_per_100g'],
                cancer_types=food.get('cancer_types', []),
                mechanisms=food.get('mechanisms', []),
                best_preparation=food['best_preparation'],
                preparation_notes=food['preparation_notes'],
                max_daily_amount_grams=food['max_daily_amount_grams'],
                side_effects=food.get('side_effects', []),
                contraindications=food.get('contraindications', []),
                evidence_level=food['evidence_level'],
                pubmed_ids=food.get('pubmed_ids', [])
            )
            for food in foods
        ]

        return FoodListResponse(
            foods=food_responses,
            total=len(food_responses)
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{food_name}", response_model=FoodResponse)
def get_food_by_name(food_name: str):
    """Get a specific food by name"""
    try:
        db = Database()
        food = db.get_food_by_name(food_name)
        db.close()

        if not food:
            raise HTTPException(status_code=404, detail=f"Food '{food_name}' not found")

        return FoodResponse(
            id=food['id'],
            name=food['name'],
            common_names=food.get('common_names', []),
            active_compounds=[
                ActiveCompound(**comp) if isinstance(comp, dict) else comp
                for comp in food.get('active_compounds', [])
            ],
            net_carbs_per_100g=food['net_carbs_per_100g'],
            protein_per_100g=food['protein_per_100g'],
            fat_per_100g=food['fat_per_100g'],
            fiber_per_100g=food['fiber_per_100g'],
            cancer_types=food.get('cancer_types', []),
            mechanisms=food.get('mechanisms', []),
            best_preparation=food['best_preparation'],
            preparation_notes=food['preparation_notes'],
            max_daily_amount_grams=food['max_daily_amount_grams'],
            side_effects=food.get('side_effects', []),
            contraindications=food.get('contraindications', []),
            evidence_level=food['evidence_level'],
            pubmed_ids=food.get('pubmed_ids', [])
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
