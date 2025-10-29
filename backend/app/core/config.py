"""
Configuration module for Cancer Fighting Foods Protocol Generator
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from project root
# Look for .env file in the project root (3 levels up from this file)
env_path = Path(__file__).parent.parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# Project paths - relative to the backend directory
PROJECT_ROOT = Path(__file__).parent.parent.parent  # Points to backend/
DATA_DIR = PROJECT_ROOT / "app" / "core" / "data"
REPORTS_DIR = PROJECT_ROOT / "app" / "core" / "reports"

# Ensure directories exist
DATA_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

# Database configuration
# Support both SQLite (local/Replit) and PostgreSQL (Vercel)

# PostgreSQL connection for production (Vercel, etc.)
DATABASE_URL = os.getenv("DATABASE_URL", "")  # PostgreSQL connection string

# SQLite path for local/Replit
DATABASE_PATH = os.getenv("DATABASE_PATH")
if DATABASE_PATH:
    # If DATABASE_PATH is relative, make it relative to project root
    db_path = Path(DATABASE_PATH)
    if not db_path.is_absolute():
        DATABASE_PATH = str(PROJECT_ROOT.parent / DATABASE_PATH)
else:
    # Default location for local development
    DATABASE_PATH = str(DATA_DIR / "cancer_foods.db")

# Database type detection
DATABASE_TYPE = "postgresql" if DATABASE_URL else "sqlite"

# NCBI/PubMed API
NCBI_EMAIL = os.getenv("NCBI_EMAIL", "")
NCBI_API_KEY = os.getenv("NCBI_API_KEY", "")

if not NCBI_EMAIL:
    print("⚠️  Warning: NCBI_EMAIL not set in .env file")

# User defaults
DEFAULT_USER = os.getenv("DEFAULT_USER", "jesse")
DEFAULT_WEIGHT_LBS = float(os.getenv("DEFAULT_WEIGHT_LBS", "179"))

# Dosing safety limits (grams per day)
SAFETY_LIMITS = {
    "ginger": float(os.getenv("MAX_GINGER_GRAMS_PER_DAY", "6")),
    "garlic": float(os.getenv("MAX_GARLIC_CLOVES_PER_DAY", "4")),  # cloves
    "turmeric": float(os.getenv("MAX_TURMERIC_GRAMS_PER_DAY", "8")),
    "curcumin": 12,  # grams (from turmeric extract)
    "green_tea_extract": 9,  # grams EGCG
    "cruciferous_vegetables": 500,  # grams (no real upper limit)
}

# Keto parameters
KETO_CONFIG = {
    "max_net_carbs_per_day": int(os.getenv("MAX_NET_CARBS_PER_DAY", "20")),
    "target_protein_g_per_kg": float(os.getenv("TARGET_PROTEIN_GRAMS_PER_KG", "1.6")),
    "target_fat_percentage": int(os.getenv("TARGET_FAT_PERCENTAGE", "75")),
}

# Allometric scaling factors for dosing conversion
# Mouse to human: dose_human = dose_mouse × (weight_human / weight_mouse) ^ 0.67
# Rat to human: dose_human = dose_rat × (weight_human / weight_rat) ^ 0.67
ALLOMETRIC_SCALING = {
    "mouse_to_human": 0.08,  # FDA factor
    "rat_to_human": 0.16,    # FDA factor
    "standard_mouse_weight_kg": 0.02,  # 20g
    "standard_rat_weight_kg": 0.2,     # 200g
}

# PubMed search terms for anti-cancer foods
CANCER_SEARCH_TERMS = [
    "cancer AND (ginger OR gingerol)",
    "cancer AND (garlic OR allicin)",
    "cancer AND (turmeric OR curcumin)",
    "cancer AND (broccoli OR sulforaphane)",
    "cancer AND (cauliflower OR cruciferous)",
    "cancer AND (kale OR glucosinolates)",
    "cancer AND (brussels sprouts)",
    "cancer AND (green tea OR EGCG)",
    "cancer AND (berries OR anthocyanins)",
    "cancer AND (omega-3 OR fish oil)",
    "cancer AND ketogenic diet",
    "colon cancer AND diet",
    "colorectal cancer AND nutrition",
]

# Weigh-in protocol
WEIGHIN_PROTOCOL = {
    "day": "Monday",
    "time": "morning",
    "instructions": "Upon first waking, naked, before any food or water",
}

# Report settings
REPORT_SETTINGS = {
    "compliance_weeks": 4,  # Default weeks to include in reports
    "min_adherence_percentage": 80,  # Flag if below this
}
