# Product Requirements Document (PRD)
# No Colon, Still Rollin' - Anti-Cancer Protocol System

**Version:** 2.0.0
**Last Updated:** October 31, 2025
**Product Owner:** JD Kristenson
**Primary User:** Jesse Mills

---

## Executive Summary

**No Colon, Still Rollin'** is a comprehensive web application designed to help cancer patients manage evidence-based anti-cancer food protocols. The system generates personalized daily nutrition plans, provides practical recipes, tracks compliance, monitors health metrics, and ensures safety through research-backed dosing.

**Core Value Proposition:** Make it as easy as possible to get cancer-fighting foods into your body every single day through automated protocol generation, meal planning, and progress tracking.

---

## 1. Product Overview

### 1.1 Purpose

To provide Jesse Mills (and potentially other colon cancer patients) with a medical-grade system for:
- Managing a personalized anti-cancer food protocol
- Tracking weight, compliance, medications, and hydration
- Accessing evidence-based dosing recommendations
- Simplifying meal planning and grocery shopping
- Monitoring health progress over time

### 1.2 Target Users

**Primary User:** Jesse Mills
- Colon cancer patient
- Needs daily protocol guidance
- Wants simple compliance tracking
- Requires keto-compatible meal plans

**Secondary Users (Future):**
- Other cancer patients
- Caregivers
- Healthcare providers

### 1.3 Key Success Metrics

- Daily protocol adherence rate ≥ 80%
- User logs weight weekly
- User completes daily check-ins
- System generates keto-compatible protocols
- All 9 anti-cancer foods incorporated daily

---

## 2. Core Features & Functionality

### 2.1 Dashboard

**Purpose:** Provide at-a-glance health status and progress overview

**Key Elements:**
- Current weight display
- 7-day adherence percentage
- Current streak (consecutive days following protocol)
- Weight trend chart (last 30 days)
- Quick stats summary

**User Stories:**
- As a user, I want to see my current health status immediately when I open the app
- As a user, I want to track my compliance streak to stay motivated
- As a user, I want to visualize my weight trend over time

### 2.2 Protocol Generator

**Purpose:** Generate personalized daily anti-cancer food protocols based on user weight and cancer type

**Key Features:**

1. **Personalized Dosing**
   - Uses FDA allometric scaling for human-equivalent doses
   - Calculates amounts based on current weight
   - Ensures safety limits are not exceeded
   - Adjusts for keto compatibility

2. **The 9 Anti-Cancer Foods:**
   - **Ginger** (4g/day) - Anti-inflammatory, anti-tumor
   - **Garlic** (10g/day) - Induces apoptosis in cancer cells
   - **Turmeric** (5g/day) - Powerful anti-inflammatory
   - **Broccoli** (200g/day) - Activates detox enzymes
   - **Cauliflower** (150g/day) - Cancer prevention
   - **Kale** (100g/day) - Antioxidant powerhouse
   - **Brussels Sprouts** (150g/day) - High in sulforaphane
   - **Green Tea** (750g/day = 3-4 cups) - EGCG anti-cancer compound
   - **Colon Support Herbal Tea** (16g/day = 2 cups) - Digestive support

3. **Protocol Display:**
   - Food name and amount (grams)
   - Timing (when to consume)
   - Preparation method
   - Cancer-fighting mechanism
   - Safety notes
   - Macronutrient breakdown

4. **Keto Compatibility Checking:**
   - Calculates net carbs, protein, fat
   - Ensures < 50g net carbs per day
   - Maintains 60-75% fat, 15-30% protein, 5-10% carbs ratio
   - Auto-adjusts high-carb foods if needed

**User Stories:**
- As a user, I want to generate today's protocol based on my current weight
- As a user, I want to know exactly how much of each food to eat
- As a user, I want the protocol to be keto-compatible
- As a user, I want to understand why each food fights cancer

**API Endpoints:**
- `GET /api/protocol/today` - Get today's protocol
- `POST /api/protocol/generate` - Generate new protocol

### 2.3 Meal Planner

**Purpose:** Translate protocol requirements into practical, easy-to-follow recipes

**Key Features:**

1. **7 Practical Recipes:**
   - Morning Colon Support Tea
   - Anti-Cancer Power Smoothie
   - Garlic Cauliflower Rice Bowl
   - Roasted Brussels Sprouts with Turmeric
   - Kale & Ginger Stir-Fry
   - Green Tea (brewing instructions)
   - Evening Colon Support Tea

2. **Weekly Shopping List:**
   - Organized by category (Fresh, Spices, Pantry)
   - Exact quantities needed
   - Keto-friendly ingredients

3. **Sample Daily Plan:**
   - Morning routine
   - Lunch suggestions
   - Afternoon tea schedule
   - Dinner options
   - Evening routine

4. **Recipe Details:**
   - Ingredients with amounts
   - Step-by-step instructions
   - Preparation time
   - Which protocol foods are included
   - Nutritional information

**User Stories:**
- As a user, I want recipes that incorporate all my protocol foods
- As a user, I want a shopping list so I know exactly what to buy
- As a user, I want a sample daily schedule to follow
- As a user, I want detailed cooking instructions

### 2.4 Compliance Tracking (Check-In)

**Purpose:** Daily progress tracking to build adherence and streaks

**Key Features:**

1. **Daily Checklist:**
   - List of today's protocol foods
   - Checkbox for each food consumed
   - Progress bar showing completion percentage
   - Motivational messages

2. **Compliance Metrics:**
   - Current streak (consecutive days)
   - 7-day rolling adherence average
   - Total days tracked
   - Missed foods list

3. **Streak System:**
   - Tracks consecutive days of 100% compliance
   - Visual celebration when milestones hit
   - Resets when protocol not followed

**User Stories:**
- As a user, I want to check off foods as I eat them throughout the day
- As a user, I want to see my adherence streak to stay motivated
- As a user, I want to know what I missed if I didn't hit 100%

**API Endpoints:**
- `GET /api/compliance/stats` - Get compliance statistics
- `POST /api/compliance/record` - Record daily compliance

### 2.5 Weight Tracking

**Purpose:** Monitor weight trends and protocol effectiveness

**Key Features:**

1. **Weight Entry:**
   - Date and time of measurement
   - Weight in pounds
   - "Followed protocol" checkbox
   - Notes field

2. **Weight Protocol:**
   - Weigh naked
   - First thing in the morning
   - Before eating or drinking
   - Weekly recommended

3. **Weight History:**
   - Table view of all weight entries
   - Trend chart (line graph)
   - Date, weight, followed protocol indicator
   - Notes column

4. **Trend Visualization:**
   - 30-day, 90-day, all-time views
   - Weight change indicators (up/down)
   - Goal weight line (if set)

**User Stories:**
- As a user, I want to record my weight weekly
- As a user, I want to see if the protocol is working (weight trend)
- As a user, I want to add notes about special circumstances
- As a user, I want to filter by measurements where I followed protocol

**API Endpoints:**
- `GET /api/weight/history` - Get weight history
- `POST /api/weight/` - Record new weight

### 2.6 Research Library

**Purpose:** Provide evidence-based research backing for protocol foods

**Key Features:**

1. **Food Database:**
   - All 9 anti-cancer foods
   - Active compounds in each food
   - Mechanisms of action
   - Cancer types targeted
   - Evidence level (in vitro, animal, human observational, clinical trials, meta-analysis)

2. **Research Studies:**
   - PubMed integration
   - Study title, authors, journal, year
   - Abstract
   - Dosing information from studies
   - Efficacy percentages
   - Direct PubMed links

3. **Food Details:**
   - Common names
   - Nutritional information (carbs, protein, fat, fiber)
   - Best preparation method
   - Preparation notes
   - Maximum safe daily amount
   - Side effects
   - Contraindications

**User Stories:**
- As a user, I want to see the research backing for each food
- As a user, I want to understand how each food fights cancer
- As a user, I want to know about potential side effects
- As a user, I want access to original research studies

**API Endpoints:**
- `GET /api/foods/` - Get all foods
- `GET /api/library/research/{food_name}` - Get research for specific food

### 2.7 Health Photos

**Purpose:** Visual progress tracking through photos

**Key Features:**

1. **Photo Upload:**
   - Date-stamped photos
   - Photo type categorization (health, before/after, etc.)
   - Notes field
   - Tags for organization

2. **Photo Gallery:**
   - Chronological view
   - Filter by date, type, tags
   - Archive functionality
   - Delete capability

3. **Photo Management:**
   - View full-size images
   - Add/edit tags
   - Add/edit notes
   - Archive old photos

**User Stories:**
- As a user, I want to track visual progress over time
- As a user, I want to add notes to photos
- As a user, I want to organize photos with tags
- As a user, I want to archive photos without deleting them

**API Endpoints:**
- `GET /api/health-photos/` - Get all photos
- `POST /api/health-photos/upload` - Upload new photo
- `PUT /api/health-photos/{id}` - Update photo metadata
- `DELETE /api/health-photos/{id}` - Delete photo

### 2.8 Medication Tracking

**Purpose:** Track medication schedules and check for food interactions

**Key Features:**

1. **Medication Management:**
   - Add/edit/delete medications
   - Medication name (brand and generic)
   - Dosage and frequency
   - Food interaction warnings
   - Interaction severity levels

2. **Medication Log:**
   - Daily medication checklist
   - Time-stamped logging
   - "Taken" confirmation
   - Skip/miss tracking
   - Notes for each dose

3. **Interaction Alerts:**
   - Check for food-drug interactions
   - Severity indicators (minor, moderate, severe)
   - Detailed interaction notes
   - Source references

**User Stories:**
- As a user, I want to track all my medications in one place
- As a user, I want to log when I take each medication
- As a user, I want to be alerted to food-drug interactions
- As a user, I want to see my medication adherence

**API Endpoints:**
- `GET /api/medications/` - Get all medications
- `POST /api/medications/` - Add medication
- `POST /api/medications/log` - Log medication dose
- `GET /api/medications/log` - Get medication log

### 2.9 Hydration Tracking

**Purpose:** Ensure adequate daily water intake

**Key Features:**

1. **Water Logging:**
   - Quick log buttons (8 oz, 16 oz, custom)
   - Time-stamped entries
   - Daily total calculation
   - Goal progress bar

2. **Hydration Goal:**
   - Customizable daily goal (default 64 oz)
   - Goal adjustment based on weight
   - Visual progress indicator

3. **Hydration History:**
   - Daily logs
   - Weekly averages
   - Goal achievement tracking

**User Stories:**
- As a user, I want to log water intake throughout the day
- As a user, I want to see if I'm hitting my hydration goal
- As a user, I want to track hydration trends over time

**API Endpoints:**
- `POST /api/hydration/log` - Log water intake
- `GET /api/hydration/today` - Get today's hydration log
- `GET /api/hydration/goal` - Get/set hydration goal

### 2.10 Data Export

**Purpose:** Export data for external analysis or backup

**Key Features:**

1. **Export Formats:**
   - CSV (Excel-compatible)
   - JSON (programmatic access)
   - PDF (printable reports)

2. **Export Types:**
   - Weight history
   - Compliance records
   - Medication logs
   - Hydration logs
   - Complete data dump

**User Stories:**
- As a user, I want to export my data for my doctor
- As a user, I want to back up my health data
- As a user, I want to analyze my data in Excel

**API Endpoints:**
- `GET /api/exports/weight` - Export weight data
- `GET /api/exports/compliance` - Export compliance data
- `GET /api/exports/all` - Export all data

---

## 3. Technical Architecture

### 3.1 Technology Stack

**Frontend:**
- **Framework:** React 19.1.1
- **Build Tool:** Vite 7.1.7
- **Language:** TypeScript 5.9.3
- **Styling:** Tailwind CSS 3.4.18
- **State Management:** TanStack Query 5.90.5
- **Routing:** React Router 7.9.4
- **Charts:** Recharts 3.3.0
- **Icons:** Lucide React 0.548.0

**Backend:**
- **Framework:** FastAPI (Python 3.8+)
- **Database:** SQLite 3
- **ORM:** Native sqlite3 (no ORM)
- **Validation:** Pydantic schemas
- **Server:** Uvicorn
- **CORS:** FastAPI CORS middleware

**Deployment:**
- **Platform:** Replit
- **Hosting:** Replit Cloud Run
- **Environment:** Nix-based configuration

### 3.2 Database Schema

**Core Tables:**

1. **users**
   - id (PK)
   - name, email, date_of_birth
   - cancer_type, diagnosis_date, current_treatment
   - medications (JSON), allergies (JSON)
   - current_weight_lbs, target_weight_lbs
   - created_at, updated_at

2. **foods**
   - id (PK)
   - name (UNIQUE)
   - common_names (JSON), active_compounds (JSON)
   - net_carbs_per_100g, protein_per_100g, fat_per_100g, fiber_per_100g
   - cancer_types (JSON), mechanisms (JSON)
   - best_preparation, preparation_notes
   - max_daily_amount_grams
   - side_effects (JSON), contraindications (JSON)
   - evidence_level, pubmed_ids (JSON)
   - last_updated

3. **research_studies**
   - id (PK)
   - pubmed_id (UNIQUE)
   - title, authors, journal, year, abstract
   - study_type, food_studied, compound_studied, cancer_type
   - dose_amount, dose_unit, dose_frequency, subject_weight_kg
   - results_summary, efficacy_percentage
   - doi, url, date_fetched

4. **weight_records**
   - id (PK)
   - user_id (FK)
   - date, weight_lbs
   - notes, followed_protocol
   - Index on (user_id, date)

5. **daily_protocols**
   - id (PK)
   - user_id (FK)
   - date, weight_lbs
   - foods (JSON)
   - total_net_carbs, total_protein, total_fat, total_calories
   - generated_at
   - UNIQUE(user_id, date)
   - Index on (user_id, date)

6. **compliance_records**
   - id (PK)
   - user_id (FK), protocol_id (FK)
   - date, foods_consumed (JSON)
   - adherence_percentage, missed_foods (JSON)
   - notes, recorded_at
   - Index on (user_id, date)

7. **medications**
   - id (PK)
   - user_id (FK)
   - name, generic_name, dosage, frequency
   - food_interactions (JSON), interaction_severity, interaction_notes
   - source_url, last_checked

8. **medication_log**
   - id (PK)
   - user_id (FK), medication_id (FK)
   - date, time, dosage
   - taken, notes, logged_at
   - Index on (user_id, date)

9. **health_photos**
   - id (PK)
   - user_id (FK)
   - date, photo_type, filename, file_path
   - notes, tags (JSON), archived
   - uploaded_at
   - Index on (user_id, date)

10. **hydration_log**
    - id (PK)
    - user_id (FK)
    - date, time, amount_oz
    - logged_at
    - Index on (user_id, date)

11. **hydration_goals**
    - id (PK)
    - user_id (FK, UNIQUE)
    - daily_goal_oz, updated_at

12. **safety_alerts**
    - id (PK)
    - user_id (FK)
    - alert_type, severity, message
    - food_or_medication, date_triggered, acknowledged

### 3.3 API Architecture

**Base URL:** `/api`

**API Documentation:**
- Swagger UI: `/api/docs`
- ReDoc: `/api/redoc`
- OpenAPI JSON: `/api/openapi.json`

**API Routers:**
- `/api/protocol` - Protocol generation
- `/api/weight` - Weight tracking
- `/api/compliance` - Compliance tracking
- `/api/foods` - Food library
- `/api/status` - Dashboard data
- `/api/library` - Research library
- `/api/exports` - Data export
- `/api/health-photos` - Photo management
- `/api/medications` - Medication tracking
- `/api/hydration` - Hydration tracking

**Key Endpoints:**

**Protocol:**
- `GET /api/protocol/today` - Get today's protocol
- `POST /api/protocol/generate` - Generate new protocol for date

**Weight:**
- `GET /api/weight/history` - Get weight history (last 52 weeks)
- `POST /api/weight/` - Record new weight measurement

**Compliance:**
- `GET /api/compliance/stats` - Get adherence stats (7-day avg, streak)
- `POST /api/compliance/record` - Record daily compliance

**Foods:**
- `GET /api/foods/` - Get all foods with nutritional data
- `GET /api/foods/{food_id}` - Get specific food details

**Status:**
- `GET /api/status/` - Get dashboard data (weight, adherence, streak)

**Library:**
- `GET /api/library/foods` - Get food library with research
- `GET /api/library/research/{food_name}` - Get research for food

**Exports:**
- `GET /api/exports/weight?format=csv` - Export weight data
- `GET /api/exports/compliance?format=csv` - Export compliance data
- `GET /api/exports/all?format=json` - Export all data

**Health Photos:**
- `GET /api/health-photos/` - Get all photos
- `POST /api/health-photos/upload` - Upload photo
- `PUT /api/health-photos/{id}` - Update photo metadata
- `DELETE /api/health-photos/{id}` - Delete photo

**Medications:**
- `GET /api/medications/` - Get user medications
- `POST /api/medications/` - Add medication
- `POST /api/medications/log` - Log medication dose
- `GET /api/medications/log` - Get medication log

**Hydration:**
- `POST /api/hydration/log` - Log water intake
- `GET /api/hydration/today` - Get today's log
- `GET /api/hydration/total` - Get today's total
- `GET /api/hydration/goal` - Get hydration goal
- `PUT /api/hydration/goal` - Set hydration goal

### 3.4 Core Algorithms

**1. Dosing Calculator (`dosing_calculator.py`)**
- Calculates human-equivalent doses from animal studies
- Uses FDA allometric scaling formula
- Factors in body surface area and weight
- Ensures safety margins

**2. Keto Compatibility Checker (`keto_checker.py`)**
- Validates macronutrient ratios
- Ensures < 50g net carbs per day
- Checks 60-75% fat, 15-30% protein, 5-10% carbs
- Suggests adjustments if not keto-compatible

**3. Protocol Generator (`protocol_generator.py`)**
- Retrieves relevant foods for cancer type
- Calculates personalized doses based on weight
- Builds dosing schedule (servings per day, timing)
- Checks keto compatibility and adjusts
- Saves protocol to database

**4. Compliance Tracker (`track_compliance.py`)**
- Calculates adherence percentage
- Tracks consecutive day streaks
- Identifies missed foods
- Computes 7-day rolling averages

### 3.5 File Storage

**Health Photos:**
- Location: `backend/uploads/health_photos/`
- Naming: `{user_id}_{timestamp}_{original_filename}`
- Formats: JPG, PNG, HEIC
- Max size: 10 MB
- Metadata stored in database

**Database:**
- Location: `backend/data/protocol.db`
- Backups: Manual export via API
- Size: ~5-10 MB (typical for 1 user, 1 year)

### 3.6 Security Considerations

**Current Implementation:**
- No authentication (single-user app)
- CORS restricted to localhost and Replit domains
- File uploads sanitized and validated
- SQL injection prevented via parameterized queries

**Future Enhancements:**
- User authentication (OAuth, JWT)
- HTTPS enforcement
- Data encryption at rest
- Audit logging
- HIPAA compliance considerations

---

## 4. User Experience

### 4.1 Navigation

**Top Navigation Bar:**
- Logo: "No Colon, Still Rollin'"
- Links: Dashboard | Protocol | Meals | Check-In | Weight | Library | Health | Hydration | Medications

**Layout:**
- Consistent header across all pages
- Max width container (1280px)
- Responsive design (mobile-friendly)
- Clean, medical theme (blues, greens, whites)

### 4.2 Design System

**Color Palette:**
- Primary: Medical blue (#3B82F6)
- Success: Green (#10B981)
- Warning: Yellow (#F59E0B)
- Danger: Red (#EF4444)
- Background: Light gray (#F9FAFB)
- Text: Dark gray (#111827)

**Typography:**
- Font: System font stack (sans-serif)
- Headings: Bold, large
- Body: Regular, readable
- Code/data: Monospace

**Components:**
- Cards with rounded corners and shadows
- Progress bars for compliance/goals
- Line charts for trends
- Tables for data display
- Buttons with hover states
- Form inputs with validation

### 4.3 Responsive Behavior

**Desktop (≥ 1024px):**
- Full navigation in header
- Multi-column layouts
- Side-by-side charts and stats

**Tablet (768px - 1023px):**
- Condensed navigation
- Stacked layouts
- Smaller chart sizes

**Mobile (< 768px):**
- Hamburger menu
- Single-column layouts
- Simplified tables
- Touch-friendly buttons

### 4.4 User Flows

**New User Onboarding:**
1. Land on Dashboard (see welcome message)
2. Navigate to Protocol
3. Generate first protocol
4. View Meals page for recipes
5. Shop for ingredients
6. Daily check-in via Compliance page
7. Weekly weight log

**Daily User Flow:**
1. Open app → Dashboard (see streak, adherence)
2. Protocol → Review today's foods
3. Meals → Follow recipes throughout day
4. Check-In → Mark foods as consumed
5. Optional: Log medications, hydration

**Weekly User Flow:**
1. Weight → Record weekly measurement
2. Dashboard → Review weight trend
3. Meals → Update shopping list
4. Library → Read new research (optional)

---

## 5. Data Models

### 5.1 Food Data Model

```python
{
  "id": 1,
  "name": "Ginger",
  "common_names": ["Ginger root", "Zingiber officinale"],
  "active_compounds": [
    {
      "name": "Gingerol",
      "amount_per_100g": 180.0,
      "mechanism": "Induces apoptosis, anti-inflammatory",
      "bioavailability": 0.8
    }
  ],
  "net_carbs_per_100g": 15.8,
  "protein_per_100g": 1.8,
  "fat_per_100g": 0.8,
  "fiber_per_100g": 2.0,
  "cancer_types": ["colon", "general"],
  "mechanisms": ["Induces apoptosis", "Reduces inflammation", "Inhibits tumor growth"],
  "best_preparation": "raw",
  "preparation_notes": "Grate fresh, add to smoothies or tea",
  "max_daily_amount_grams": 10.0,
  "side_effects": ["Heartburn (rare)", "Stomach upset (high doses)"],
  "contraindications": ["Blood thinners (may increase bleeding risk)"],
  "evidence_level": "human_clinical",
  "pubmed_ids": ["12345678", "87654321"],
  "last_updated": "2025-10-31T00:00:00"
}
```

### 5.2 Protocol Data Model

```python
{
  "id": 42,
  "user_id": 1,
  "date": "2025-10-31",
  "weight_lbs": 179.0,
  "foods": [
    {
      "name": "Ginger",
      "amount_grams": 4.0,
      "net_carbs_per_100g": 15.8,
      "protein_per_100g": 1.8,
      "fat_per_100g": 0.8,
      "net_carbs": 0.6,
      "protein": 0.1,
      "fat": 0.0,
      "servings_per_day": 2,
      "grams_per_serving": 2.0,
      "timing": "Morning and Evening",
      "timing_notes": "Add to smoothie or tea",
      "preparation": "raw",
      "preparation_notes": "Grate fresh",
      "reason": "Anti-cancer compounds: Gingerol",
      "mechanisms": ["Induces apoptosis", "Reduces inflammation"],
      "safety_notes": "Max safe dose: 10g/day"
    }
    // ... 8 more foods
  ],
  "total_net_carbs": 42.5,
  "total_protein": 18.3,
  "total_fat": 2.1,
  "total_calories": 265.0,
  "keto_compatible": true,
  "keto_score": 95,
  "generated_at": "2025-10-31T08:00:00"
}
```

### 5.3 Compliance Data Model

```python
{
  "id": 10,
  "user_id": 1,
  "protocol_id": 42,
  "date": "2025-10-31",
  "foods_consumed": [
    {"name": "Ginger", "consumed": true},
    {"name": "Garlic", "consumed": true},
    {"name": "Turmeric", "consumed": true},
    {"name": "Broccoli", "consumed": true},
    {"name": "Cauliflower", "consumed": true},
    {"name": "Kale", "consumed": true},
    {"name": "Brussels Sprouts", "consumed": false},
    {"name": "Green Tea", "consumed": true},
    {"name": "Colon Support Herbal Tea", "consumed": true}
  ],
  "adherence_percentage": 88.9,
  "missed_foods": ["Brussels Sprouts"],
  "notes": "Forgot Brussels sprouts at dinner",
  "recorded_at": "2025-10-31T22:00:00"
}
```

### 5.4 Weight Record Data Model

```python
{
  "id": 5,
  "user_id": 1,
  "date": "2025-10-31",
  "weight_lbs": 178.5,
  "notes": "Feeling good, consistent protocol adherence",
  "followed_protocol": true
}
```

---

## 6. Business Rules

### 6.1 Protocol Generation Rules

1. **Weight-based dosing:** All food amounts scale with user weight
2. **Safety limits:** Never exceed `max_daily_amount_grams` for any food
3. **Keto compatibility:** Adjust high-carb foods if total net carbs > 50g
4. **Daily regeneration:** Protocol can be regenerated if weight changes
5. **Cancer-type filtering:** Only include foods relevant to user's cancer type

### 6.2 Compliance Tracking Rules

1. **Adherence calculation:** `(foods_consumed / total_foods) * 100`
2. **Streak counting:** Consecutive days with 100% adherence
3. **Streak reset:** Any day < 100% resets streak to 0
4. **7-day average:** Rolling average of last 7 days' adherence

### 6.3 Weight Tracking Rules

1. **Measurement protocol:**
   - Naked
   - Morning (before eating/drinking)
   - Weekly recommended
   - Same scale each time

2. **Trend visualization:** Minimum 2 data points required for chart

3. **Goal tracking:** Optional target weight for visual comparison

### 6.4 Keto Compatibility Rules

1. **Net carbs:** < 50g per day (strict < 20g, moderate < 50g)
2. **Macro ratios:**
   - Fat: 60-75% of calories
   - Protein: 15-30% of calories
   - Carbs: 5-10% of calories

3. **Adjustment strategy:**
   - Reduce highest-carb foods by 25%
   - Suggest adding fat sources (olive oil, coconut oil, avocado)

### 6.5 Safety Rules

1. **Drug interactions:** Display warnings for known food-drug interactions
2. **Contraindications:** Show contraindications for each food
3. **Side effects:** List potential side effects
4. **Maximum doses:** Enforce maximum safe daily amounts
5. **Allergy checking:** (Future) Check user allergies against protocol foods

---

## 7. Special Considerations

### 7.1 Colon Support Herbal Tea

**Custom Blend:**
- Peppermint: 40%
- Chamomile: 30%
- Ginger: 15%
- Fennel: 15%

**Dosing:**
- 8g tea per cup
- 2 cups per day (16g total)
- Morning (upon waking) and Evening (before bed)

**Benefits:**
- Soothes intestinal lining
- Reduces inflammation
- Anti-spasmodic properties
- Supports digestive health

**Preparation:**
- Steep 8g in hot water (not boiling) for 5-7 minutes
- Can add honey if needed

**Documentation:** See `COLON_TEA_INFO.md` for complete details

### 7.2 Green Tea

**Dosing:**
- 750g per day = 3-4 cups
- Distributed throughout afternoon

**Preparation:**
- Water temperature: 160-180°F (NOT boiling)
- Steep time: 2-3 minutes
- Avoid adding milk (reduces EGCG absorption)

**Timing:**
- Between meals (better iron absorption)
- Avoid late evening (caffeine)

**Active compound:** EGCG (epigallocatechin gallate)

### 7.3 Garlic Preparation

**Critical Rule:** Crush and wait 10 minutes before eating

**Reason:** Activates allicin (primary anti-cancer compound)

**Dosing:** 10g/day = ~3 cloves

**Preparation methods:**
- Raw (most potent)
- Lightly cooked (retain some allicin)
- Avoid microwaving (destroys compounds)

### 7.4 Turmeric + Black Pepper

**Synergy:** Black pepper increases curcumin absorption by 2000%

**Dosing:**
- Turmeric: 5g/day
- Black pepper: Pinch (0.1g) with each turmeric dose

**Preparation:**
- Mix turmeric powder with black pepper
- Add to fat source (coconut oil, olive oil) for better absorption
- Can be added to meals or made into "golden paste"

---

## 8. Future Enhancements (Post-MVP)

### 8.1 Phase 2 Features (Partially Implemented)

- ✅ Medication tracking
- ✅ Hydration logging
- ✅ Health photo uploads
- 🔄 Medication interaction checking (basic)
- 🔄 Photo comparison views

### 8.2 Phase 3 Features (Planned)

**Multi-user support:**
- User authentication
- Personal accounts
- Data privacy/isolation

**Advanced Analytics:**
- Correlation analysis (weight vs. adherence)
- Predictive modeling
- Custom reporting

**PubMed Integration:**
- Automatic research fetching
- Study summarization
- Dose extraction from papers

**Meal Planning v2:**
- Custom recipe builder
- Meal prep scheduler
- Nutrition calculator

**Mobile App:**
- Native iOS/Android apps
- Push notifications for reminders
- Offline mode

**Integrations:**
- MyFitnessPal sync
- Apple Health / Google Fit
- Smart scale integration
- Calendar sync for reminders

**Social Features:**
- Share progress with caregivers
- Support groups
- Healthcare provider portal

---

## 9. Development Guidelines

### 9.1 Code Organization

**Backend Structure:**
```
backend/
├── app/
│   ├── main.py                 # FastAPI app entry
│   ├── api/                    # API route handlers
│   │   ├── protocol.py
│   │   ├── weight.py
│   │   ├── compliance.py
│   │   ├── foods.py
│   │   ├── status.py
│   │   ├── library.py
│   │   ├── exports.py
│   │   ├── health_photos.py
│   │   ├── medications.py
│   │   └── hydration.py
│   ├── core/                   # Core business logic
│   │   ├── database.py
│   │   ├── models.py
│   │   ├── protocol_generator.py
│   │   ├── dosing_calculator.py
│   │   ├── keto_checker.py
│   │   ├── init_database.py
│   │   └── config.py
│   └── schemas/                # Pydantic schemas
│       ├── protocol.py
│       ├── weight.py
│       ├── compliance.py
│       └── foods.py
├── data/                       # Database files
└── uploads/                    # User uploads
```

**Frontend Structure:**
```
frontend/
├── src/
│   ├── App.tsx                 # Main app component
│   ├── main.tsx                # Entry point
│   ├── pages/                  # Page components
│   │   ├── Dashboard.tsx
│   │   ├── Protocol.tsx
│   │   ├── MealPlanner.tsx
│   │   ├── Compliance.tsx
│   │   ├── Weight.tsx
│   │   ├── Library.tsx
│   │   ├── Health.tsx
│   │   ├── Hydration.tsx
│   │   └── Medications.tsx
│   ├── lib/                    # Utilities
│   │   ├── api.ts              # API client
│   │   └── utils.ts            # Helper functions
│   └── index.css               # Global styles
└── public/                     # Static assets
```

### 9.2 Development Workflow

**Local Development:**
1. Start backend: `cd backend && python3 -m uvicorn app.main:app --reload`
2. Start frontend: `cd frontend && npm run dev`
3. Access app: `http://localhost:5173`
4. API docs: `http://localhost:8000/api/docs`

**Database Management:**
- Location: `backend/data/protocol.db`
- Reset: Delete file, restart backend (auto-seeds)
- Migrations: Manual SQL scripts in `backend/migrations/`

**Testing:**
- Backend: pytest (tests not yet implemented)
- Frontend: Manual testing
- E2E: Manual user flows

### 9.3 Deployment

**Replit Deployment:**
1. Push to GitHub
2. Import to Replit
3. Configure environment variables
4. Run `start.sh` script
5. Access via Replit URL

**Environment Variables:**
- `PORT`: Server port (default 8000)
- `CORS_ORIGINS`: Allowed CORS origins (comma-separated)
- `DATABASE_PATH`: Path to SQLite database

**Static File Serving:**
- Frontend builds to `frontend/dist/`
- Backend serves static files in production
- API available at `/api/*`
- Frontend at `/*`

---

## 10. Success Criteria

### 10.1 MVP Success Metrics

**User Adoption:**
- Jesse uses app daily for 30+ days
- 80%+ adherence rate maintained
- Weekly weight logging consistently performed

**Technical Performance:**
- Page load time < 2 seconds
- API response time < 500ms
- Zero critical bugs
- 99% uptime

**User Satisfaction:**
- Jesse reports app is "easy to use"
- Meal planning saves time vs. manual planning
- Protocol compliance easier than without app

### 10.2 Product Validation

**Health Outcomes:**
- Weight trend shows stability or improvement
- Jesse reports feeling better
- Oncologist approves of nutrition approach

**Usability:**
- No training required (self-explanatory UI)
- Mobile-friendly for on-the-go logging
- Fast enough to use multiple times per day

**Reliability:**
- No data loss
- Consistent protocol generation
- Accurate tracking and calculations

---

## 11. Open Questions & Decisions Needed

### 11.1 Outstanding Questions

1. **Multi-user expansion:** Should this be productized for other cancer patients?
2. **Healthcare provider access:** Should doctors/oncologists have read access?
3. **Data backup:** What's the backup/disaster recovery strategy?
4. **Privacy compliance:** Do we need HIPAA compliance?
5. **Paid vs. Free:** If productized, what's the business model?

### 11.2 Technical Debt

1. **No automated tests:** Need pytest for backend, Jest for frontend
2. **No authentication:** Required for multi-user
3. **Manual database migrations:** Need migration framework
4. **File upload limits:** No virus scanning, size limits not enforced
5. **PubMed integration incomplete:** Fetcher exists but not fully integrated

### 11.3 Design Decisions

1. **Why SQLite?** Simple, serverless, perfect for single-user. May need PostgreSQL for multi-user.
2. **Why no ORM?** Direct SQL is faster, simpler for small schema. May want SQLAlchemy later.
3. **Why React?** Modern, well-supported, TypeScript compatibility.
4. **Why FastAPI?** Fast, automatic API docs, Pydantic validation, async support.
5. **Why Replit?** Easy deployment, free tier, integrated development environment.

---

## 12. Appendices

### 12.1 Glossary

- **Adherence:** Percentage of protocol foods consumed in a day
- **Allometric Scaling:** Method to convert animal study doses to human-equivalent doses
- **Apoptosis:** Programmed cell death (cancer cells)
- **Compliance:** Same as adherence
- **EGCG:** Epigallocatechin gallate (green tea compound)
- **FDA:** U.S. Food and Drug Administration
- **Keto:** Ketogenic diet (high fat, low carb)
- **Net Carbs:** Total carbs minus fiber
- **Protocol:** Daily personalized anti-cancer food plan
- **PubMed:** Database of biomedical research papers
- **Streak:** Consecutive days of 100% adherence
- **Sulforaphane:** Anti-cancer compound in cruciferous vegetables

### 12.2 References

**Food Dosing:**
- FDA guidance on dose conversions (animal to human)
- NIH dietary supplement fact sheets
- Peer-reviewed studies on anti-cancer foods

**Nutrition Data:**
- USDA FoodData Central
- Nutritionix API
- Self Nutrition Data

**Research:**
- PubMed/NCBI
- Cochrane Reviews
- Cancer research journals

### 12.3 Related Documents

- `README.md` - User guide and quick start
- `JESSE_START_HERE.md` - Onboarding guide for Jesse
- `DEVELOPER_NOTES.md` - Technical implementation notes
- `COLON_TEA_INFO.md` - Colon support tea specifications
- `DEPLOYMENT.md` - Deployment instructions
- `REPLIT_DEPLOYMENT_GUIDE.md` - Replit-specific deployment
- `TEST_RESULTS.md` - Testing documentation

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-10-31 | JD Kristenson | Initial PRD created from existing codebase |

---

**End of Document**
