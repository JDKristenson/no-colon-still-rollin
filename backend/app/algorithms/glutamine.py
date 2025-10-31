from sqlalchemy.orm import Session
from app.models.soreness import SorenessRecord
from app.models.compliance import ComplianceRecord
from datetime import date
from typing import List

def calculate_glutamine_score(user_id: int, db: Session) -> float:
    """
    Complex glutamine competition score calculation
    
    Factors:
    - Number of sore muscle groups (coverage)
    - Average soreness intensity
    - Nutrition adherence
    - Protein intake penalty
    
    Returns: Score 0-100
    """
    today = date.today()
    
    # Get recent soreness records
    soreness_records = db.query(SorenessRecord).filter(
        SorenessRecord.user_id == user_id,
        SorenessRecord.date == today,
        SorenessRecord.soreness_intensity >= 5  # Active soreness
    ).all()
    
    # Get recent compliance
    compliance = db.query(ComplianceRecord).filter(
        ComplianceRecord.user_id == user_id,
        ComplianceRecord.date == today
    ).first()
    
    # Base score from soreness coverage
    sore_muscle_groups = len(soreness_records)
    max_muscle_groups = 6
    coverage_score = (sore_muscle_groups / max_muscle_groups) * 100
    
    # Weight by average soreness intensity
    if soreness_records:
        avg_intensity = sum(r.soreness_intensity for r in soreness_records) / len(soreness_records)
        intensity_multiplier = avg_intensity / 10.0
    else:
        intensity_multiplier = 0
    
    # Factor in nutrition adherence
    adherence_multiplier = (compliance.nutrition_adherence_percentage / 100.0) if compliance else 0.5
    
    # Protein penalty (would need protein intake data - placeholder)
    protein_penalty = 0  # TODO: Calculate based on actual protein intake
    
    score = (coverage_score * intensity_multiplier * adherence_multiplier) - protein_penalty
    
    return max(0.0, min(100.0, score))

