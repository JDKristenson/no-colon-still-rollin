"""Add new foods (kimchi and liver detox tea) to existing database"""
import sys
import os

# Add the backend directory to the path
backend_dir = '/Users/JDKristenson/Desktop/Manual Library/No Colon Still Rollin/backend'
sys.path.insert(0, backend_dir)
sys.path.insert(0, os.path.join(backend_dir, 'app', 'core'))

from database import Database

def add_new_foods():
    """Add kimchi and liver detox tea to database"""

    db = Database()

    new_foods = [
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
            "max_daily_amount_grams": 150.0,
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
            "max_daily_amount_grams": 500.0,
            "side_effects": ["Mild laxative effect", "Rare: mild digestive upset"],
            "contraindications": ["Bile duct obstruction", "Gallstones", "Allergies to ragweed family"],
            "evidence_level": "human_clinical",
            "pubmed_ids": [],
        },
    ]

    print("🌱 Adding new foods to database...\n")

    for food_data in new_foods:
        try:
            food_id = db.add_food(food_data)
            print(f"  ✅ Added: {food_data['name']} (ID: {food_id})")
        except Exception as e:
            print(f"  ⚠️  Skipped {food_data['name']}: {str(e)}")

    # Verify foods were added
    cursor = db.conn.cursor()
    cursor.execute("SELECT COUNT(*) as count FROM foods")
    count = cursor.fetchone()[0]
    print(f"\n✅ Database now contains {count} foods")

    db.close()

if __name__ == "__main__":
    add_new_foods()
