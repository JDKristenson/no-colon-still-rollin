"""Research library API endpoints"""
from fastapi import APIRouter, HTTPException
from typing import List, Optional
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "core"))

from database import Database
from pubmed_client import PubMedClient
from dose_calculator import DoseCalculator, StudyType
from app.schemas.library import (
    ResearchStudyResponse,
    SearchRequest,
    SaveStudyRequest
)
from pydantic import BaseModel

router = APIRouter()


@router.get("/search", response_model=List[ResearchStudyResponse])
def search_pubmed(
    query: str,
    max_results: int = 20
):
    """
    Search PubMed for research studies

    Example queries:
    - "ginger AND colon cancer"
    - "turmeric AND colorectal cancer"
    - "green tea EGCG AND cancer"
    """
    try:
        client = PubMedClient()
        studies = client.search_and_fetch(query, max_results)

        # Add a 'saved' field to indicate if study is already in database
        db = Database()
        for study in studies:
            existing = db.conn.cursor().execute(
                "SELECT id FROM research_studies WHERE pubmed_id = ?",
                (study.get('pubmed_id'),)
            ).fetchone()
            study['saved'] = existing is not None
        db.close()

        return studies
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/save")
def save_study(request: SaveStudyRequest):
    """Save a research study to the library"""
    try:
        db = Database()

        study_id = db.add_research_study({
            'pubmed_id': request.pubmed_id,
            'title': request.title,
            'authors': request.authors,
            'journal': request.journal,
            'year': request.year,
            'abstract': request.abstract,
            'study_type': request.study_type or 'research',
            'food_studied': request.food_studied or '',
            'compound_studied': request.compound_studied or '',
            'cancer_type': request.cancer_type or 'colon',
            'doi': request.doi or '',
            'url': request.url or f"https://pubmed.ncbi.nlm.nih.gov/{request.pubmed_id}/"
        })

        db.close()

        if study_id == -1:
            return {"message": "Study already saved", "study_id": None}

        return {"message": "Study saved successfully", "study_id": study_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/saved", response_model=List[ResearchStudyResponse])
def get_saved_studies(food_name: Optional[str] = None):
    """Get all saved research studies, optionally filtered by food"""
    try:
        db = Database()

        if food_name:
            cursor = db.conn.cursor()
            cursor.execute("""
                SELECT * FROM research_studies
                WHERE food_studied LIKE ?
                ORDER BY year DESC, title
            """, (f"%{food_name}%",))
            rows = cursor.fetchall()
        else:
            cursor = db.conn.cursor()
            cursor.execute("""
                SELECT * FROM research_studies
                ORDER BY year DESC, title
            """)
            rows = cursor.fetchall()

        studies = []
        for row in rows:
            study = dict(row)
            study['saved'] = True  # All studies from this endpoint are saved
            studies.append(study)

        db.close()
        return studies
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{pubmed_id}")
def delete_study(pubmed_id: str):
    """Remove a study from the library"""
    try:
        db = Database()
        cursor = db.conn.cursor()
        cursor.execute("DELETE FROM research_studies WHERE pubmed_id = ?", (pubmed_id,))
        db.conn.commit()
        deleted_count = cursor.rowcount
        db.close()

        if deleted_count == 0:
            raise HTTPException(status_code=404, detail="Study not found")

        return {"message": "Study deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats")
def get_library_stats():
    """Get statistics about the research library"""
    try:
        db = Database()
        cursor = db.conn.cursor()

        # Total studies
        cursor.execute("SELECT COUNT(*) FROM research_studies")
        total_studies = cursor.fetchone()[0]

        # Studies by food
        cursor.execute("""
            SELECT food_studied, COUNT(*) as count
            FROM research_studies
            WHERE food_studied != ''
            GROUP BY food_studied
            ORDER BY count DESC
            LIMIT 10
        """)
        by_food = [{"food": row[0], "count": row[1]} for row in cursor.fetchall()]

        # Recent studies
        cursor.execute("""
            SELECT COUNT(*) FROM research_studies
            WHERE year >= 2020
        """)
        recent_studies = cursor.fetchone()[0]

        db.close()

        return {
            "total_studies": total_studies,
            "by_food": by_food,
            "recent_studies": recent_studies
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class DoseCalculatorRequest(BaseModel):
    study_dose_mg_kg: float
    study_type: str  # "mouse", "rat", "rabbit", "dog", "monkey", "petri_dish"
    compound_name: str
    food_name: str
    compound_per_100g_food: float
    human_weight_kg: float = 70


@router.post("/dose-calculator")
def calculate_human_dose(request: DoseCalculatorRequest):
    """
    Calculate human equivalent dose from animal studies

    Uses FDA allometric scaling to convert doses from:
    - Mouse studies
    - Rat studies
    - Other animal studies

    Helps translate research findings into practical daily food amounts
    """
    try:
        # Convert study type string to enum
        try:
            study_type_enum = StudyType(request.study_type.lower())
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid study type. Must be one of: mouse, rat, rabbit, dog, monkey, petri_dish"
            )

        # Calculate protocol
        calc = DoseCalculator()
        result = calc.calculate_full_protocol(
            study_dose_mg_kg=request.study_dose_mg_kg,
            study_type=study_type_enum,
            compound_name=request.compound_name,
            food_name=request.food_name,
            compound_per_100g_food=request.compound_per_100g_food,
            human_weight_kg=request.human_weight_kg
        )

        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
