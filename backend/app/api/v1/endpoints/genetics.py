from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.models.genetic_marker import GeneticMarker, CTDNATestResult, DetectedMarker
from app.api.v1.endpoints.auth import get_current_user
from app.core.signatera_parser import parse_signatera_excel
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
import tempfile
import os
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

class MarkerCreate(BaseModel):
    target_id: str
    chromosome: str
    position: int
    variant_type: str
    ref_base: str
    mut_base: str
    gene_name: Optional[str] = None
    notes: Optional[str] = None

class ManualDetectionRequest(BaseModel):
    target_ids: List[str]  # List of target_id values to mark as detected
    test_date: Optional[datetime] = None

@router.post("/upload-test")
async def upload_test(
    file: UploadFile = File(...),
    test_date: Optional[datetime] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload Signatera Excel file and create test result with detected markers"""
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be an Excel file (.xlsx or .xls)"
        )
    
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp_file:
        content = await file.read()
        tmp_file.write(content)
        tmp_file_path = tmp_file.name
    
    try:
        # Parse Excel file
        markers_data = parse_signatera_excel(tmp_file_path)
        
        if not markers_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No markers found in file"
            )
        
        # Create test result
        test_result = CTDNATestResult(
            user_id=current_user.id,
            test_date=test_date or datetime.utcnow(),
            test_lab="Signatera",
            result_file_name=file.filename
        )
        db.add(test_result)
        db.flush()  # Get ID without committing
        
        # Process markers
        created_count = 0
        detected_count = 0
        
        for marker_data in markers_data:
            # Find or create genetic marker
            marker = db.query(GeneticMarker).filter(
                GeneticMarker.user_id == current_user.id,
                GeneticMarker.target_id == marker_data["target_id"]
            ).first()
            
            if not marker:
                # Create new marker (baseline)
                marker = GeneticMarker(
                    user_id=current_user.id,
                    **marker_data
                )
                db.add(marker)
                db.flush()
                created_count += 1
            
            # For now, assume all markers in file are detected
            # In real Signatera files, detection would be indicated separately
            detected = DetectedMarker(
                test_result_id=test_result.id,
                marker_id=marker.id,
                detected=True
            )
            db.add(detected)
            detected_count += 1
        
        db.commit()
        db.refresh(test_result)
        
        return {
            "test_id": test_result.id,
            "test_date": test_result.test_date.isoformat(),
            "markers_processed": len(markers_data),
            "markers_created": created_count,
            "markers_detected": detected_count,
            "message": "Test uploaded successfully"
        }
        
    except ValueError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        db.rollback()
        logger.error(f"Error uploading test: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process test file: {str(e)}"
        )
    finally:
        # Clean up temp file
        if os.path.exists(tmp_file_path):
            os.unlink(tmp_file_path)

@router.get("/markers")
async def get_markers(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all baseline markers for the user"""
    markers = db.query(GeneticMarker).filter(
        GeneticMarker.user_id == current_user.id
    ).order_by(GeneticMarker.target_id).all()
    
    # Get active markers
    active_marker_ids = get_active_marker_ids(current_user.id, db)
    
    return {
        "markers": [
            {
                "id": m.id,
                "target_id": m.target_id,
                "chromosome": m.chromosome,
                "position": m.position,
                "variant_type": m.variant_type,
                "ref_base": m.ref_base,
                "mut_base": m.mut_base,
                "gene_name": m.gene_name,
                "is_active": m.id in active_marker_ids,
                "created_at": m.created_at.isoformat() if m.created_at else None,
            }
            for m in markers
        ],
        "total": len(markers),
        "active_count": len(active_marker_ids)
    }

@router.get("/markers/active")
async def get_active_markers(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get currently detected/active markers from most recent test"""
    from app.algorithms.glutamine import get_active_markers as _get_active_markers
    
    active_markers = _get_active_markers(current_user.id, db)
    
    return {
        "markers": [
            {
                "id": m.id,
                "target_id": m.target_id,
                "chromosome": m.chromosome,
                "position": m.position,
                "variant_type": m.variant_type,
                "ref_base": m.ref_base,
                "mut_base": m.mut_base,
                "gene_name": m.gene_name,
            }
            for m in active_markers
        ],
        "count": len(active_markers)
    }

@router.get("/tests")
async def get_tests(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all test results for the user"""
    tests = db.query(CTDNATestResult).filter(
        CTDNATestResult.user_id == current_user.id
    ).order_by(CTDNATestResult.test_date.desc()).all()
    
    results = []
    for test in tests:
        detected_count = db.query(DetectedMarker).filter(
            DetectedMarker.test_result_id == test.id,
            DetectedMarker.detected == True
        ).count()
        
        results.append({
            "id": test.id,
            "test_date": test.test_date.isoformat(),
            "test_lab": test.test_lab,
            "result_file_name": test.result_file_name,
            "detected_count": detected_count,
            "uploaded_at": test.uploaded_at.isoformat() if test.uploaded_at else None,
        })
    
    return {
        "tests": results,
        "total": len(results)
    }

@router.get("/tests/{test_id}")
async def get_test_details(
    test_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get specific test with detected markers"""
    test = db.query(CTDNATestResult).filter(
        CTDNATestResult.id == test_id,
        CTDNATestResult.user_id == current_user.id
    ).first()
    
    if not test:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Test not found"
        )
    
    detected = db.query(DetectedMarker).filter(
        DetectedMarker.test_result_id == test.id,
        DetectedMarker.detected == True
    ).all()
    
    markers = []
    for d in detected:
        m = d.marker
        markers.append({
            "id": m.id,
            "target_id": m.target_id,
            "chromosome": m.chromosome,
            "position": m.position,
            "variant_type": m.variant_type,
            "ref_base": m.ref_base,
            "mut_base": m.mut_base,
            "variant_allele_frequency": d.variant_allele_frequency,
        })
    
    return {
        "id": test.id,
        "test_date": test.test_date.isoformat(),
        "test_lab": test.test_lab,
        "result_file_name": test.result_file_name,
        "notes": test.notes,
        "detected_markers": markers,
        "detected_count": len(markers),
        "uploaded_at": test.uploaded_at.isoformat() if test.uploaded_at else None,
    }

@router.post("/markers/manual-detect")
async def manual_detect_markers(
    request: ManualDetectionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Manually mark markers as detected (for when genetic counselor provides info)"""
    test_date = request.test_date or datetime.utcnow()
    
    # Create a test result for this manual entry
    test_result = CTDNATestResult(
        user_id=current_user.id,
        test_date=test_date,
        test_lab="Signatera",
        result_file_name="Manual Entry",
        notes="Manually entered based on genetic counselor information"
    )
    db.add(test_result)
    db.flush()
    
    detected_count = 0
    not_found = []
    
    for target_id in request.target_ids:
        # Find marker by target_id
        marker = db.query(GeneticMarker).filter(
            GeneticMarker.user_id == current_user.id,
            GeneticMarker.target_id == target_id
        ).first()
        
        if not marker:
            not_found.append(target_id)
            continue
        
        # Check if already detected in this test
        existing = db.query(DetectedMarker).filter(
            DetectedMarker.test_result_id == test_result.id,
            DetectedMarker.marker_id == marker.id
        ).first()
        
        if not existing:
            detected = DetectedMarker(
                test_result_id=test_result.id,
                marker_id=marker.id,
                detected=True
            )
            db.add(detected)
            detected_count += 1
    
    db.commit()
    db.refresh(test_result)
    
    return {
        "test_id": test_result.id,
        "test_date": test_result.test_date.isoformat(),
        "detected_count": detected_count,
        "not_found": not_found,
        "message": f"Marked {detected_count} marker(s) as detected"
    }

@router.post("/markers/create-baseline")
async def create_baseline_markers(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create baseline markers from the Signatera Excel file (16 markers)"""
    # Check if baseline already exists
    existing = db.query(GeneticMarker).filter(
        GeneticMarker.user_id == current_user.id
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Baseline markers already exist for this user"
        )
    
    # Parse the Excel file from Desktop
    excel_path = "/Users/JDKristenson/Desktop/JM_Signatera_variant_information_19053697.xlsx"
    
    try:
        markers_data = parse_signatera_excel(excel_path)
        
        for marker_data in markers_data:
            marker = GeneticMarker(
                user_id=current_user.id,
                **marker_data
            )
            db.add(marker)
        
        db.commit()
        
        return {
            "created": len(markers_data),
            "message": "Baseline markers created successfully"
        }
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating baseline markers: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create baseline markers: {str(e)}"
        )

def get_active_marker_ids(user_id: int, db: Session) -> List[int]:
    """Helper to get active marker IDs"""
    from app.models.genetic_marker import CTDNATestResult, DetectedMarker
    
    latest_test = db.query(CTDNATestResult).filter(
        CTDNATestResult.user_id == user_id
    ).order_by(CTDNATestResult.test_date.desc()).first()
    
    if not latest_test:
        return []
    
    detected = db.query(DetectedMarker).filter(
        DetectedMarker.test_result_id == latest_test.id,
        DetectedMarker.detected == True
    ).all()
    
    return [d.marker_id for d in detected]

