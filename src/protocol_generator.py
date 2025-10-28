"""
Daily protocol generator for No Colon, Still Rollin'
Generates personalized anti-cancer food protocols
"""
import argparse
from datetime import datetime, date
from typing import List, Dict, Optional
import json

from database import Database
from dosing_calculator import DosingCalculator
from keto_checker import KetoChecker
from models import PreparationMethod


class ProtocolGenerator:
    """Generate daily food protocols"""

    def __init__(self):
        self.db = Database()
        self.dosing_calc = DosingCalculator()
        self.keto_checker = KetoChecker()

    def generate_daily_protocol(self, user_name: str = "Jesse Mills",
                                weight_lbs: Optional[float] = None,
                                target_date: Optional[str] = None) -> Dict:
        """
        Generate a complete daily protocol

        Args:
            user_name: User's name
            weight_lbs: Current weight (if None, uses stored weight)
            target_date: Date for protocol (default: today)

        Returns:
            Complete daily protocol
        """
        # Get user
        user = self.db.get_user(name=user_name)
        if not user:
            raise ValueError(f"User '{user_name}' not found. Run init_database.py first.")

        # Use provided weight or stored weight
        if weight_lbs is None:
            weight_lbs = user['current_weight_lbs']

        # Date
        if target_date is None:
            target_date = date.today().isoformat()

        print(f"\n{'='*60}")
        print(f"Generating Protocol for {user_name}")
        print(f"{'='*60}")
        print(f"Date: {target_date}")
        print(f"Weight: {weight_lbs} lbs ({weight_lbs * 0.453592:.1f} kg)")
        print(f"Cancer type: {user['cancer_type']}")
        print()

        # Get all anti-cancer foods
        all_foods = self.db.get_all_foods()

        # Filter for best foods for this cancer type
        relevant_foods = [
            f for f in all_foods
            if user['cancer_type'] in f.get('cancer_types', []) or 'general' in f.get('cancer_types', [])
        ]

        print(f"Found {len(relevant_foods)} relevant anti-cancer foods")
        print()

        # Generate protocol foods
        protocol_foods = []

        for food_data in relevant_foods:
            # Get research for this food
            research = self.db.get_research_for_food(
                food_data['name'],
                user['cancer_type']
            )

            # Calculate recommended dose
            food_protocol = self._calculate_food_dose(
                food_data,
                weight_lbs,
                research
            )

            if food_protocol:
                protocol_foods.append(food_protocol)

        # Check keto compatibility
        print("Checking keto compatibility...")
        weight_kg = weight_lbs * 0.453592
        keto_result = self.keto_checker.check_daily_protocol(
            protocol_foods,
            weight_kg
        )

        # If not keto-compatible, adjust
        if not keto_result.is_keto_friendly:
            print(f"⚠️  Protocol needs adjustment for keto compatibility")
            protocol_foods = self._adjust_for_keto(
                protocol_foods,
                keto_result,
                weight_kg
            )
            # Re-check
            keto_result = self.keto_checker.check_daily_protocol(
                protocol_foods,
                weight_kg
            )

        # Calculate totals
        total_net_carbs = sum(f.get('net_carbs', 0) for f in protocol_foods)
        total_protein = sum(f.get('protein', 0) for f in protocol_foods)
        total_fat = sum(f.get('fat', 0) for f in protocol_foods)
        total_calories = (total_net_carbs * 4) + (total_protein * 4) + (total_fat * 9)

        # Create protocol
        protocol = {
            "user_id": user['id'],
            "date": target_date,
            "weight_lbs": weight_lbs,
            "foods": protocol_foods,
            "total_net_carbs": round(total_net_carbs, 1),
            "total_protein": round(total_protein, 1),
            "total_fat": round(total_fat, 1),
            "total_calories": round(total_calories, 0),
            "keto_compatible": keto_result.is_keto_friendly,
            "keto_score": keto_result.compatibility_score,
        }

        # Save to database
        protocol_id = self.db.save_daily_protocol(protocol)
        print(f"\n✅ Protocol saved (ID: {protocol_id})")

        return protocol

    def _calculate_food_dose(self, food_data: Dict, weight_lbs: float,
                            research: List[Dict]) -> Optional[Dict]:
        """Calculate dose for a single food"""

        food_name = food_data['name']

        # Use a default therapeutic dose based on food type
        # In a real scenario, we'd calculate from research studies
        dose_grams = self._get_default_dose(food_name)

        # Check safety
        max_safe = food_data.get('max_daily_amount_grams', 1000)
        if dose_grams > max_safe:
            dose_grams = max_safe

        # Calculate schedule
        schedule = self.dosing_calc.recommend_dosing_schedule(
            dose_grams,
            food_name
        )

        # Calculate macros
        multiplier = dose_grams / 100
        net_carbs = food_data['net_carbs_per_100g'] * multiplier
        protein = food_data['protein_per_100g'] * multiplier
        fat = food_data['fat_per_100g'] * multiplier

        # Build protocol food entry
        return {
            "name": food_name,
            "amount_grams": dose_grams,
            "net_carbs_per_100g": food_data['net_carbs_per_100g'],
            "protein_per_100g": food_data['protein_per_100g'],
            "fat_per_100g": food_data['fat_per_100g'],
            "net_carbs": round(net_carbs, 1),
            "protein": round(protein, 1),
            "fat": round(fat, 1),
            "servings_per_day": schedule["servings_per_day"],
            "grams_per_serving": schedule["grams_per_serving"],
            "timing": schedule["timing"],
            "timing_notes": schedule["timing_notes"],
            "preparation": food_data['best_preparation'],
            "preparation_notes": food_data['preparation_notes'],
            "reason": f"Anti-cancer compounds: {', '.join([c['name'] for c in food_data.get('active_compounds', [])])}",
            "mechanisms": food_data.get('mechanisms', []),
            "safety_notes": f"Max safe dose: {max_safe}g/day",
        }

    def _get_default_dose(self, food_name: str) -> float:
        """
        Get default therapeutic dose for a food

        These are conservative doses based on typical research
        and traditional use. Will be refined with actual research data.
        """
        defaults = {
            "Ginger": 4.0,  # 4g raw ginger per day
            "Garlic": 10.0,  # ~3 cloves
            "Turmeric": 5.0,  # 5g powder (about 150mg curcumin with pepper)
            "Broccoli": 200.0,  # 200g per day
            "Cauliflower": 150.0,
            "Kale": 100.0,
            "Brussels Sprouts": 150.0,
            "Green Tea": 750.0,  # ~3-4 cups
        }

        return defaults.get(food_name, 100.0)

    def _adjust_for_keto(self, foods: List[Dict],
                        keto_result, weight_kg: float) -> List[Dict]:
        """Adjust food amounts to be keto-compatible"""

        # If carbs are too high, reduce higher-carb foods
        if keto_result.net_carbs_per_day > self.keto_checker.max_net_carbs:
            # Sort by net carbs
            foods_by_carbs = sorted(
                foods,
                key=lambda f: f.get('net_carbs', 0),
                reverse=True
            )

            # Reduce highest-carb foods first
            carb_reduction_needed = keto_result.net_carbs_per_day - self.keto_checker.max_net_carbs

            for food in foods_by_carbs:
                if carb_reduction_needed <= 0:
                    break

                current_carbs = food.get('net_carbs', 0)
                if current_carbs > 2:  # Only adjust if significant carbs
                    # Reduce by 25%
                    reduction = current_carbs * 0.25
                    new_amount = food['amount_grams'] * 0.75

                    # Recalculate macros
                    multiplier = new_amount / 100
                    food['amount_grams'] = round(new_amount, 1)
                    food['net_carbs'] = round(food['net_carbs_per_100g'] * multiplier, 1)
                    food['protein'] = round(food['protein_per_100g'] * multiplier, 1)
                    food['fat'] = round(food['fat_per_100g'] * multiplier, 1)
                    food['grams_per_serving'] = round(new_amount / food['servings_per_day'], 1)

                    carb_reduction_needed -= reduction

        # If fat percentage is too low, suggest adding fat sources
        if keto_result.macro_ratios['fat'] < 60:
            print("\n💡 Add fat sources to reach keto ratios:")
            suggestions = self.keto_checker.suggest_keto_additions(
                keto_result.net_carbs_per_day,
                keto_result.macro_ratios['fat']
            )
            for suggestion in suggestions:
                print(f"  - {suggestion['food']}: {suggestion['amount']}")

        return foods

    def print_protocol(self, protocol: Dict):
        """Print protocol in human-readable format"""

        print("\n" + "="*60)
        print(f"DAILY PROTOCOL - {protocol['date']}")
        print("="*60)
        print()

        print("FOODS:")
        print("-"*60)

        for i, food in enumerate(protocol['foods'], 1):
            print(f"\n{i}. {food['name'].upper()}")
            print(f"   Amount: {food['amount_grams']}g per day")
            print(f"   Schedule: {food['timing']} ({food['servings_per_day']}x {food['grams_per_serving']}g)")
            print(f"   Timing: {food['timing_notes']}")
            print(f"   Preparation: {food['preparation']}")
            if food['preparation_notes']:
                print(f"   Notes: {food['preparation_notes']}")
            print(f"   Why: {food['reason']}")

        print("\n" + "-"*60)
        print("DAILY TOTALS:")
        print("-"*60)
        print(f"Net Carbs: {protocol['total_net_carbs']}g")
        print(f"Protein: {protocol['total_protein']}g")
        print(f"Fat: {protocol['total_fat']}g")
        print(f"Calories: {protocol['total_calories']}")

        print()
        print("KETO COMPATIBILITY:")
        print("-"*60)
        print(f"Score: {protocol['keto_score']}/100")
        print(f"Status: {'✅ Keto-friendly' if protocol['keto_compatible'] else '⚠️  Needs adjustment'}")

        print("\n" + "="*60)


def main():
    """Command line interface"""
    parser = argparse.ArgumentParser(
        description="Generate daily anti-cancer food protocol"
    )
    parser.add_argument(
        "--user",
        default="Jesse Mills",
        help="User name (default: Jesse Mills)"
    )
    parser.add_argument(
        "--weight",
        type=float,
        help="Current weight in pounds (default: use stored weight)"
    )
    parser.add_argument(
        "--date",
        help="Date for protocol (YYYY-MM-DD, default: today)"
    )
    parser.add_argument(
        "--save-json",
        help="Save protocol to JSON file"
    )

    args = parser.parse_args()

    # Generate protocol
    generator = ProtocolGenerator()

    try:
        protocol = generator.generate_daily_protocol(
            user_name=args.user,
            weight_lbs=args.weight,
            target_date=args.date
        )

        # Print it
        generator.print_protocol(protocol)

        # Save JSON if requested
        if args.save_json:
            with open(args.save_json, 'w') as f:
                json.dump(protocol, f, indent=2)
            print(f"\n✅ Saved to {args.save_json}")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
