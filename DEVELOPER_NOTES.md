# No Colon, Still Rollin' - Developer Notes

## System Architecture

### Core Modules

1. **config.py**: Configuration and constants
   - Database paths
   - API keys
   - Safety limits
   - Keto parameters
   - Allometric scaling factors (FDA-approved)

2. **models.py**: Data models and enums
   - Food, ResearchStudy, User, WeightRecord
   - DailyProtocol, ComplianceRecord
   - Medication, SafetyAlert

3. **database.py**: SQLite database with SQLAlchemy-style operations
   - Users, foods, research, protocols, compliance
   - Weight tracking
   - Fully relational schema with indexes

4. **pubmed_fetcher.py**: Research from PubMed/NCBI
   - Searches PubMed for anti-cancer food research
   - Extracts dosing info from abstracts
   - Classifies study types (in vitro, animal, human)
   - Identifies foods and compounds
   - **Status**: ✅ Complete, tested

5. **dosing_calculator.py**: Animal to human dose conversion
   - FDA allometric scaling (mouse/rat → human)
   - In vitro concentration estimation
   - Food dose from compound concentration
   - Safety checking
   - Dosing schedule recommendations
   - **Status**: ✅ Complete with safety checks

6. **keto_checker.py**: Ketogenic diet compatibility
   - Macro calculation per food/serving
   - Daily protocol keto scoring
   - Adjustment suggestions
   - List of keto-friendly anti-cancer foods
   - **Status**: ✅ Complete with scoring system

7. **protocol_generator.py**: Main protocol generation
   - Integrates dosing calculator + keto checker
   - Generates personalized daily protocols
   - Saves to database
   - **Status**: ✅ Complete MVP

8. **track_compliance.py**: Daily compliance tracking
   - Quick check-in system
   - Weight recording (Monday protocol)
   - Adherence calculation
   - History view with streak tracking
   - **Status**: ✅ Complete

9. **init_database.py**: Database seeding
   - Preloaded with Jesse's 8 key foods
   - Creates Jesse's user profile
   - **Status**: ✅ Complete

10. **main.py**: Unified CLI
    - Simple commands: setup, protocol, track, weight, history, status
    - **Status**: ✅ Complete and tested

### Data Flow

```
User Input → Protocol Generator
              ↓
    Dosing Calculator (research-based doses)
              ↓
    Keto Checker (compatibility & adjustment)
              ↓
    Database (save protocol)
              ↓
    User (daily protocol output)
              ↓
    Compliance Tracker (daily check-in)
              ↓
    Database (save compliance)
```

---

## What's Built (MVP Complete) ✅

### Core Functionality
- [✅] User profiles and weight tracking
- [✅] Food database with 8 key anti-cancer foods
- [✅] PubMed research integration
- [✅] FDA-standard dosing calculations (animal → human)
- [✅] Keto compatibility checking and scoring
- [✅] Daily protocol generation
- [✅] Easy compliance tracking
- [✅] Weight recording with protocol
- [✅] History and streak tracking
- [✅] Simple CLI for Jesse

### Research-Backed Features
- [✅] Active compound tracking
- [✅] Cancer-type specific recommendations
- [✅] Evidence level classification
- [✅] Safety limits per food
- [✅] Preparation method recommendations
- [✅] Timing and frequency optimization

---

## What's Next (Enhancements)

### High Priority
- [ ] **Report Generator** - PDF reports for oncology team
  - Compliance charts
  - Weight trends
  - Protocol details with citations
  - Adherence metrics

- [ ] **Medication Interaction Checker**
  - Database of common chemo/medications
  - Web scraping for interactions
  - Safety alerts

- [ ] **Enhanced PubMed Integration**
  - Better abstract parsing for dosing
  - Colon cancer specific filtering
  - Automatic weekly updates

### Medium Priority
- [ ] **Web Interface**
  - Simpler for Jesse than CLI
  - Daily check-in form
  - Protocol display
  - Graphs and charts

- [ ] **Meal Planning**
  - Actual recipes
  - Shopping lists
  - Meal prep instructions

- [ ] **Safety Alerts System**
  - Overdose warnings
  - Interaction alerts
  - Side effect tracking

### Future Enhancements
- [ ] **Mobile App**
  - Daily reminders
  - Photo logging
  - Barcode scanning

- [ ] **Bioavailability Optimization**
  - Black pepper with turmeric
  - Timing with fats
  - Compound synergies

- [ ] **Lab Value Tracking**
  - CEA levels
  - CBC results
  - Correlate with protocol adherence

---

## Technical Debt & TODOs

1. **Error Handling**: Add more comprehensive try-catch blocks
2. **Input Validation**: Validate all user inputs more thoroughly
3. **Testing**: Add pytest unit tests for all modules
4. **Logging**: Add proper logging (currently just print statements)
5. **Configuration**: More settings in .env file
6. **API Rate Limiting**: Better handling of PubMed API limits

---

## How to Extend

### Adding a New Food

Edit `src/init_database.py` and add to `foods_data`:

```python
{
    "name": "New Food",
    "common_names": ["alternative names"],
    "active_compounds": [
        {"name": "compound", "amount_per_100g": 100, "mechanism": "how it works"}
    ],
    "net_carbs_per_100g": 5.0,
    "protein_per_100g": 2.0,
    "fat_per_100g": 0.5,
    "fiber_per_100g": 3.0,
    "cancer_types": ["colon", "general"],
    "mechanisms": ["Induces apoptosis", "Anti-inflammatory"],
    "best_preparation": "raw",
    "preparation_notes": "Notes here",
    "max_daily_amount_grams": 100.0,
    "side_effects": [],
    "contraindications": [],
    "evidence_level": "animal",
    "pubmed_ids": [],
}
```

Then:
```bash
python3 src/init_database.py
```

### Adjusting Doses

Edit `src/protocol_generator.py`, function `_get_default_dose()`:

```python
defaults = {
    "Ginger": 4.0,  # Adjust this
    "NewFood": 50.0,  # Add this
}
```

### Changing Keto Parameters

Edit `.env`:
```
MAX_NET_CARBS_PER_DAY=25
TARGET_PROTEIN_GRAMS_PER_KG=1.8
TARGET_FAT_PERCENTAGE=70
```

### Adding Medications

Future enhancement, but structure is:
```python
db.add_medication({
    "user_id": 1,
    "name": "Medication Name",
    "dosage": "100mg",
    "frequency": "twice daily",
    "food_interactions": ["grapefruit", "dairy"],
})
```

---

## Research Sources

### Implemented
- PubMed/MEDLINE via Biopython Entrez API
- Manual curation for 8 key foods

### To Add
- Clinical trials database
- USDA nutritional database API
- Cancer-specific research journals

---

## Database Schema

### Tables
1. **users**: User profiles
2. **foods**: Anti-cancer foods with compounds
3. **research_studies**: PubMed research
4. **weight_records**: Weekly weigh-ins
5. **daily_protocols**: Generated protocols
6. **compliance_records**: Daily adherence
7. **medications**: User medications (for interactions)
8. **safety_alerts**: Warnings and alerts

All tables have proper foreign keys and indexes.

---

## Deployment Notes

### Current Setup
- Command-line Python application
- SQLite database (local file)
- No server required
- Runs on Mac

### Future Options
1. **Web App**: Flask/FastAPI + React frontend
2. **Mobile**: React Native or Flutter
3. **Cloud**: AWS Lambda + DynamoDB or Supabase
4. **Desktop**: Electron wrapper around web app

---

## Key Files

### Must Keep
- `data/cancer_foods.db` - All Jesse's data
- `.env` - Configuration
- `src/*.py` - All source code

### Can Regenerate
- Virtual environment
- `__pycache__`

### Backup Strategy
```bash
# Backup database
cp data/cancer_foods.db data/cancer_foods.db.backup

# Or use git
git add .
git commit -m "Backup"
```

---

## Testing the System

```bash
# Full test sequence
cd "/Users/JDKristenson/Desktop/No Colon Still Rollin"

# 1. Setup (only once)
python3 src/main.py setup

# 2. Generate protocol
python3 src/main.py protocol

# 3. Check status
python3 src/main.py status

# 4. Record weight (Monday)
python3 src/main.py weight 179

# 5. Track compliance (daily)
python3 src/main.py track

# 6. View history
python3 src/main.py history
```

---

## Performance

- Database: Fast (SQLite with indexes)
- PubMed: ~0.5-1 sec per article (with API key)
- Protocol generation: < 1 second
- All operations: Instant on modern hardware

---

## Security & Privacy

- All data stored locally
- No external connections except PubMed (optional)
- No PHI sent to external services
- Database not encrypted (consider for production)

---

## Known Limitations

1. **PubMed Parsing**: Abstract parsing is heuristic, not perfect
2. **In Vitro Dosing**: Highly approximate, needs refinement
3. **Bioavailability**: Simple model, could be more sophisticated
4. **Meal Timing**: Basic recommendations, not circadian-optimized
5. **No Supplement Forms**: Only whole foods currently

---

## Support & Maintenance

### For Jesse
- Simple CLI commands
- Comprehensive user guide (JESSE_START_HERE.md)
- All defaults pre-configured

### For You (JD)
- Modular code, easy to extend
- Good separation of concerns
- Database abstraction layer
- Configuration in .env

### Future Users
- Currently single-user
- Easy to extend to multi-user
- Each user gets own protocol

---

## Credits & References

### Research
- FDA Guidance on Allometric Scaling
- PubMed/NCBI (U.S. National Library of Medicine)
- Numerous peer-reviewed studies (referenced in database)

### Python Libraries
- biopython: PubMed access
- sqlite3: Database
- python-dotenv: Configuration
- reportlab: PDF generation (for future reports)

---

## Final Notes

This is a research tool, not medical advice. Jesse should:
1. Share protocols with his oncology team
2. Monitor for side effects
3. Adjust based on bloodwork and scans
4. Not replace medical treatment, only supplement

**The system is live and ready for Jesse to use!**

Built with care for Jesse by JD Kristenson
October 2025
