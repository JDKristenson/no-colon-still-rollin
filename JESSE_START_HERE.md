# No Colon, Still Rollin' - Quick Start Guide for Jesse

Hey Jesse! This system will help you:
1. Know exactly what anti-cancer foods to eat each day
2. Calculate proper doses based on research
3. Keep it all keto-friendly
4. Track your compliance
5. Generate reports for your oncology team

## Already Set Up! ✅

The system is ready to go. Everything is installed and your profile is created.

---

## Daily Routine

### Every Morning
```bash
cd "/Users/JDKristenson/Desktop/No Colon Still Rollin"
python3 src/main.py protocol
```

This generates your food protocol for the day - tells you what to eat, how much, when, and how to prepare it.

### Every Evening (5 minutes)
```bash
python3 src/main.py track
```

Quick check-in to record what you actually ate. The system will ask about each food and calculate your adherence percentage.

### Every Monday Morning
**Weigh-in Protocol**: Naked, first thing upon waking, before food or water.

```bash
python3 src/main.py weight 177
```

(Replace 177 with your actual weight)

### Anytime - Check Your Progress
```bash
python3 src/main.py history
```

Shows your compliance over the past week.

```bash
python3 src/main.py status
```

Shows your current stats and system info.

---

## Understanding Your Protocol

When you run `python3 src/main.py protocol`, you'll see something like:

```
1. GINGER
   Amount: 4.0g per day
   Schedule: once daily (1x 4.0g)
   Timing: with a meal
   Preparation: raw
   Notes: Raw ginger has highest gingerol content...
   Why: Anti-cancer compounds: gingerol, shogaol
```

This means:
- **Amount**: Total for the whole day
- **Schedule**: How many times to take it
- **Timing**: When during the day
- **Preparation**: Raw, cooked, powdered, etc.
- **Why**: What makes it anti-cancer

---

## Your Questions Answered

### "How much ginger can I push beyond 4 grams?"

The system sets safety limits based on research:
- Ginger: 6g max per day
- Garlic: ~12g (4 cloves) max per day
- Turmeric: 8g max per day

These are conservative limits. The system will warn you if you try to exceed them.

### "Does pickled ginger have the same properties?"

The system's database notes: "Raw ginger has highest gingerol content. Pickled (sushi ginger) has less."

Raw is better, but pickled still has benefits. If you prefer pickled, increase the amount by ~25-50% to compensate.

### "Should I eat ginger all at once or split it up?"

The system calculates this for you! Look at the "Schedule" line:
- `once daily` = one big dose
- `twice daily` = split into morning and evening
- `three times daily` = with each meal

For most foods, the system recommends splitting larger amounts to:
1. Reduce side effects (like heartburn)
2. Maintain steadier blood levels of compounds

### "What about keto compatibility?"

The protocol generator automatically:
- Keeps net carbs under 20g/day
- Calculates protein based on your weight
- Targets 70-75% calories from fat

If foods push you over carb limits, it reduces portions.

**Important**: The anti-cancer vegetables are naturally low in fat, so you'll need to add:
- MCT oil or coconut oil (1-2 tablespoons)
- Avocado (1/2 medium)
- Fatty fish (salmon, mackerel) (100-150g)
- Olive oil on veggies
- Nuts in moderation

---

## Weekly Routine

### Monday Morning
1. **Weigh in** (protocol: naked, before food/water)
2. **Record weight**: `python3 src/main.py weight [your_weight]`
3. **Generate this week's protocol**: `python3 src/main.py protocol`

Your weight affects dose calculations, so update it weekly.

---

## Optional: Update Research Database

The system can pull the latest anti-cancer food research from PubMed:

```bash
python3 src/main.py update-research
```

**Note**: You need a PubMed API key for large updates. For now, the system uses curated research data.

To get an API key (free):
1. Create account at https://www.ncbi.nlm.nih.gov/account/
2. Get API key from settings
3. Add to `.env` file: `NCBI_API_KEY=your_key_here`

---

## Troubleshooting

### "User not found" error
```bash
python3 src/main.py setup
```

This reinitializes the database.

### "No protocol found for today"
```bash
python3 src/main.py protocol
```

Generate today's protocol first.

### Python errors
Make sure you're in the right directory:
```bash
cd "/Users/JDKristenson/Desktop/No Colon Still Rollin"
```

---

## File Locations

- **Database**: `data/cancer_foods.db` (your data is here)
- **Reports**: `reports/` (future: doctor reports will go here)
- **Settings**: `.env` (configuration)

---

## Next Steps

1. **Today**: Run `python3 src/main.py protocol` and get your food list
2. **Tonight**: Run `python3 src/main.py track` to record compliance
3. **Monday**: Weigh in and update your weight
4. **In 1 week**: Check your adherence with `python3 src/main.py history`

---

## Questions?

Ask JD to:
- Add new foods
- Adjust doses
- Add your medications (for interaction checking)
- Generate reports for your doctors
- Modify the keto parameters
- Add meal planning features

---

**Remember**: This is a tool to help you and your oncology team. Always discuss dietary changes with your doctors, especially if you're on active treatment.

**You've got this, Jesse. No colon, still rollin'!** 💪
