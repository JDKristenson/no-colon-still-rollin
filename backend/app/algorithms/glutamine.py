from sqlalchemy.orm import Session
from app.models.soreness import SorenessRecord
from app.models.compliance import ComplianceRecord
from app.models.genetic_marker import GeneticMarker, CTDNATestResult, DetectedMarker
from datetime import date
from typing import List, Optional

def calculate_glutamine_score(user_id: int, db: Session, active_markers: Optional[List] = None) -> float:
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
    
    base_score = (coverage_score * intensity_multiplier * adherence_multiplier) - protein_penalty
    
    # Marker-based boost: Active markers indicate higher priority for glutamine competition
    if active_markers is None:
        # Query active markers if not provided
        active_markers = get_active_markers(user_id, db)
    
    marker_count = len(active_markers) if active_markers else 0
    if marker_count > 0:
        # Boost score by 15% per active marker, max 30% boost for 2+ markers
        marker_boost = min(0.30, marker_count * 0.15)
        base_score = base_score * (1 + marker_boost)
    
    score = base_score
    
    return max(0.0, min(100.0, score))

def get_active_markers(user_id: int, db: Session) -> List[GeneticMarker]:
    """
    Get currently detected markers from the most recent test.
    Returns list of GeneticMarker objects that are currently active.
    """
    # Get most recent test
    latest_test = db.query(CTDNATestResult).filter(
        CTDNATestResult.user_id == user_id
    ).order_by(CTDNATestResult.test_date.desc()).first()
    
    if not latest_test:
        return []
    
    # Get detected markers from this test
    detected = db.query(DetectedMarker).filter(
        DetectedMarker.test_result_id == latest_test.id,
        DetectedMarker.detected == True
    ).all()
    
    # Return the actual marker objects
    markers = [d.marker for d in detected if d.marker]
    return markers

