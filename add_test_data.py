#!/usr/bin/env python3
"""Add test compliance data for demo"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from database import Database
from datetime import datetime, timedelta

db = Database()

# Get Jesse's user and protocol
user = db.get_user(name='Jesse Mills')
protocol = db.get_protocol_for_date(user['id'], '2025-10-28')

# Add a few fake compliance records for testing
dates = [
    (datetime.now() - timedelta(days=i)).date().isoformat()
    for i in range(5, 0, -1)
]

adherences = [85, 95, 100, 80, 90]  # Realistic adherence percentages
notes_list = [
    "Felt good, slight heartburn from garlic",
    "Perfect day, all foods on time",
    "100% adherence! Feeling strong",
    "Missed kale, forgot to buy it",
    "Good day overall"
]

for date_str, adherence, notes in zip(dates, adherences, notes_list):
    compliance_data = {
        'user_id': user['id'],
        'protocol_id': protocol['id'] if protocol else 1,
        'date': date_str,
        'foods_consumed': [
            {'food': 'Ginger', 'percentage': adherence},
            {'food': 'Garlic', 'percentage': adherence},
            {'food': 'Turmeric', 'percentage': adherence},
        ],
        'adherence_percentage': adherence,
        'missed_foods': [] if adherence >= 90 else ['Kale'],
        'notes': notes
    }
    db.record_compliance(compliance_data)
    print(f"✅ Added compliance record for {date_str}: {adherence}%")

print(f"\n✅ Added {len(dates)} test compliance records")
db.close()
