from sqlalchemy import Column, Integer, String, Text, JSON, Integer as Int
from app.core.database import Base

class ResearchStudy(Base):
    __tablename__ = "research_studies"
    
    id = Column(Integer, primary_key=True, index=True)
    pubmed_id = Column(String, unique=True, index=True)
    title = Column(Text, nullable=False)
    authors = Column(Text)
    journal = Column(String)
    year = Column(Int)
    
    study_type = Column(String)  # "nutrition", "exercise", "glutamine", "metabolic"
    relevance_tags = Column(JSON, default=list)
    
    summary = Column(Text)
    results = Column(Text)
    efficacy_percentage = Column(Integer)
    
    url = Column(String)
    doi = Column(String)
    
    # Genetic marker relevance
    related_markers = Column(JSON, nullable=True)  # Array of marker targetIds this research relates to

