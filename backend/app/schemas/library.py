"""Schemas for research library API"""
from pydantic import BaseModel
from typing import Optional


class SearchRequest(BaseModel):
    query: str
    max_results: int = 20


class SaveStudyRequest(BaseModel):
    pubmed_id: str
    title: str
    authors: Optional[str] = ""
    journal: Optional[str] = ""
    year: Optional[int] = None
    abstract: Optional[str] = ""
    study_type: Optional[str] = "research"
    food_studied: Optional[str] = ""
    compound_studied: Optional[str] = ""
    cancer_type: Optional[str] = "colon"
    doi: Optional[str] = ""
    url: Optional[str] = ""


class ResearchStudyResponse(BaseModel):
    pubmed_id: str
    title: str
    authors: Optional[str] = ""
    journal: Optional[str] = ""
    year: Optional[int] = None
    abstract: Optional[str] = ""
    doi: Optional[str] = ""
    url: Optional[str] = ""
    saved: Optional[bool] = False

    class Config:
        from_attributes = True
