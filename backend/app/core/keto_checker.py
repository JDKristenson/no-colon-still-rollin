"""
Keto compatibility checker for No Colon, Still Rollin'
Ensures food recommendations fit ketogenic diet requirements
"""
from typing import Dict, List
from dataclasses import dataclass

from config import KETO_CONFIG


@dataclass
class MacroProfile:
    """Nutritional macros for a food or protocol"""
    food_name: str
    serving_size_g: float

    # Macros per serving
    total_carbs_g: float
    fiber_g: float
    net_carbs_g: float
    protein_g: float
    fat_g: float

    # Calories
    calories: float

    # Keto ratios (as percentages)
    carb_percentage: float
    protein_percentage: float
    fat_percentage: float

    def __post_init__(self):
        """Calculate net carbs and percentages"""
        if self.net_carbs_g == 0:
            self.net_carbs_g = max(0, self.total_carbs_g - self.fiber_g)

        if self.calories == 0:
            # Calculate from macros (4 cal/g carbs, 4 cal/g protein, 9 cal/g fat)
            self.calories = (self.net_carbs_g * 4) + (self.protein_g * 4) + (self.fat_g * 9)

        if self.calories > 0:
            self.carb_percentage = (self.net_carbs_g * 4 / self.calories) * 100
            self.protein_percentage = (self.protein_g * 4 / self.calories) * 100
            self.fat_percentage = (self.fat_g * 9 / self.calories) * 100


@dataclass
class KetoCompatibility:
    """Keto compatibility assessment"""
    is_keto_friendly: bool
    compatibility_score: float  # 0-100
    net_carbs_per_day: float
    protein_per_day: float
    fat_per_day: float
    macro_ratios: Dict[str, float]  # percentages
    recommendations: List[str]
    warnings: List[str]


class KetoChecker:
    """Check and optimize for ketogenic diet compatibility"""

    def __init__(self):
        self.max_net_carbs = KETO_CONFIG["max_net_carbs_per_day"]
        self.target_protein_g_per_kg = KETO_CONFIG["target_protein_g_per_kg"]
        self.target_fat_percentage = KETO_CONFIG["target_fat_percentage"]

    def calculate_macro_profile(self, food_data: Dict, serving_g: float) -> MacroProfile:
        """
        Calculate macros for a specific serving size

        Args:
            food_data: Dict with nutritional info per 100g
            serving_g: Serving size in grams

        Returns:
            MacroProfile object
        """
        multiplier = serving_g / 100

        total_carbs = food_data.get('total_carbs_per_100g', food_data.get('net_carbs_per_100g', 0)) * multiplier
        fiber = food_data.get('fiber_per_100g', 0) * multiplier
        net_carbs = food_data.get('net_carbs_per_100g', 0) * multiplier
        protein = food_data.get('protein_per_100g', 0) * multiplier
        fat = food_data.get('fat_per_100g', 0) * multiplier

        return MacroProfile(
            food_name=food_data.get('name', 'Unknown'),
            serving_size_g=serving_g,
            total_carbs_g=total_carbs,
            fiber_g=fiber,
            net_carbs_g=net_carbs,
            protein_g=protein,
            fat_g=fat,
            calories=0,  # Will be calculated
            carb_percentage=0,
            protein_percentage=0,
            fat_percentage=0,
        )

    def check_daily_protocol(self, foods: List[Dict],
                            user_weight_kg: float) -> KetoCompatibility:
        """
        Check if daily food protocol is keto-compatible

        Args:
            foods: List of food dicts with amounts
            user_weight_kg: User's weight in kg

        Returns:
            KetoCompatibility assessment
        """
        # Calculate totals
        total_net_carbs = 0
        total_protein = 0
        total_fat = 0
        total_calories = 0

        for food in foods:
            profile = self.calculate_macro_profile(
                food,
                food.get('amount_grams', 0)
            )
            total_net_carbs += profile.net_carbs_g
            total_protein += profile.protein_g
            total_fat += profile.fat_g
            total_calories += profile.calories

        # Calculate macro ratios
        if total_calories > 0:
            carb_pct = (total_net_carbs * 4 / total_calories) * 100
            protein_pct = (total_protein * 4 / total_calories) * 100
            fat_pct = (total_fat * 9 / total_calories) * 100
        else:
            carb_pct = protein_pct = fat_pct = 0

        # Calculate target protein
        target_protein = user_weight_kg * self.target_protein_g_per_kg

        # Assess compatibility
        is_keto = (
            total_net_carbs <= self.max_net_carbs and
            fat_pct >= 60  # At least 60% fat
        )

        # Calculate score (0-100)
        score = 100

        # Deduct points for carbs over limit
        if total_net_carbs > self.max_net_carbs:
            carb_overage = total_net_carbs - self.max_net_carbs
            score -= min(50, carb_overage * 5)  # -5 points per gram over, max -50

        # Deduct points for fat ratio under target
        if fat_pct < self.target_fat_percentage:
            fat_shortage = self.target_fat_percentage - fat_pct
            score -= min(30, fat_shortage)  # -1 point per percent under, max -30

        # Deduct points for protein far from target
        protein_diff = abs(total_protein - target_protein)
        if protein_diff > 20:
            score -= min(20, (protein_diff - 20) * 0.5)

        score = max(0, score)

        # Generate recommendations
        recommendations = []
        warnings = []

        if total_net_carbs > self.max_net_carbs:
            warnings.append(
                f"⚠️  Net carbs ({total_net_carbs:.1f}g) exceed daily limit ({self.max_net_carbs}g)"
            )
            recommendations.append(
                "Reduce portions of higher-carb foods or eliminate some"
            )

        if fat_pct < 60:
            warnings.append(
                f"⚠️  Fat percentage ({fat_pct:.1f}%) is below keto range (should be >60%)"
            )
            recommendations.append(
                "Add healthy fats: MCT oil, olive oil, avocado, fatty fish"
            )

        if total_protein < target_protein * 0.8:
            warnings.append(
                f"⚠️  Protein ({total_protein:.1f}g) is below target ({target_protein:.1f}g)"
            )
            recommendations.append(
                f"Increase protein to ~{target_protein:.0f}g with lean meats or fish"
            )
        elif total_protein > target_protein * 1.5:
            warnings.append(
                f"⚠️  Protein ({total_protein:.1f}g) is well above target ({target_protein:.1f}g)"
            )
            recommendations.append(
                "Excess protein can affect ketosis; consider reducing portions"
            )

        if not warnings:
            recommendations.append("✅ Protocol is keto-compatible!")

        return KetoCompatibility(
            is_keto_friendly=is_keto,
            compatibility_score=round(score, 1),
            net_carbs_per_day=round(total_net_carbs, 1),
            protein_per_day=round(total_protein, 1),
            fat_per_day=round(total_fat, 1),
            macro_ratios={
                "carbs": round(carb_pct, 1),
                "protein": round(protein_pct, 1),
                "fat": round(fat_pct, 1),
            },
            recommendations=recommendations,
            warnings=warnings,
        )

    def suggest_keto_additions(self, current_net_carbs: float,
                              current_fat_pct: float) -> List[Dict]:
        """
        Suggest keto-friendly additions to improve macros

        Returns:
            List of suggested foods with amounts
        """
        suggestions = []

        carb_room = self.max_net_carbs - current_net_carbs

        # If fat percentage is low, suggest fat sources
        if current_fat_pct < 60:
            suggestions.append({
                "food": "MCT oil or coconut oil",
                "amount": "1-2 tablespoons (15-30ml)",
                "benefit": "Boosts ketone production",
                "net_carbs": 0,
            })

            suggestions.append({
                "food": "Avocado",
                "amount": "1/2 medium (75g)",
                "benefit": "Healthy fats, fiber, low carbs",
                "net_carbs": 2,
            })

            suggestions.append({
                "food": "Fatty fish (salmon, mackerel)",
                "amount": "100g",
                "benefit": "Omega-3s, protein, healthy fats",
                "net_carbs": 0,
            })

        # If there's carb room, suggest low-carb nutrient-dense foods
        if carb_room > 5:
            suggestions.append({
                "food": "Leafy greens (spinach, kale)",
                "amount": "100-200g",
                "benefit": "Micronutrients, very low carbs",
                "net_carbs": 1-2,
            })

            suggestions.append({
                "food": "Berries (raspberries, blackberries)",
                "amount": "50g",
                "benefit": "Antioxidants, anthocyanins (anti-cancer)",
                "net_carbs": 3,
            })

        return suggestions

    @staticmethod
    def get_keto_friendly_cancer_foods() -> List[Dict]:
        """
        Return list of foods that are both keto-friendly and anti-cancer

        Returns:
            List of food recommendations
        """
        return [
            {
                "name": "Broccoli",
                "net_carbs_per_100g": 4.0,
                "why_keto": "Low carb cruciferous vegetable",
                "why_anticancer": "Sulforaphane inhibits cancer cell growth",
                "max_daily_g": 500,
            },
            {
                "name": "Cauliflower",
                "net_carbs_per_100g": 3.0,
                "why_keto": "Very low carb, versatile",
                "why_anticancer": "Glucosinolates, cancer-protective compounds",
                "max_daily_g": 500,
            },
            {
                "name": "Kale",
                "net_carbs_per_100g": 5.0,
                "why_keto": "Nutrient-dense, low carb",
                "why_anticancer": "Multiple anti-cancer compounds",
                "max_daily_g": 300,
            },
            {
                "name": "Brussels Sprouts",
                "net_carbs_per_100g": 5.0,
                "why_keto": "Low carb cruciferous",
                "why_anticancer": "Sulforaphane, indole-3-carbinol",
                "max_daily_g": 300,
            },
            {
                "name": "Turmeric",
                "net_carbs_per_100g": 3.9,
                "why_keto": "Used in small amounts, negligible carbs",
                "why_anticancer": "Curcumin - powerful anti-inflammatory",
                "max_daily_g": 8,
            },
            {
                "name": "Ginger",
                "net_carbs_per_100g": 15.0,
                "why_keto": "Small amounts used, manageable carbs",
                "why_anticancer": "Gingerol shows anti-tumor effects",
                "max_daily_g": 6,
            },
            {
                "name": "Garlic",
                "net_carbs_per_100g": 30.0,
                "why_keto": "Very small amounts used",
                "why_anticancer": "Allicin and sulfur compounds",
                "max_daily_g": 10,  # ~3-4 cloves
            },
            {
                "name": "Green Tea (brewed)",
                "net_carbs_per_100g": 0,
                "why_keto": "Zero carbs",
                "why_anticancer": "EGCG - potent anti-cancer catechin",
                "max_daily_g": 1000,  # ~4-5 cups
            },
            {
                "name": "Fatty Fish (salmon, mackerel)",
                "net_carbs_per_100g": 0,
                "why_keto": "High fat, zero carbs",
                "why_anticancer": "Omega-3s reduce inflammation",
                "max_daily_g": 300,
            },
            {
                "name": "Berries (limited)",
                "net_carbs_per_100g": 6.0,
                "why_keto": "Lowest-carb fruits in moderation",
                "why_anticancer": "Anthocyanins, ellagic acid",
                "max_daily_g": 50,  # Small portion
            },
        ]


def demo_keto_checker():
    """Demonstrate the keto checker"""
    print("=" * 60)
    print("Keto Compatibility Checker Demo")
    print("=" * 60)

    checker = KetoChecker()

    # Jesse's example protocol
    jesse_weight_kg = 179 * 0.453592  # ~81 kg

    sample_protocol = [
        {
            "name": "Broccoli",
            "amount_grams": 200,
            "net_carbs_per_100g": 4.0,
            "protein_per_100g": 2.8,
            "fat_per_100g": 0.4,
            "fiber_per_100g": 2.6,
        },
        {
            "name": "Ginger",
            "amount_grams": 5,
            "net_carbs_per_100g": 15.0,
            "protein_per_100g": 1.8,
            "fat_per_100g": 0.8,
            "fiber_per_100g": 2.0,
        },
        {
            "name": "Turmeric",
            "amount_grams": 5,
            "net_carbs_per_100g": 3.9,
            "protein_per_100g": 7.8,
            "fat_per_100g": 9.9,
            "fiber_per_100g": 21.1,
        },
        {
            "name": "Salmon",
            "amount_grams": 150,
            "net_carbs_per_100g": 0,
            "protein_per_100g": 20.0,
            "fat_per_100g": 13.0,
            "fiber_per_100g": 0,
        },
    ]

    compat = checker.check_daily_protocol(sample_protocol, jesse_weight_kg)

    print(f"\nDaily Totals:")
    print(f"  Net Carbs: {compat.net_carbs_per_day}g (limit: {checker.max_net_carbs}g)")
    print(f"  Protein: {compat.protein_per_day}g")
    print(f"  Fat: {compat.fat_per_day}g")

    print(f"\nMacro Ratios:")
    print(f"  Carbs: {compat.macro_ratios['carbs']}%")
    print(f"  Protein: {compat.macro_ratios['protein']}%")
    print(f"  Fat: {compat.macro_ratios['fat']}%")

    print(f"\nKeto Compatibility Score: {compat.compatibility_score}/100")
    print(f"Keto-Friendly: {'✅ Yes' if compat.is_keto_friendly else '❌ No'}")

    if compat.warnings:
        print(f"\n⚠️  Warnings:")
        for warning in compat.warnings:
            print(f"  {warning}")

    if compat.recommendations:
        print(f"\n💡 Recommendations:")
        for rec in compat.recommendations:
            print(f"  {rec}")

    print("\n" + "=" * 60)
    print("Keto-Friendly Anti-Cancer Foods:")
    print("=" * 60)

    for food in checker.get_keto_friendly_cancer_foods():
        print(f"\n{food['name']}")
        print(f"  Net carbs: {food['net_carbs_per_100g']}g per 100g")
        print(f"  Keto: {food['why_keto']}")
        print(f"  Anti-cancer: {food['why_anticancer']}")
        print(f"  Max daily: {food['max_daily_g']}g")


if __name__ == "__main__":
    demo_keto_checker()
