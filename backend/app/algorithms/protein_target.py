from sqlalchemy.orm import Session
from app.models.soreness import SorenessRecord
from app.models.user import User
from datetime import date
from typing import Dict

def calculate_protein_target(user_id: int, soreness_state: Dict[str, int], intensity_goal: str, db: Session) -> Dict:
    """
    Adjusts daily protein target based on current soreness state and goals
    
    Default: Minimal protein (0.6-0.8g per lb) for glutamine competition
    Adjustment: Slightly higher on heavy training days to prevent muscle loss
    
    Balance: Enough protein to maintain muscle, but not so much that cancer
             gets easy access to glutamine
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user or not user.current_weight_lbs:
        return {
            "target_grams": 0,
            "reasoning": "User weight not set"
        }
    
    weight_lbs = user.current_weight_lbs
    base_protein_low = weight_lbs * 0.6  # Low end for glutamine competition
    base_protein_moderate = weight_lbs * 0.8  # Moderate for training days
    
    # Check if heavy training day
    if intensity_goal == "high":
        target = base_protein_moderate
        reasoning = f"Higher protein target for heavy training day to support muscle repair while maintaining glutamine competition."
    else:
        target = base_protein_low
        reasoning = f"Lower protein target to maximize glutamine competition with cancer while maintaining muscle mass."
    
    # Count very sore muscle groups (intensity >= 7)
    very_sore_count = sum(1 for intensity in soreness_state.values() if intensity >= 7)
    
    # If multiple muscle groups very sore, can afford slightly less protein
    # (muscles are already consuming glutamine from soreness)
    if very_sore_count >= 2:
        target *= 0.9
        reasoning += f" Reduced by 10% since {very_sore_count} muscle groups are very sore (already consuming glutamine)."
    
    # Safety threshold: never below 0.5g per lb
    minimum_protein = weight_lbs * 0.5
    if target < minimum_protein:
        target = minimum_protein
        reasoning = f" Minimum protein threshold applied for muscle maintenance (0.5g/lb)."
    
    return {
        "target_grams": round(target, 1),
        "reasoning": reasoning,
        "base_target": round(base_protein_low, 1),
        "adjusted": target != base_protein_low
    }

