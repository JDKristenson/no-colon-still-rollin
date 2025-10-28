"""
Dosing calculator for No Colon, Still Rollin'
Converts animal/in-vitro doses to human therapeutic doses
Uses FDA allometric scaling guidelines
"""
from typing import Dict, Optional
from dataclasses import dataclass

from config import ALLOMETRIC_SCALING, SAFETY_LIMITS


@dataclass
class DoseRecommendation:
    """A dose recommendation with safety checks"""
    food_name: str
    compound_name: str

    # Calculated dose
    recommended_grams_per_day: float
    recommended_servings_per_day: int
    grams_per_serving: float

    # Timing
    timing: str  # "once daily", "twice daily", etc.
    timing_notes: str  # "with meals", "morning and evening"

    # Preparation
    preparation: str  # "raw", "cooked", "powdered"
    preparation_notes: str

    # Safety
    within_safety_limits: bool
    safety_notes: str
    max_safe_dose_grams: float

    # Evidence
    based_on_study_type: str  # "animal", "human_clinical", etc.
    confidence_level: str  # "high", "medium", "low"
    citations: list


class DosingCalculator:
    """Calculate human doses from research studies"""

    def __init__(self):
        self.mouse_factor = ALLOMETRIC_SCALING["mouse_to_human"]
        self.rat_factor = ALLOMETRIC_SCALING["rat_to_human"]
        self.standard_mouse_weight = ALLOMETRIC_SCALING["standard_mouse_weight_kg"]
        self.standard_rat_weight = ALLOMETRIC_SCALING["standard_rat_weight_kg"]

    def mouse_to_human_dose(self, mouse_dose_mg_kg: float,
                           human_weight_kg: float,
                           mouse_weight_kg: Optional[float] = None) -> float:
        """
        Convert mouse dose to human dose using FDA allometric scaling

        Args:
            mouse_dose_mg_kg: Dose given to mouse in mg/kg
            human_weight_kg: Human's weight in kg
            mouse_weight_kg: Mouse weight (default: 0.02 kg = 20g)

        Returns:
            Human dose in mg/kg

        FDA Formula:
        Human dose (mg/kg) = Mouse dose (mg/kg) × (Mouse weight / Human weight)^0.33
        Simplified: Human dose (mg/kg) = Mouse dose (mg/kg) × 0.08
        """
        if mouse_weight_kg is None:
            mouse_weight_kg = self.standard_mouse_weight

        # FDA simplified factor
        human_dose_mg_kg = mouse_dose_mg_kg * self.mouse_factor

        # Total dose for this human
        total_dose_mg = human_dose_mg_kg * human_weight_kg

        return total_dose_mg / 1000  # Convert to grams

    def rat_to_human_dose(self, rat_dose_mg_kg: float,
                         human_weight_kg: float,
                         rat_weight_kg: Optional[float] = None) -> float:
        """
        Convert rat dose to human dose

        Args:
            rat_dose_mg_kg: Dose given to rat in mg/kg
            human_weight_kg: Human's weight in kg
            rat_weight_kg: Rat weight (default: 0.2 kg = 200g)

        Returns:
            Human dose in grams
        """
        if rat_weight_kg is None:
            rat_weight_kg = self.standard_rat_weight

        # FDA simplified factor
        human_dose_mg_kg = rat_dose_mg_kg * self.rat_factor
        total_dose_mg = human_dose_mg_kg * human_weight_kg

        return total_dose_mg / 1000  # Convert to grams

    def in_vitro_to_human_dose(self, concentration_uM: float,
                               bioavailability: float = 0.2) -> float:
        """
        Estimate human dose from in vitro concentration

        This is highly approximate since in vitro doesn't translate directly.
        Uses conservative assumptions.

        Args:
            concentration_uM: Effective concentration in micromolar
            bioavailability: Estimated oral bioavailability (0-1)

        Returns:
            Estimated human dose in grams
        """
        # Very rough approximation
        # Assume average body water volume of 42L for 70kg person
        # Adjust proportionally for different weights

        # This is a placeholder - real calculation would need:
        # - Molecular weight of compound
        # - Volume of distribution
        # - Clearance rate
        # - Bioavailability

        # For now, use a conservative multiplier
        estimated_grams = (concentration_uM * 0.01) / bioavailability

        return max(estimated_grams, 0.1)  # Minimum 0.1g

    def calculate_food_dose_from_compound(self, compound_dose_grams: float,
                                         compound_concentration_per_100g: float) -> float:
        """
        Calculate how much of the whole food is needed to get compound dose

        Args:
            compound_dose_grams: Desired amount of active compound in grams
            compound_concentration_per_100g: mg of compound per 100g of food

        Returns:
            Grams of food needed

        Example:
            Gingerol concentration in raw ginger: ~500 mg per 100g
            To get 2g of gingerol: (2000 mg / 500 mg) * 100g = 400g ginger
        """
        compound_dose_mg = compound_dose_grams * 1000
        grams_of_food = (compound_dose_mg / compound_concentration_per_100g) * 100

        return grams_of_food

    def check_safety(self, food_name: str, dose_grams: float) -> Dict:
        """
        Check if dose is within safety limits

        Args:
            food_name: Name of food
            dose_grams: Proposed dose in grams

        Returns:
            Dict with safety info
        """
        # Normalize food name
        food_key = food_name.lower().replace(" ", "_")

        max_safe = SAFETY_LIMITS.get(food_key, 1000)  # Default 1kg

        within_limits = dose_grams <= max_safe

        safety_info = {
            "within_limits": within_limits,
            "max_safe_dose": max_safe,
            "proposed_dose": dose_grams,
            "safety_margin": max_safe - dose_grams,
            "notes": "",
        }

        if not within_limits:
            safety_info["notes"] = f"⚠️  Proposed dose ({dose_grams}g) exceeds " \
                                  f"maximum safe dose ({max_safe}g)"
        elif dose_grams > (max_safe * 0.8):
            safety_info["notes"] = f"⚠️  Proposed dose is near maximum safe limit"

        return safety_info

    def recommend_dosing_schedule(self, total_daily_grams: float,
                                 food_name: str) -> Dict:
        """
        Recommend how to divide dose throughout the day

        Args:
            total_daily_grams: Total grams per day
            food_name: Name of food

        Returns:
            Dict with schedule recommendation
        """
        food_lower = food_name.lower()

        # Default: once daily
        servings = 1
        timing = "once daily"
        timing_notes = "with a meal"

        # Adjust based on food type and amount
        if "ginger" in food_lower or "garlic" in food_lower:
            # Pungent foods - better split up
            if total_daily_grams > 4:
                servings = 2
                timing = "twice daily"
                timing_notes = "morning and evening with meals"
            elif total_daily_grams > 8:
                servings = 3
                timing = "three times daily"
                timing_notes = "with each main meal"

        elif "turmeric" in food_lower or "curcumin" in food_lower:
            # Better absorption with fat and pepper
            if total_daily_grams > 3:
                servings = 2
                timing = "twice daily"
                timing_notes = "with meals containing fat and black pepper"
            else:
                timing_notes = "with meal containing fat and black pepper"

        elif any(veg in food_lower for veg in ["broccoli", "kale", "cauliflower", "brussels"]):
            # Cruciferous vegetables
            if total_daily_grams > 200:
                servings = 2
                timing = "twice daily"
                timing_notes = "with lunch and dinner"
            else:
                timing_notes = "with main meal"

        grams_per_serving = total_daily_grams / servings

        return {
            "servings_per_day": servings,
            "grams_per_serving": round(grams_per_serving, 1),
            "timing": timing,
            "timing_notes": timing_notes,
        }

    def generate_recommendation(self, food_name: str,
                               compound_name: str,
                               study_dose_mg_kg: float,
                               study_type: str,
                               human_weight_lbs: float,
                               compound_concentration_per_100g: float = None,
                               bioavailability: float = 1.0) -> DoseRecommendation:
        """
        Generate complete dose recommendation

        Args:
            food_name: Name of food
            compound_name: Active compound
            study_dose_mg_kg: Dose from study
            study_type: "animal", "in_vitro", "human_clinical"
            human_weight_lbs: Person's weight in pounds
            compound_concentration_per_100g: mg of compound per 100g food
            bioavailability: Absorption rate (0-1)

        Returns:
            DoseRecommendation object
        """
        # Convert weight to kg
        human_weight_kg = human_weight_lbs * 0.453592

        # Calculate base dose based on study type
        if study_type == "animal":
            # Assume mouse unless specified
            compound_dose_g = self.mouse_to_human_dose(
                study_dose_mg_kg,
                human_weight_kg
            )
        elif study_type == "in_vitro":
            # Very approximate
            compound_dose_g = self.in_vitro_to_human_dose(
                study_dose_mg_kg,  # Actually concentration
                bioavailability
            )
        elif study_type == "human_clinical":
            # Direct conversion
            compound_dose_g = (study_dose_mg_kg * human_weight_kg) / 1000
        else:
            # Conservative estimate
            compound_dose_g = self.mouse_to_human_dose(
                study_dose_mg_kg,
                human_weight_kg
            ) * 0.5  # Extra safety factor

        # If we know compound concentration, calculate food amount
        if compound_concentration_per_100g:
            food_dose_g = self.calculate_food_dose_from_compound(
                compound_dose_g,
                compound_concentration_per_100g
            )
        else:
            # Direct food dose (whole food was studied)
            food_dose_g = compound_dose_g * 1000  # mg to g

        # Check safety
        safety = self.check_safety(food_name, food_dose_g)

        # If unsafe, reduce to maximum safe dose
        if not safety["within_limits"]:
            food_dose_g = safety["max_safe_dose"]
            safety["notes"] += " Dose reduced to maximum safe limit."

        # Recommend schedule
        schedule = self.recommend_dosing_schedule(food_dose_g, food_name)

        # Assess confidence
        confidence = "medium"
        if study_type == "human_clinical":
            confidence = "high"
        elif study_type == "meta_analysis":
            confidence = "high"
        elif study_type == "in_vitro":
            confidence = "low"

        return DoseRecommendation(
            food_name=food_name,
            compound_name=compound_name,
            recommended_grams_per_day=round(food_dose_g, 1),
            recommended_servings_per_day=schedule["servings_per_day"],
            grams_per_serving=schedule["grams_per_serving"],
            timing=schedule["timing"],
            timing_notes=schedule["timing_notes"],
            preparation="raw",  # Default, will be refined later
            preparation_notes="",
            within_safety_limits=safety["within_limits"],
            safety_notes=safety["notes"],
            max_safe_dose_grams=safety["max_safe_dose"],
            based_on_study_type=study_type,
            confidence_level=confidence,
            citations=[],
        )


def demo_dosing_calculator():
    """Demonstrate the dosing calculator"""
    print("=" * 60)
    print("Dosing Calculator Demo")
    print("=" * 60)

    calc = DosingCalculator()
    jesse_weight = 179  # lbs

    # Example 1: Ginger from mouse study
    print("\n1. GINGER (from mouse study)")
    print("-" * 60)
    print("Study: Mice given 100 mg/kg/day of ginger extract")
    print("Active compound: Gingerol (~500 mg per 100g raw ginger)")

    ginger_rec = calc.generate_recommendation(
        food_name="ginger",
        compound_name="gingerol",
        study_dose_mg_kg=100,
        study_type="animal",
        human_weight_lbs=jesse_weight,
        compound_concentration_per_100g=500,  # mg per 100g
    )

    print(f"\nRecommendation:")
    print(f"  Total daily: {ginger_rec.recommended_grams_per_day}g raw ginger")
    print(f"  Schedule: {ginger_rec.timing}")
    print(f"  Per serving: {ginger_rec.grams_per_serving}g")
    print(f"  How: {ginger_rec.timing_notes}")
    print(f"  Safety: {'✅ Within limits' if ginger_rec.within_safety_limits else '⚠️ Exceeds limits'}")
    print(f"  Confidence: {ginger_rec.confidence_level}")

    # Example 2: Curcumin from human trial
    print("\n\n2. TURMERIC/CURCUMIN (from human clinical trial)")
    print("-" * 60)
    print("Study: Humans given 3000 mg/day curcumin")
    print("Curcumin content: ~3% in turmeric powder")

    turmeric_rec = calc.generate_recommendation(
        food_name="turmeric",
        compound_name="curcumin",
        study_dose_mg_kg=3000 / 70,  # Assuming 70kg person in study
        study_type="human_clinical",
        human_weight_lbs=jesse_weight,
        compound_concentration_per_100g=3000,  # 3g per 100g
        bioavailability=0.2,  # Curcumin has low bioavailability
    )

    print(f"\nRecommendation:")
    print(f"  Total daily: {turmeric_rec.recommended_grams_per_day}g turmeric")
    print(f"  Schedule: {turmeric_rec.timing}")
    print(f"  Per serving: {turmeric_rec.grams_per_serving}g")
    print(f"  How: {turmeric_rec.timing_notes}")
    print(f"  Safety: {'✅ Within limits' if turmeric_rec.within_safety_limits else '⚠️ Exceeds limits'}")
    print(f"  Confidence: {turmeric_rec.confidence_level}")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    demo_dosing_calculator()
