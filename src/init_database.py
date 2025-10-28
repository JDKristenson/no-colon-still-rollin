"""
Initialize database with Jesse's anti-cancer foods
Seed with known foods and their properties
"""
from datetime import datetime
from database import Database


def seed_foods(db: Database):
    """Add initial anti-cancer foods to database"""

    foods_data = [
        {
            "name": "Ginger",
            "common_names": ["fresh ginger", "ginger root"],
            "active_compounds": [
                {"name": "gingerol", "amount_per_100g": 500, "mechanism": "Induces apoptosis in cancer cells"},
                {"name": "shogaol", "amount_per_100g": 150, "mechanism": "Anti-inflammatory, anti-metastatic"},
            ],
            "net_carbs_per_100g": 15.0,
            "protein_per_100g": 1.8,
            "fat_per_100g": 0.8,
            "fiber_per_100g": 2.0,
            "cancer_types": ["colon", "colorectal", "general"],
            "mechanisms": [
                "Induces apoptosis",
                "Inhibits tumor growth",
                "Anti-inflammatory",
                "Antioxidant"
            ],
            "best_preparation": "raw",
            "preparation_notes": "Raw ginger has highest gingerol content. Pickled (sushi ginger) has less. Can be juiced, grated, or sliced.",
            "max_daily_amount_grams": 6.0,
            "side_effects": ["Possible heartburn", "Diarrhea at high doses"],
            "contraindications": ["Blood thinners (increases bleeding risk)"],
            "evidence_level": "animal",
            "pubmed_ids": [],
        },
        {
            "name": "Garlic",
            "common_names": ["fresh garlic", "garlic cloves"],
            "active_compounds": [
                {"name": "allicin", "amount_per_100g": 4000, "mechanism": "Induces apoptosis, inhibits angiogenesis"},
                {"name": "s-allyl cysteine", "amount_per_100g": 500, "mechanism": "Detoxification, anti-tumor"},
            ],
            "net_carbs_per_100g": 30.0,
            "protein_per_100g": 6.4,
            "fat_per_100g": 0.5,
            "fiber_per_100g": 2.1,
            "cancer_types": ["colon", "colorectal", "stomach", "general"],
            "mechanisms": [
                "Induces apoptosis",
                "Inhibits cancer cell proliferation",
                "Enhances immune function",
                "Antioxidant"
            ],
            "best_preparation": "raw",
            "preparation_notes": "Crush or chop and let sit 10 minutes before eating to activate allicin. Raw is most potent. 1 clove ≈ 3g.",
            "max_daily_amount_grams": 12.0,  # ~4 cloves
            "side_effects": ["Body odor", "Heartburn", "Upset stomach"],
            "contraindications": ["Blood thinners", "Upcoming surgery"],
            "evidence_level": "human_observational",
            "pubmed_ids": [],
        },
        {
            "name": "Turmeric",
            "common_names": ["turmeric powder", "fresh turmeric root"],
            "active_compounds": [
                {"name": "curcumin", "amount_per_100g": 3000, "mechanism": "Anti-inflammatory, inhibits tumor growth"},
            ],
            "net_carbs_per_100g": 3.9,
            "protein_per_100g": 7.8,
            "fat_per_100g": 9.9,
            "fiber_per_100g": 21.1,
            "cancer_types": ["colon", "colorectal", "breast", "prostate", "general"],
            "mechanisms": [
                "Inhibits NF-κB (inflammation)",
                "Induces apoptosis",
                "Inhibits angiogenesis",
                "Anti-metastatic"
            ],
            "best_preparation": "powdered",
            "preparation_notes": "Take with black pepper (piperine) for 2000% better absorption. Take with fats. Consider high-bioavailability forms.",
            "max_daily_amount_grams": 8.0,
            "side_effects": ["Upset stomach at high doses", "May worsen gallbladder problems"],
            "contraindications": ["Gallstones", "Bile duct obstruction"],
            "evidence_level": "human_clinical",
            "pubmed_ids": [],
        },
        {
            "name": "Broccoli",
            "common_names": ["broccoli florets", "broccoli crowns"],
            "active_compounds": [
                {"name": "sulforaphane", "amount_per_100g": 100, "mechanism": "Activates detox enzymes, induces apoptosis"},
                {"name": "indole-3-carbinol", "amount_per_100g": 50, "mechanism": "Hormonal balance, anti-cancer"},
            ],
            "net_carbs_per_100g": 4.0,
            "protein_per_100g": 2.8,
            "fat_per_100g": 0.4,
            "fiber_per_100g": 2.6,
            "cancer_types": ["colon", "colorectal", "breast", "prostate"],
            "mechanisms": [
                "Activates Phase II detoxification",
                "Induces apoptosis",
                "Inhibits cancer stem cells",
                "Anti-inflammatory"
            ],
            "best_preparation": "steamed",
            "preparation_notes": "Light steaming (3-4 min) preserves sulforaphane. Raw also good. Sprinkle with mustard seed powder to boost sulforaphane.",
            "max_daily_amount_grams": 500.0,
            "side_effects": ["Gas", "Bloating"],
            "contraindications": ["Thyroid issues (in very large amounts)"],
            "evidence_level": "human_observational",
            "pubmed_ids": [],
        },
        {
            "name": "Cauliflower",
            "common_names": ["cauliflower florets", "cauliflower rice"],
            "active_compounds": [
                {"name": "sulforaphane", "amount_per_100g": 80, "mechanism": "Detoxification, anti-cancer"},
                {"name": "glucosinolates", "amount_per_100g": 200, "mechanism": "Cancer prevention"},
            ],
            "net_carbs_per_100g": 3.0,
            "protein_per_100g": 1.9,
            "fat_per_100g": 0.3,
            "fiber_per_100g": 2.0,
            "cancer_types": ["colon", "colorectal", "general"],
            "mechanisms": ["Detoxification", "Induces apoptosis", "Anti-inflammatory"],
            "best_preparation": "steamed",
            "preparation_notes": "Light cooking preferred. Can be eaten raw. Versatile for keto recipes (cauliflower rice, mash, etc.).",
            "max_daily_amount_grams": 500.0,
            "side_effects": ["Gas", "Bloating"],
            "contraindications": [],
            "evidence_level": "animal",
            "pubmed_ids": [],
        },
        {
            "name": "Kale",
            "common_names": ["curly kale", "lacinato kale", "dinosaur kale"],
            "active_compounds": [
                {"name": "sulforaphane", "amount_per_100g": 90, "mechanism": "Anti-cancer, detoxification"},
                {"name": "quercetin", "amount_per_100g": 23, "mechanism": "Antioxidant, anti-inflammatory"},
            ],
            "net_carbs_per_100g": 5.0,
            "protein_per_100g": 4.3,
            "fat_per_100g": 0.9,
            "fiber_per_100g": 3.6,
            "cancer_types": ["colon", "colorectal", "general"],
            "mechanisms": ["Detoxification", "Anti-inflammatory", "Antioxidant"],
            "best_preparation": "steamed",
            "preparation_notes": "Massage raw kale to break down cellulose. Lightly steam or sauté. Very nutrient-dense.",
            "max_daily_amount_grams": 300.0,
            "side_effects": ["Gas", "May interfere with thyroid medication"],
            "contraindications": ["Thyroid medication", "Blood thinners (high vitamin K)"],
            "evidence_level": "animal",
            "pubmed_ids": [],
        },
        {
            "name": "Brussels Sprouts",
            "common_names": ["brussels sprouts"],
            "active_compounds": [
                {"name": "sulforaphane", "amount_per_100g": 110, "mechanism": "Anti-cancer, detoxification"},
                {"name": "indole-3-carbinol", "amount_per_100g": 60, "mechanism": "Hormonal balance"},
            ],
            "net_carbs_per_100g": 5.0,
            "protein_per_100g": 3.4,
            "fat_per_100g": 0.3,
            "fiber_per_100g": 3.8,
            "cancer_types": ["colon", "colorectal", "general"],
            "mechanisms": ["Detoxification", "Induces apoptosis", "Anti-inflammatory"],
            "best_preparation": "steamed",
            "preparation_notes": "Don't overcook - keeps compounds active. Roasting also good.",
            "max_daily_amount_grams": 300.0,
            "side_effects": ["Gas", "Bloating"],
            "contraindications": [],
            "evidence_level": "animal",
            "pubmed_ids": [],
        },
        {
            "name": "Green Tea",
            "common_names": ["green tea", "matcha"],
            "active_compounds": [
                {"name": "EGCG", "amount_per_100g": 500, "mechanism": "Powerful antioxidant, induces apoptosis"},
                {"name": "catechins", "amount_per_100g": 800, "mechanism": "Anti-cancer, anti-inflammatory"},
            ],
            "net_carbs_per_100g": 0.0,
            "protein_per_100g": 0.0,
            "fat_per_100g": 0.0,
            "fiber_per_100g": 0.0,
            "cancer_types": ["colon", "colorectal", "breast", "prostate", "general"],
            "mechanisms": [
                "Induces apoptosis",
                "Inhibits angiogenesis",
                "Antioxidant",
                "Anti-metastatic"
            ],
            "best_preparation": "extract",
            "preparation_notes": "Brew at 160-180°F for 2-3 min. Don't boil (destroys compounds). Matcha has higher concentration. 3-5 cups/day.",
            "max_daily_amount_grams": 1000.0,  # ~5 cups
            "side_effects": ["Caffeine effects", "May reduce iron absorption"],
            "contraindications": ["Caffeine sensitivity", "Anemia (take separately from iron)"],
            "evidence_level": "human_observational",
            "pubmed_ids": [],
        },
    ]

    print("🌱 Seeding database with anti-cancer foods...\n")

    for food_data in foods_data:
        try:
            food_id = db.add_food(food_data)
            print(f"  ✅ Added: {food_data['name']}")
        except Exception as e:
            print(f"  ⚠️  Skipped {food_data['name']}: {str(e)}")

    print(f"\n✅ Database seeded with {len(foods_data)} foods")


def create_jesse_user(db: Database):
    """Create Jesse's user profile"""

    jesse_data = {
        "name": "Jesse Mills",
        "email": "",
        "cancer_type": "colon",
        "diagnosis_date": None,  # Can be filled in
        "current_treatment": "",
        "medications": [],  # Will be added separately
        "allergies": [],
        "current_weight_lbs": 179.0,
        "target_weight_lbs": 173.0,
    }

    try:
        user_id = db.create_user(jesse_data)
        print(f"\n✅ Created user: Jesse Mills (ID: {user_id})")
        return user_id
    except Exception as e:
        print(f"\n⚠️  User may already exist: {str(e)}")
        # Try to get existing user
        user = db.get_user(name="Jesse Mills")
        if user:
            return user['id']
        return None


def main():
    """Initialize the database"""
    print("=" * 60)
    print("No Colon, Still Rollin' - Database Initialization")
    print("=" * 60)
    print()

    db = Database()

    # Seed foods
    seed_foods(db)

    # Create Jesse's user
    create_jesse_user(db)

    print("\n" + "=" * 60)
    print("✅ Database initialization complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Update research: python src/pubmed_fetcher.py")
    print("2. Generate protocol: python src/protocol_generator.py")
    print("3. Track compliance: python src/track_compliance.py")

    db.close()


if __name__ == "__main__":
    main()
