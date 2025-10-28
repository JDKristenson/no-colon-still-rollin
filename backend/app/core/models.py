"""
Data models for Cancer Fighting Foods Protocol Generator
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict
from enum import Enum


class EvidenceLevel(Enum):
    """Strength of scientific evidence"""
    IN_VITRO = "in_vitro"  # Petri dish studies
    ANIMAL = "animal"       # Mouse/rat studies
    HUMAN_OBSERVATIONAL = "human_observational"  # Population studies
    HUMAN_CLINICAL = "human_clinical"  # Clinical trials
    META_ANALYSIS = "meta_analysis"  # Multiple studies combined


class PreparationMethod(Enum):
    """How food should be prepared"""
    RAW = "raw"
    COOKED = "cooked"
    STEAMED = "steamed"
    PICKLED = "pickled"
    FERMENTED = "fermented"
    POWDERED = "powdered"
    EXTRACT = "extract"
    JUICE = "juice"


@dataclass
class ActiveCompound:
    """A bioactive compound in food"""
    name: str
    amount_per_100g: float  # milligrams
    mechanism: str  # How it fights cancer
    bioavailability: float = 1.0  # 0-1, absorption rate


@dataclass
class Food:
    """An anti-cancer food"""
    id: Optional[int] = None
    name: str = ""
    common_names: List[str] = field(default_factory=list)
    active_compounds: List[ActiveCompound] = field(default_factory=list)

    # Keto compatibility
    net_carbs_per_100g: float = 0.0
    protein_per_100g: float = 0.0
    fat_per_100g: float = 0.0
    fiber_per_100g: float = 0.0

    # Cancer-fighting properties
    cancer_types: List[str] = field(default_factory=list)  # Which cancers it fights
    mechanisms: List[str] = field(default_factory=list)  # How it works

    # Preparation
    best_preparation: PreparationMethod = PreparationMethod.RAW
    preparation_notes: str = ""

    # Safety
    max_daily_amount_grams: float = 1000.0
    side_effects: List[str] = field(default_factory=list)
    contraindications: List[str] = field(default_factory=list)

    # Research backing
    evidence_level: EvidenceLevel = EvidenceLevel.IN_VITRO
    pubmed_ids: List[str] = field(default_factory=list)
    last_updated: datetime = field(default_factory=datetime.now)


@dataclass
class ResearchStudy:
    """A scientific study from PubMed"""
    id: Optional[int] = None
    pubmed_id: str = ""
    title: str = ""
    authors: str = ""
    journal: str = ""
    year: int = 0
    abstract: str = ""

    # Study details
    study_type: EvidenceLevel = EvidenceLevel.IN_VITRO
    food_studied: str = ""
    compound_studied: str = ""
    cancer_type: str = ""

    # Dosing information
    dose_amount: Optional[float] = None
    dose_unit: str = ""
    dose_frequency: str = ""
    subject_weight_kg: Optional[float] = None

    # Results
    results_summary: str = ""
    efficacy_percentage: Optional[float] = None

    # Metadata
    doi: str = ""
    url: str = ""
    date_fetched: datetime = field(default_factory=datetime.now)


@dataclass
class User:
    """A user of the system (e.g., Jesse)"""
    id: Optional[int] = None
    name: str = ""
    email: str = ""
    date_of_birth: Optional[datetime] = None

    # Medical info
    cancer_type: str = "colon"
    diagnosis_date: Optional[datetime] = None
    current_treatment: str = ""
    medications: List[str] = field(default_factory=list)
    allergies: List[str] = field(default_factory=list)

    # Current status
    current_weight_lbs: float = 179.0
    target_weight_lbs: Optional[float] = None

    # Created/updated
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)


@dataclass
class WeightRecord:
    """Weekly weight measurement"""
    id: Optional[int] = None
    user_id: int = 0
    date: datetime = field(default_factory=datetime.now)
    weight_lbs: float = 0.0
    notes: str = ""

    # Protocol validation
    followed_protocol: bool = True  # Naked, morning, before food/water


@dataclass
class DailyProtocol:
    """Daily food protocol for a user"""
    id: Optional[int] = None
    user_id: int = 0
    date: datetime = field(default_factory=datetime.now)
    weight_lbs: float = 179.0

    # Foods and doses
    foods: List['ProtocolFood'] = field(default_factory=list)

    # Macros
    total_net_carbs: float = 0.0
    total_protein: float = 0.0
    total_fat: float = 0.0
    total_calories: float = 0.0

    # Generated
    generated_at: datetime = field(default_factory=datetime.now)


@dataclass
class ProtocolFood:
    """A food in a daily protocol with specific dosing"""
    food_name: str = ""
    amount_grams: float = 0.0
    preparation: PreparationMethod = PreparationMethod.RAW

    # Timing
    times_per_day: int = 1
    timing_notes: str = ""  # e.g., "with meals", "morning and evening"

    # Rationale
    reason: str = ""  # Why this food/dose
    evidence: str = ""  # Study citation

    # Nutrients
    net_carbs: float = 0.0
    protein: float = 0.0
    fat: float = 0.0


@dataclass
class ComplianceRecord:
    """Daily compliance tracking"""
    id: Optional[int] = None
    user_id: int = 0
    protocol_id: int = 0
    date: datetime = field(default_factory=datetime.now)

    # What was actually consumed
    foods_consumed: List[Dict[str, any]] = field(default_factory=list)

    # Compliance metrics
    adherence_percentage: float = 0.0
    missed_foods: List[str] = field(default_factory=list)
    notes: str = ""

    # Recorded at
    recorded_at: datetime = field(default_factory=datetime.now)


@dataclass
class Medication:
    """A medication the user is taking"""
    id: Optional[int] = None
    name: str = ""
    generic_name: str = ""
    dosage: str = ""
    frequency: str = ""

    # Interactions
    food_interactions: List[str] = field(default_factory=list)
    interaction_severity: str = ""  # minor, moderate, severe
    interaction_notes: str = ""

    # Source
    source_url: str = ""
    last_checked: datetime = field(default_factory=datetime.now)


@dataclass
class SafetyAlert:
    """Safety warning or alert"""
    id: Optional[int] = None
    user_id: int = 0
    alert_type: str = ""  # "overdose", "interaction", "side_effect"
    severity: str = ""  # "low", "medium", "high"
    message: str = ""
    food_or_medication: str = ""
    date_triggered: datetime = field(default_factory=datetime.now)
    acknowledged: bool = False
