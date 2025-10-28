"""Add medication log and hydration tracking tables + update health photos"""
import sys
import os
import sqlite3

# Add the backend directory to the path
backend_dir = '/Users/JDKristenson/Desktop/Manual Library/No Colon Still Rollin/backend'
sys.path.insert(0, backend_dir)
sys.path.insert(0, os.path.join(backend_dir, 'app', 'core'))

from config import DATABASE_PATH

def add_new_tables():
    """Add medication_log, hydration_log, and update health_photos"""

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    print("🔧 Updating database schema...\n")

    # 1. Add columns to health_photos table
    try:
        print("  📸 Updating health_photos table...")
        cursor.execute("""
            ALTER TABLE health_photos ADD COLUMN tags TEXT DEFAULT '[]'
        """)
        print("    ✅ Added 'tags' column")
    except sqlite3.OperationalError:
        print("    ⚠️  'tags' column already exists")

    try:
        cursor.execute("""
            ALTER TABLE health_photos ADD COLUMN archived BOOLEAN DEFAULT 0
        """)
        print("    ✅ Added 'archived' column")
    except sqlite3.OperationalError:
        print("    ⚠️  'archived' column already exists")

    # 2. Create medication_log table
    try:
        print("\n  💊 Creating medication_log table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS medication_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                medication_id INTEGER NOT NULL,
                date TEXT NOT NULL,
                time TEXT NOT NULL,
                dosage TEXT,
                taken BOOLEAN DEFAULT 1,
                notes TEXT,
                logged_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (medication_id) REFERENCES medications (id)
            )
        """)
        print("    ✅ Created medication_log table")

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_medication_log_user_date
            ON medication_log(user_id, date)
        """)
        print("    ✅ Created index on medication_log")
    except Exception as e:
        print(f"    ⚠️  Error creating medication_log: {e}")

    # 3. Create hydration_log table
    try:
        print("\n  💧 Creating hydration_log table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS hydration_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                date TEXT NOT NULL,
                time TEXT NOT NULL,
                amount_oz REAL DEFAULT 8.0,
                logged_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)
        print("    ✅ Created hydration_log table")

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_hydration_log_user_date
            ON hydration_log(user_id, date)
        """)
        print("    ✅ Created index on hydration_log")
    except Exception as e:
        print(f"    ⚠️  Error creating hydration_log: {e}")

    # 4. Create hydration_goals table
    try:
        print("\n  🎯 Creating hydration_goals table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS hydration_goals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL UNIQUE,
                daily_goal_oz REAL DEFAULT 64.0,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)
        print("    ✅ Created hydration_goals table")

        # Set default goal for Jesse
        cursor.execute("""
            INSERT OR IGNORE INTO hydration_goals (user_id, daily_goal_oz)
            VALUES (1, 64.0)
        """)
        print("    ✅ Set default goal (64 oz) for Jesse")
    except Exception as e:
        print(f"    ⚠️  Error creating hydration_goals: {e}")

    conn.commit()
    conn.close()

    print("\n✅ Database schema updated successfully!")
    print("\nNew features added:")
    print("  • Health photo tagging (color, consistency, blood, etc.)")
    print("  • Health photo archiving")
    print("  • Medication log tracking")
    print("  • Hydration tracker (8oz cups)")
    print("  • Adjustable daily hydration goal")

if __name__ == "__main__":
    add_new_tables()
