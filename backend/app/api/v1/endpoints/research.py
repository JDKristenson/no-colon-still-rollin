from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.models.research import ResearchStudy
from app.api.v1.endpoints.auth import get_current_user
from typing import Optional

router = APIRouter()

@router.get("/nutrition")
async def get_nutrition_research(
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get nutrition-related research studies"""
    studies = db.query(ResearchStudy).filter(
        ResearchStudy.study_type == "nutrition"
    ).limit(limit).all()
    
    return [
        {
            "id": s.id,
            "pubmed_id": s.pubmed_id,
            "title": s.title,
            "authors": s.authors,
            "journal": s.journal,
            "year": s.year,
            "summary": s.summary,
            "evidence_level": "strong",  # Would be in database
            "url": s.url,
        }
        for s in studies
    ]

@router.get("/glutamine")
async def get_glutamine_research(
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get glutamine competition research"""
    studies = db.query(ResearchStudy).filter(
        ResearchStudy.study_type.in_(["glutamine", "metabolic"])
    ).limit(limit).all()
    
    return [
        {
            "id": s.id,
            "pubmed_id": s.pubmed_id,
            "title": s.title,
            "authors": s.authors,
            "journal": s.journal,
            "year": s.year,
            "summary": s.summary,
            "url": s.url,
        }
        for s in studies
    ]

@router.get("/exercise-cancer")
async def get_exercise_cancer_research(
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get exercise and cancer research"""
    studies = db.query(ResearchStudy).filter(
        ResearchStudy.study_type == "exercise"
    ).limit(limit).all()
    
    return [
        {
            "id": s.id,
            "pubmed_id": s.pubmed_id,
            "title": s.title,
            "authors": s.authors,
            "journal": s.journal,
            "year": s.year,
            "summary": s.summary,
            "url": s.url,
        }
        for s in studies
    ]

@router.get("/search")
async def search_research(
    query: str,
    study_type: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Search research studies"""
    db_query = db.query(ResearchStudy)
    
    if study_type:
        db_query = db_query.filter(ResearchStudy.study_type == study_type)
    
    if query:
        db_query = db_query.filter(
            ResearchStudy.title.ilike(f"%{query}%")
        )
    
    studies = db_query.limit(50).all()
    
    return [
        {
            "id": s.id,
            "pubmed_id": s.pubmed_id,
            "title": s.title,
            "authors": s.authors,
            "journal": s.journal,
            "year": s.year,
            "summary": s.summary,
            "study_type": s.study_type,
            "url": s.url,
        }
        for s in studies
    ]

