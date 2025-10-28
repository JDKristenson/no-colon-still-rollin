# No Colon, Still Rollin' - Anti-Cancer Protocol System

**For Jesse Mills**

A comprehensive web application for managing your personalized anti-cancer food protocol. This system makes compliance easy by providing meal plans, recipes, shopping lists, and progress tracking.

## 🎯 What This Does

This application helps you fight cancer through evidence-based nutrition by:

1. **Generating personalized daily protocols** - Exact amounts of anti-cancer foods based on your weight
2. **Making compliance easy** - Simple recipes and meal plans
3. **Tracking your progress** - Weight trends, adherence, and streaks
4. **Shopping made simple** - Weekly shopping lists

## 🚀 Quick Start

### Starting the Application

1. **Start Backend** (from project root):
   ```bash
   cd backend
   python3 -m uvicorn app.main:app --reload
   ```
   Backend runs at: http://localhost:8000

2. **Start Frontend** (in new terminal):
   ```bash
   cd frontend
   npm run dev
   ```
   Frontend runs at: http://localhost:5173

3. **Open in browser**: http://localhost:5173/

## 📱 Using the Application

### Dashboard
- See your current weight, 7-day adherence, and streak
- View weight trend chart
- Quick overview of your progress

### Protocol Page
- Click "Generate Today's Protocol" to get your personalized food plan
- Each food shows:
  - Exact amounts (grams)
  - When to take it (timing)
  - How to prepare it
  - Why it fights cancer
  - Safety notes

### Meals Page 🍽️
**This is where compliance gets easy!**

- **7 practical recipes** that incorporate all your protocol foods
- **Weekly shopping list** - know exactly what to buy
- **Sample daily plan** - follow this and you'll hit all your targets
- Click any recipe to see detailed instructions

**Key Recipes:**
- Morning Colon Support Tea
- Anti-Cancer Power Smoothie
- Garlic Cauliflower Rice Bowl
- Roasted Brussels Sprouts with Turmeric
- Kale & Ginger Stir-Fry
- Green Tea (throughout day)
- Evening Colon Support Tea

### Check-In Page
- Quick daily tracker - check off foods as you eat them
- Progress bar shows completion
- Motivational messages
- See your streak and adherence stats

### Weight Page
- Record your weight anytime
- See trend chart
- View history table with notes
- Track if you followed protocol each day

## 🌿 Your Protocol Foods

You'll be eating 9 powerful anti-cancer foods:

1. **Ginger** (4g/day) - Anti-inflammatory, anti-tumor
2. **Garlic** (10g/day) - Induces apoptosis in cancer cells
3. **Turmeric** (5g/day) - Powerful anti-inflammatory
4. **Broccoli** (200g/day) - Activates detox enzymes
5. **Cauliflower** (150g/day) - Cancer prevention
6. **Kale** (100g/day) - Antioxidant powerhouse
7. **Brussels Sprouts** (150g/day) - High in sulforaphane
8. **Green Tea** (750g/day = 3-4 cups) - EGCG anti-cancer compound
9. **Colon Support Herbal Tea** (16g/day = 2 cups) - Twice daily for digestive support

## ☕ Special Note: Colon Support Tea

This custom herbal blend is designed specifically for colon health:
- **Blend:** Peppermint (40%), Chamomile (30%), Ginger (15%), Fennel (15%)
- **When:** Morning (upon waking) and Evening (before bed)
- **Benefits:** Soothes intestinal lining, reduces inflammation, anti-spasmodic
- **See:** `COLON_TEA_INFO.md` for complete details

## 📊 Your Daily Schedule

**Sample Day:**

**Morning (upon waking):**
- Colon Support Tea (1 cup)
- Anti-Cancer Smoothie (with ginger, turmeric, kale)

**Lunch:**
- Garlic Cauliflower Rice Bowl with Broccoli

**Afternoon:**
- Green Tea (2-3 cups throughout afternoon)

**Dinner:**
- Roasted Brussels Sprouts with Turmeric OR Kale Ginger Stir-Fry

**Evening (before bed):**
- Colon Support Tea (1 cup)

This hits ALL your protocol foods in an easy, natural way!

## 🛒 Weekly Shopping

The Meals page has a complete shopping list. Key items:

**Fresh:**
- Fresh ginger root
- Garlic bulbs
- Kale, broccoli, cauliflower, Brussels sprouts

**Spices:**
- Turmeric powder (organic)
- Black pepper (fresh ground)
- Colon support tea blend

**Pantry:**
- Olive oil, coconut oil
- Unsweetened almond milk
- Green tea

## 💡 Tips for Success

1. **Meal prep on Sundays** - Chop veggies, make tea blend
2. **Don't skip the tea** - Morning and evening doses are crucial
3. **Use the Check-In page daily** - Builds your streak
4. **Track your weight weekly** - See your progress
5. **Follow recipes exactly** - They're designed for maximum benefit
6. **Crush garlic 10 min before eating** - Activates allicin
7. **Add black pepper to turmeric** - Increases absorption 2000%
8. **Don't boil green tea** - Use 160-180°F water

## ⚠️ Important Safety Notes

- These foods are generally safe, but always consult your oncologist
- Ginger and garlic can increase bleeding risk (important if on blood thinners)
- Peppermint in colon tea may worsen GERD
- Take green tea between meals for better iron absorption

## 🔬 Evidence-Based

All foods and doses are based on:
- FDA allometric scaling for human doses
- Published research studies
- Traditional therapeutic use
- Safety-tested maximum amounts

## 📈 Tracking Your Progress

The app automatically tracks:
- **Weight trends** - See if protocol is working
- **Compliance adherence** - 7-day rolling average
- **Current streak** - Consecutive days of following protocol
- **Total days tracked** - Your commitment to healing

## 🎯 Goal

**Simple:** Make it as easy as possible for you to get these cancer-fighting foods into your body every single day.

**The protocol works if you work the protocol.**

## 🆘 Need Help?

- All recipes in Meals page
- Protocol page shows exact amounts
- Check-In page keeps you on track
- Shopping list tells you what to buy

**You've got this, Jesse. One day at a time. 💪**

---

## Technical Setup (For Developers)

### Backend Stack
- FastAPI (Python 3.8+)
- SQLite database
- Pydantic schemas
- CORS enabled for localhost:5173

### Frontend Stack
- Vite + React + TypeScript
- Tailwind CSS (medical theme)
- TanStack Query for state management
- React Router for navigation
- Recharts for visualizations

### Database
- Location: `data/protocol.db`
- Pre-seeded with 9 foods
- User: Jesse Mills (ID: 1, 179 lbs)

### API Endpoints
- `GET /api/status/` - Dashboard data
- `GET /api/protocol/today` - Today's protocol
- `POST /api/protocol/generate` - Generate new protocol
- `GET /api/weight/history` - Weight history
- `POST /api/weight/` - Record weight
- `GET /api/compliance/stats` - Compliance statistics
- `GET /api/foods/` - All foods

### Development
```bash
# Backend
cd backend
pip install -r requirements.txt
python3 -m uvicorn app.main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

## License

Private use only.

## Author

Built for Jesse Mills by JD Kristenson
October 2025
