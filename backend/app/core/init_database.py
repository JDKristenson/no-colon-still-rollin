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
        {
            "name": "Colon Support Herbal Tea",
            "common_names": ["colon tea", "digestive support tea", "gut health tea"],
            "active_compounds": [
                {"name": "menthol", "amount_per_100g": 100, "mechanism": "Soothes digestive tract, anti-spasmodic"},
                {"name": "apigenin", "amount_per_100g": 50, "mechanism": "Anti-inflammatory, induces apoptosis"},
                {"name": "gingerol", "amount_per_100g": 80, "mechanism": "Anti-inflammatory, anti-nausea"},
                {"name": "anethole", "amount_per_100g": 60, "mechanism": "Reduces bloating, anti-inflammatory"},
            ],
            "net_carbs_per_100g": 0.0,
            "protein_per_100g": 0.0,
            "fat_per_100g": 0.0,
            "fiber_per_100g": 0.0,
            "cancer_types": ["colon", "colorectal", "digestive"],
            "mechanisms": [
                "Soothes intestinal lining",
                "Reduces inflammation",
                "Anti-spasmodic",
                "Promotes healing",
                "Supports gut microbiome"
            ],
            "best_preparation": "tea",
            "preparation_notes": "Blend: Peppermint (40%), Chamomile (30%), Ginger (15%), Fennel (15%). Steep 1-2 tsp in 8oz hot water (200°F) for 5-7 minutes. Drink twice daily: morning and evening.",
            "max_daily_amount_grams": 500.0,  # ~2 cups per day
            "side_effects": ["Rare: mild drowsiness from chamomile", "Heartburn if too much ginger"],
            "contraindications": ["GERD (peppermint may worsen)", "Allergies to ragweed family (chamomile)"],
            "evidence_level": "traditional_use",
            "pubmed_ids": [],
        },
        {
            "name": "Kimchi",
            "common_names": ["kimchi", "fermented cabbage", "Korean kimchi"],
            "active_compounds": [
                {"name": "probiotics", "amount_per_100g": 1000000, "mechanism": "Supports gut microbiome, immune function"},
                {"name": "capsaicin", "amount_per_100g": 100, "mechanism": "Anti-cancer, anti-inflammatory"},
                {"name": "sulforaphane", "amount_per_100g": 70, "mechanism": "Detoxification, induces apoptosis"},
            ],
            "net_carbs_per_100g": 2.4,
            "protein_per_100g": 1.1,
            "fat_per_100g": 0.5,
            "fiber_per_100g": 1.6,
            "cancer_types": ["colon", "colorectal", "gastric", "general"],
            "mechanisms": [
                "Supports gut microbiome",
                "Enhances immune function",
                "Anti-inflammatory",
                "Induces apoptosis",
                "Provides beneficial bacteria",
                "Improves digestion"
            ],
            "best_preparation": "raw",
            "preparation_notes": "Eat unpasteurized/raw kimchi to get live probiotics. Start with small amounts (1-2 tbsp) and increase gradually. Can add to meals or eat as side dish. Store refrigerated.",
            "max_daily_amount_grams": 150.0,  # ~3/4 cup
            "side_effects": ["Gas initially", "High sodium content", "May cause bloating at first"],
            "contraindications": ["Very high blood pressure (due to sodium)", "Histamine intolerance"],
            "evidence_level": "human_observational",
            "pubmed_ids": [],
        },
        {
            "name": "Liver Detox Tea",
            "common_names": ["liver support tea", "liver cleanse tea", "hepatic tea"],
            "active_compounds": [
                {"name": "silymarin", "amount_per_100g": 200, "mechanism": "Liver protection, regeneration, antioxidant"},
                {"name": "curcumin", "amount_per_100g": 150, "mechanism": "Anti-inflammatory, liver support"},
                {"name": "cynarin", "amount_per_100g": 100, "mechanism": "Bile production, liver detoxification"},
            ],
            "net_carbs_per_100g": 0.0,
            "protein_per_100g": 0.0,
            "fat_per_100g": 0.0,
            "fiber_per_100g": 0.0,
            "cancer_types": ["liver", "colorectal", "general"],
            "mechanisms": [
                "Supports liver detoxification pathways",
                "Protects against liver metastasis",
                "Regenerates liver cells",
                "Antioxidant protection",
                "Enhances bile production",
                "Anti-inflammatory"
            ],
            "best_preparation": "tea",
            "preparation_notes": "Blend: Milk Thistle (40%), Dandelion Root (25%), Turmeric (20%), Artichoke Leaf (15%). Steep 1-2 tsp in 8oz hot water (200-210°F) for 10-15 minutes. Drink 1-2 cups daily. Note: Liver is primary metastasis site for colon cancer.",
            "max_daily_amount_grams": 500.0,  # ~2 cups per day
            "side_effects": ["Mild laxative effect", "Rare: mild digestive upset"],
            "contraindications": ["Bile duct obstruction", "Gallstones", "Allergies to ragweed family"],
            "evidence_level": "human_clinical",
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
