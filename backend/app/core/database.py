"""
Database setup and operations for No Colon, Still Rollin'
Using SQLAlchemy with SQLite
"""
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict, Any
import json

from config import DATABASE_PATH


class Database:
    """Database manager for the application"""

    def __init__(self, db_path: str = DATABASE_PATH):
        self.db_path = db_path
        self.conn = None
        self._ensure_database_exists()

    def _ensure_database_exists(self):
        """Create database and tables if they don't exist"""
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row  # Return rows as dictionaries
        self._create_tables()

    def _create_tables(self):
        """Create all necessary tables"""
        cursor = self.conn.cursor()

        # Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT,
                date_of_birth TEXT,
                cancer_type TEXT DEFAULT 'colon',
                diagnosis_date TEXT,
                current_treatment TEXT,
                medications TEXT,  -- JSON array
                allergies TEXT,    -- JSON array
                current_weight_lbs REAL NOT NULL,
                target_weight_lbs REAL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Foods table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS foods (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                common_names TEXT,  -- JSON array
                active_compounds TEXT,  -- JSON array of compounds
                net_carbs_per_100g REAL DEFAULT 0,
                protein_per_100g REAL DEFAULT 0,
                fat_per_100g REAL DEFAULT 0,
                fiber_per_100g REAL DEFAULT 0,
                cancer_types TEXT,  -- JSON array
                mechanisms TEXT,    -- JSON array
                best_preparation TEXT,
                preparation_notes TEXT,
                max_daily_amount_grams REAL DEFAULT 1000,
                side_effects TEXT,  -- JSON array
                contraindications TEXT,  -- JSON array
                evidence_level TEXT,
                pubmed_ids TEXT,  -- JSON array
                last_updated TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Research studies table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS research_studies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pubmed_id TEXT UNIQUE NOT NULL,
                title TEXT NOT NULL,
                authors TEXT,
                journal TEXT,
                year INTEGER,
                abstract TEXT,
                study_type TEXT,
                food_studied TEXT,
                compound_studied TEXT,
                cancer_type TEXT,
                dose_amount REAL,
                dose_unit TEXT,
                dose_frequency TEXT,
                subject_weight_kg REAL,
                results_summary TEXT,
                efficacy_percentage REAL,
                doi TEXT,
                url TEXT,
                date_fetched TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Weight records table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS weight_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                date TEXT NOT NULL,
                weight_lbs REAL NOT NULL,
                notes TEXT,
                followed_protocol BOOLEAN DEFAULT 1,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)

        # Daily protocols table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS daily_protocols (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                date TEXT NOT NULL,
                weight_lbs REAL NOT NULL,
                foods TEXT NOT NULL,  -- JSON array of ProtocolFood objects
                total_net_carbs REAL DEFAULT 0,
                total_protein REAL DEFAULT 0,
                total_fat REAL DEFAULT 0,
                total_calories REAL DEFAULT 0,
                generated_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id),
                UNIQUE(user_id, date)
            )
        """)

        # Compliance records table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS compliance_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                protocol_id INTEGER NOT NULL,
                date TEXT NOT NULL,
                foods_consumed TEXT,  -- JSON array
                adherence_percentage REAL DEFAULT 0,
                missed_foods TEXT,  -- JSON array
                notes TEXT,
                recorded_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (protocol_id) REFERENCES daily_protocols (id)
            )
        """)

        # Medications table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS medications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                generic_name TEXT,
                dosage TEXT,
                frequency TEXT,
                food_interactions TEXT,  -- JSON array
                interaction_severity TEXT,
                interaction_notes TEXT,
                source_url TEXT,
                last_checked TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)

        # Safety alerts table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS safety_alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                alert_type TEXT NOT NULL,
                severity TEXT NOT NULL,
                message TEXT NOT NULL,
                food_or_medication TEXT,
                date_triggered TEXT DEFAULT CURRENT_TIMESTAMP,
                acknowledged BOOLEAN DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)

        # Create indexes for common queries
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_weight_records_user_date
            ON weight_records(user_id, date)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_protocols_user_date
            ON daily_protocols(user_id, date)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_compliance_user_date
            ON compliance_records(user_id, date)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_research_food
            ON research_studies(food_studied, cancer_type)
        """)

        self.conn.commit()

    # User operations
    def create_user(self, user_data: Dict[str, Any]) -> int:
        """Create a new user"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO users (
                name, email, date_of_birth, cancer_type, diagnosis_date,
                current_treatment, medications, allergies, current_weight_lbs,
                target_weight_lbs
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            user_data.get('name'),
            user_data.get('email'),
            user_data.get('date_of_birth'),
            user_data.get('cancer_type', 'colon'),
            user_data.get('diagnosis_date'),
            user_data.get('current_treatment'),
            json.dumps(user_data.get('medications', [])),
            json.dumps(user_data.get('allergies', [])),
            user_data.get('current_weight_lbs'),
            user_data.get('target_weight_lbs'),
        ))
        self.conn.commit()
        return cursor.lastrowid

    def get_user(self, user_id: int = None, name: str = None) -> Optional[Dict]:
        """Get user by ID or name"""
        cursor = self.conn.cursor()
        if user_id:
            cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        elif name:
            cursor.execute("SELECT * FROM users WHERE name = ?", (name,))
        else:
            return None

        row = cursor.fetchone()
        if row:
            user = dict(row)
            user['medications'] = json.loads(user['medications']) if user['medications'] else []
            user['allergies'] = json.loads(user['allergies']) if user['allergies'] else []
            return user
        return None

    def update_user_weight(self, user_id: int, weight_lbs: float):
        """Update user's current weight"""
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE users
            SET current_weight_lbs = ?, updated_at = ?
            WHERE id = ?
        """, (weight_lbs, datetime.now().isoformat(), user_id))
        self.conn.commit()

    # Weight tracking
    def add_weight_record(self, user_id: int, weight_lbs: float,
                         followed_protocol: bool = True, notes: str = ""):
        """Add a weight measurement"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO weight_records (user_id, date, weight_lbs, followed_protocol, notes)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, datetime.now().isoformat(), weight_lbs, followed_protocol, notes))
        self.conn.commit()

        # Also update user's current weight
        self.update_user_weight(user_id, weight_lbs)

    def get_weight_history(self, user_id: int, limit: int = 52) -> List[Dict]:
        """Get weight history (default last year of weekly weigh-ins)"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM weight_records
            WHERE user_id = ?
            ORDER BY date DESC
            LIMIT ?
        """, (user_id, limit))
        return [dict(row) for row in cursor.fetchall()]

    # Food operations
    def add_food(self, food_data: Dict[str, Any]) -> int:
        """Add a new food to the database"""
        cursor = self.conn.cursor()

        # Convert lists/dicts to JSON
        for field in ['common_names', 'active_compounds', 'cancer_types',
                     'mechanisms', 'side_effects', 'contraindications', 'pubmed_ids']:
            if field in food_data and isinstance(food_data[field], (list, dict)):
                food_data[field] = json.dumps(food_data[field])

        cursor.execute("""
            INSERT INTO foods (
                name, common_names, active_compounds,
                net_carbs_per_100g, protein_per_100g, fat_per_100g, fiber_per_100g,
                cancer_types, mechanisms, best_preparation, preparation_notes,
                max_daily_amount_grams, side_effects, contraindications,
                evidence_level, pubmed_ids
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            food_data.get('name'),
            food_data.get('common_names'),
            food_data.get('active_compounds'),
            food_data.get('net_carbs_per_100g', 0),
            food_data.get('protein_per_100g', 0),
            food_data.get('fat_per_100g', 0),
            food_data.get('fiber_per_100g', 0),
            food_data.get('cancer_types'),
            food_data.get('mechanisms'),
            food_data.get('best_preparation', 'raw'),
            food_data.get('preparation_notes', ''),
            food_data.get('max_daily_amount_grams', 1000),
            food_data.get('side_effects'),
            food_data.get('contraindications'),
            food_data.get('evidence_level', 'in_vitro'),
            food_data.get('pubmed_ids'),
        ))
        self.conn.commit()
        return cursor.lastrowid

    def get_all_foods(self) -> List[Dict]:
        """Get all foods"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM foods ORDER BY name")
        foods = []
        for row in cursor.fetchall():
            food = dict(row)
            # Parse JSON fields
            for field in ['common_names', 'active_compounds', 'cancer_types',
                         'mechanisms', 'side_effects', 'contraindications', 'pubmed_ids']:
                if food[field]:
                    food[field] = json.loads(food[field])
            foods.append(food)
        return foods

    def get_food_by_name(self, name: str) -> Optional[Dict]:
        """Get a specific food"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM foods WHERE name = ?", (name,))
        row = cursor.fetchone()
        if row:
            food = dict(row)
            for field in ['common_names', 'active_compounds', 'cancer_types',
                         'mechanisms', 'side_effects', 'contraindications', 'pubmed_ids']:
                if food[field]:
                    food[field] = json.loads(food[field])
            return food
        return None

    # Research operations
    def add_research_study(self, study_data: Dict[str, Any]) -> int:
        """Add a research study"""
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO research_studies (
                    pubmed_id, title, authors, journal, year, abstract,
                    study_type, food_studied, compound_studied, cancer_type,
                    dose_amount, dose_unit, dose_frequency, subject_weight_kg,
                    results_summary, efficacy_percentage, doi, url
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                study_data.get('pubmed_id'),
                study_data.get('title'),
                study_data.get('authors'),
                study_data.get('journal'),
                study_data.get('year'),
                study_data.get('abstract'),
                study_data.get('study_type'),
                study_data.get('food_studied'),
                study_data.get('compound_studied'),
                study_data.get('cancer_type'),
                study_data.get('dose_amount'),
                study_data.get('dose_unit'),
                study_data.get('dose_frequency'),
                study_data.get('subject_weight_kg'),
                study_data.get('results_summary'),
                study_data.get('efficacy_percentage'),
                study_data.get('doi'),
                study_data.get('url'),
            ))
            self.conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            # Study already exists (duplicate pubmed_id)
            return -1

    def get_research_for_food(self, food_name: str, cancer_type: str = None) -> List[Dict]:
        """Get research studies for a specific food"""
        cursor = self.conn.cursor()
        if cancer_type:
            cursor.execute("""
                SELECT * FROM research_studies
                WHERE food_studied = ? AND cancer_type = ?
                ORDER BY year DESC
            """, (food_name, cancer_type))
        else:
            cursor.execute("""
                SELECT * FROM research_studies
                WHERE food_studied = ?
                ORDER BY year DESC
            """, (food_name,))
        return [dict(row) for row in cursor.fetchall()]

    # Protocol operations
    def save_daily_protocol(self, protocol_data: Dict[str, Any]) -> int:
        """Save a daily protocol"""
        cursor = self.conn.cursor()

        foods_json = json.dumps(protocol_data.get('foods', []))

        cursor.execute("""
            INSERT OR REPLACE INTO daily_protocols (
                user_id, date, weight_lbs, foods,
                total_net_carbs, total_protein, total_fat, total_calories
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            protocol_data.get('user_id'),
            protocol_data.get('date'),
            protocol_data.get('weight_lbs'),
            foods_json,
            protocol_data.get('total_net_carbs', 0),
            protocol_data.get('total_protein', 0),
            protocol_data.get('total_fat', 0),
            protocol_data.get('total_calories', 0),
        ))
        self.conn.commit()
        return cursor.lastrowid

    def get_protocol_for_date(self, user_id: int, date: str) -> Optional[Dict]:
        """Get protocol for a specific date"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM daily_protocols
            WHERE user_id = ? AND date = ?
        """, (user_id, date))
        row = cursor.fetchone()
        if row:
            protocol = dict(row)
            protocol['foods'] = json.loads(protocol['foods'])
            return protocol
        return None

    # Compliance tracking
    def record_compliance(self, compliance_data: Dict[str, Any]) -> int:
        """Record daily compliance"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO compliance_records (
                user_id, protocol_id, date, foods_consumed,
                adherence_percentage, missed_foods, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            compliance_data.get('user_id'),
            compliance_data.get('protocol_id'),
            compliance_data.get('date'),
            json.dumps(compliance_data.get('foods_consumed', [])),
            compliance_data.get('adherence_percentage', 0),
            json.dumps(compliance_data.get('missed_foods', [])),
            compliance_data.get('notes', ''),
        ))
        self.conn.commit()
        return cursor.lastrowid

    def get_compliance_history(self, user_id: int, days: int = 30) -> List[Dict]:
        """Get compliance history"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM compliance_records
            WHERE user_id = ?
            ORDER BY date DESC
            LIMIT ?
        """, (user_id, days))
        records = []
        for row in cursor.fetchall():
            record = dict(row)
            record['foods_consumed'] = json.loads(record['foods_consumed'])
            record['missed_foods'] = json.loads(record['missed_foods'])
            records.append(record)
        return records

    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
