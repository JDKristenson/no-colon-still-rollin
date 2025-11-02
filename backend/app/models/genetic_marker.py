from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Float, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class GeneticMarker(Base):
    __tablename__ = "genetic_markers"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    # Marker identification
    target_id = Column(String, nullable=False)  # e.g., "target_1", "target_2"
    chromosome = Column(String, nullable=False)  # e.g., "chr16", "chr17"
    position = Column(Integer, nullable=False)
    
    # Variant information
    variant_type = Column(String, nullable=False)  # "Transversion" or "Transition"
    ref_base = Column(String, nullable=False)  # Reference base (A, C, G, T)
    mut_base = Column(String, nullable=False)  # Mutation base (A, C, G, T)
    
    # Optional fields
    gene_name = Column(String, nullable=True)
    notes = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationship
    user = relationship("User", backref="genetic_markers")
    
    # Unique constraint is handled by the migration, not here

class CTDNATestResult(Base):
    __tablename__ = "ctdna_test_results"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    # Test information
    test_date = Column(DateTime(timezone=True), nullable=False, index=True)
    test_lab = Column(String, default="Signatera")
    result_file_name = Column(String, nullable=True)
    notes = Column(Text, nullable=True)
    
    # Timestamps
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationship
    user = relationship("User", backref="ctdna_tests")
    detected_markers = relationship("DetectedMarker", back_populates="test_result", cascade="all, delete-orphan")

class DetectedMarker(Base):
    __tablename__ = "detected_markers"
    
    id = Column(Integer, primary_key=True, index=True)
    test_result_id = Column(Integer, ForeignKey("ctdna_test_results.id"), nullable=False, index=True)
    marker_id = Column(Integer, ForeignKey("genetic_markers.id"), nullable=False, index=True)
    
    # Detection data
    detected = Column(Boolean, default=True, nullable=False)
    variant_allele_frequency = Column(Float, nullable=True)  # VAF if available
    
    # Relationships
    test_result = relationship("CTDNATestResult", back_populates="detected_markers")
    marker = relationship("GeneticMarker", backref="detections")

