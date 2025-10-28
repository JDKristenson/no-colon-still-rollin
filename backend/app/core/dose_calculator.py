"""
Dose Calculator for Converting Animal/In Vitro Studies to Human Equivalent Doses
Uses FDA allometric scaling and standard conversion factors
"""
from typing import Dict, Optional
from enum import Enum


class StudyType(str, Enum):
    """Types of preclinical studies"""
    PETRI_DISH = "petri_dish"  # In vitro, cell culture
    MOUSE = "mouse"
    RAT = "rat"
    RABBIT = "rabbit"
    DOG = "dog"
    MONKEY = "monkey"
    HUMAN = "human"


# FDA Body Surface Area (BSA) Conversion Factors
# Based on FDA Guidance for Industry: Estimating the Maximum Safe Starting Dose
BSA_FACTORS = {
    StudyType.MOUSE: 3,      # 20g mouse
    StudyType.RAT: 6,        # 200g rat
    StudyType.RABBIT: 12,    # 1.8kg rabbit
    StudyType.DOG: 20,       # 10kg dog
    StudyType.MONKEY: 12,    # 3kg monkey
    StudyType.HUMAN: 37,     # 60kg human (default)
}


class DoseCalculator:
    """Calculate human equivalent doses from animal studies"""

    @staticmethod
    def animal_to_human_bsa(
        animal_dose_mg_kg: float,
        animal_type: StudyType,
        human_weight_kg: float = 70
    ) -> Dict:
        """
        Convert animal dose to Human Equivalent Dose (HED) using BSA method

        Formula: HED (mg/kg) = Animal Dose (mg/kg) × (Animal Km / Human Km)
        Where Km = body weight (kg) / body surface area (m²)

        Args:
            animal_dose_mg_kg: Dose in mg/kg given to animals
            animal_type: Type of animal (mouse, rat, etc.)
            human_weight_kg: Human body weight in kg (default 70kg)

        Returns:
            Dictionary with calculated doses and details
        """
        if animal_type == StudyType.PETRI_DISH:
            return {
                "error": "Cannot calculate dose from petri dish studies",
                "explanation": "In vitro (petri dish) studies show biological activity but don't provide dosing information. Look for animal studies or human trials for dose guidance."
            }

        if animal_type == StudyType.HUMAN:
            return {
                "human_dose_mg_kg": animal_dose_mg_kg,
                "total_dose_mg": animal_dose_mg_kg * human_weight_kg,
                "source": "human",
                "note": "This is already a human dose"
            }

        # Get conversion factors
        animal_km = BSA_FACTORS[animal_type]
        human_km = BSA_FACTORS[StudyType.HUMAN]

        # Calculate HED
        hed_mg_kg = animal_dose_mg_kg * (animal_km / human_km)
        total_dose_mg = hed_mg_kg * human_weight_kg

        # Safety factor (typically divide by 10 for first-in-human)
        conservative_hed_mg_kg = hed_mg_kg / 10
        conservative_total_mg = conservative_hed_mg_kg * human_weight_kg

        return {
            "animal_dose_mg_kg": animal_dose_mg_kg,
            "animal_type": animal_type.value,
            "human_weight_kg": human_weight_kg,

            "calculated_hed_mg_kg": round(hed_mg_kg, 3),
            "calculated_total_mg": round(total_dose_mg, 1),

            "conservative_hed_mg_kg": round(conservative_hed_mg_kg, 3),
            "conservative_total_mg": round(conservative_total_mg, 1),

            "method": "FDA Allometric Scaling (BSA)",
            "safety_note": "Conservative dose includes 10x safety factor. Start low and increase gradually.",
            "conversion_factor": round(animal_km / human_km, 4)
        }

    @staticmethod
    def food_dose_to_daily_amount(
        dose_mg: float,
        compound_per_100g_food: float,
        food_name: str
    ) -> Dict:
        """
        Convert compound dose (mg) to daily food amount (grams)

        Args:
            dose_mg: Desired dose of active compound in mg
            compound_per_100g_food: Amount of compound per 100g of food (mg)
            food_name: Name of the food

        Returns:
            Dictionary with food amounts needed
        """
        if compound_per_100g_food <= 0:
            return {
                "error": "Invalid compound amount",
                "explanation": "Compound amount per 100g must be greater than 0"
            }

        # Calculate grams of food needed
        grams_needed = (dose_mg / compound_per_100g_food) * 100

        # Convert to practical measurements
        tablespoons = grams_needed / 15  # Approx 15g per tablespoon
        teaspoons = grams_needed / 5     # Approx 5g per teaspoon

        return {
            "target_dose_mg": dose_mg,
            "food_name": food_name,
            "compound_per_100g": compound_per_100g_food,

            "grams_needed": round(grams_needed, 1),
            "tablespoons": round(tablespoons, 1),
            "teaspoons": round(teaspoons, 1),

            "practical_note": f"Approximately {round(grams_needed, 0)}g of {food_name} per day"
        }

    @staticmethod
    def calculate_full_protocol(
        study_dose_mg_kg: float,
        study_type: StudyType,
        compound_name: str,
        food_name: str,
        compound_per_100g_food: float,
        human_weight_kg: float = 70
    ) -> Dict:
        """
        Complete calculation from study to daily food intake

        Args:
            study_dose_mg_kg: Dose used in study (mg/kg)
            study_type: Type of study (mouse, rat, etc.)
            compound_name: Name of active compound
            food_name: Food containing the compound
            compound_per_100g_food: Compound amount per 100g food
            human_weight_kg: Human body weight

        Returns:
            Complete protocol with all calculations
        """
        # Step 1: Convert animal dose to human dose
        hed = DoseCalculator.animal_to_human_bsa(
            study_dose_mg_kg,
            study_type,
            human_weight_kg
        )

        if "error" in hed:
            return hed

        # Step 2: Calculate food amounts for both calculated and conservative doses
        calculated_food = DoseCalculator.food_dose_to_daily_amount(
            hed["calculated_total_mg"],
            compound_per_100g_food,
            food_name
        )

        conservative_food = DoseCalculator.food_dose_to_daily_amount(
            hed["conservative_total_mg"],
            compound_per_100g_food,
            food_name
        )

        return {
            "compound": compound_name,
            "food_source": food_name,
            "study_details": {
                "dose_mg_kg": study_dose_mg_kg,
                "study_type": study_type.value,
                "method": hed["method"]
            },
            "human_equivalent": {
                "weight_kg": human_weight_kg,
                "calculated_dose_mg": hed["calculated_total_mg"],
                "conservative_dose_mg": hed["conservative_total_mg"]
            },
            "daily_food_amounts": {
                "calculated": {
                    "grams": calculated_food["grams_needed"],
                    "tablespoons": calculated_food["tablespoons"],
                    "note": calculated_food["practical_note"]
                },
                "conservative": {
                    "grams": conservative_food["grams_needed"],
                    "tablespoons": conservative_food["tablespoons"],
                    "note": conservative_food["practical_note"]
                }
            },
            "recommendation": f"Start with {conservative_food['grams_needed']}g daily (conservative dose) and assess tolerance. May increase to {calculated_food['grams_needed']}g if well-tolerated.",
            "safety_note": hed["safety_note"]
        }


# Example usage and test cases
if __name__ == "__main__":
    calc = DoseCalculator()

    # Example: Mouse study with curcumin (turmeric)
    # Study: 50 mg/kg curcumin in mice showed anti-cancer effects
    # Turmeric contains ~3000mg curcumin per 100g

    result = calc.calculate_full_protocol(
        study_dose_mg_kg=50,
        study_type=StudyType.MOUSE,
        compound_name="curcumin",
        food_name="turmeric powder",
        compound_per_100g_food=3000,
        human_weight_kg=70
    )

    print("Example Calculation:")
    print(f"Compound: {result['compound']}")
    print(f"Food Source: {result['food_source']}")
    print(f"\nStudy Details:")
    print(f"  - Dose: {result['study_details']['dose_mg_kg']} mg/kg")
    print(f"  - Study Type: {result['study_details']['study_type']}")
    print(f"\nHuman Equivalent (70kg person):")
    print(f"  - Calculated: {result['human_equivalent']['calculated_dose_mg']} mg")
    print(f"  - Conservative: {result['human_equivalent']['conservative_dose_mg']} mg")
    print(f"\nDaily Food Amounts:")
    print(f"  - Conservative: {result['daily_food_amounts']['conservative']['grams']}g ({result['daily_food_amounts']['conservative']['tablespoons']} tbsp)")
    print(f"  - Calculated: {result['daily_food_amounts']['calculated']['grams']}g ({result['daily_food_amounts']['calculated']['tablespoons']} tbsp)")
    print(f"\nRecommendation: {result['recommendation']}")
