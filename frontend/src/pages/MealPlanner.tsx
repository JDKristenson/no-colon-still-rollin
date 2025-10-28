import { useQuery } from '@tanstack/react-query';
import { api } from '../lib/api';
import { useState } from 'react';

interface Recipe {
  id: string;
  name: string;
  meal: 'breakfast' | 'lunch' | 'dinner' | 'snack';
  protocolFoods: string[];
  ingredients: string[];
  instructions: string[];
  prepTime: string;
  notes?: string;
}

const RECIPES: Recipe[] = [
  {
    id: 'morning-tea',
    name: 'Morning Colon Support Tea',
    meal: 'breakfast',
    protocolFoods: ['Colon Support Herbal Tea'],
    ingredients: [
      '1-2 tsp colon support tea blend (peppermint, chamomile, ginger, fennel)',
      '8 oz hot water (200°F)',
    ],
    instructions: [
      'Heat water to just under boiling (200°F)',
      'Add tea blend to cup or tea infuser',
      'Steep for 5-7 minutes',
      'Strain and enjoy upon waking',
    ],
    prepTime: '10 minutes',
    notes: 'Take on empty stomach first thing in the morning',
  },
  {
    id: 'anti-cancer-smoothie',
    name: 'Anti-Cancer Power Smoothie',
    meal: 'breakfast',
    protocolFoods: ['Ginger', 'Turmeric', 'Kale'],
    ingredients: [
      '1 cup unsweetened almond milk',
      '½ cup kale (50g)',
      '1 tsp fresh ginger, grated (3g)',
      '1 tsp turmeric powder (2.5g)',
      'Pinch of black pepper (for turmeric absorption)',
      '½ avocado (healthy fats)',
      '5-6 ice cubes',
      'Optional: stevia for sweetness',
    ],
    instructions: [
      'Add all ingredients to blender',
      'Blend on high for 60 seconds until smooth',
      'Drink immediately',
    ],
    prepTime: '5 minutes',
    notes: 'The pepper increases turmeric absorption by 2000%',
  },
  {
    id: 'garlic-cauliflower-rice',
    name: 'Garlic Cauliflower Rice Bowl',
    meal: 'lunch',
    protocolFoods: ['Cauliflower', 'Garlic', 'Broccoli'],
    ingredients: [
      '150g cauliflower, riced',
      '100g broccoli florets',
      '3 cloves garlic, minced (9g)',
      '2 tbsp olive oil',
      'Salt and pepper to taste',
      'Optional: grilled chicken or salmon',
    ],
    instructions: [
      'Steam broccoli lightly for 3-4 minutes, set aside',
      'Crush garlic and let sit 10 minutes (activates allicin)',
      'Heat olive oil in pan',
      'Sauté garlic for 30 seconds',
      'Add cauliflower rice, cook 5-7 minutes',
      'Add steamed broccoli, mix well',
      'Season and serve',
    ],
    prepTime: '20 minutes',
    notes: 'Can meal prep for 3-4 days',
  },
  {
    id: 'brussels-sprouts-turmeric',
    name: 'Roasted Brussels Sprouts with Turmeric',
    meal: 'dinner',
    protocolFoods: ['Brussels Sprouts', 'Turmeric', 'Garlic'],
    ingredients: [
      '150g Brussels sprouts, halved',
      '1 clove garlic, minced (3g)',
      '1 tsp turmeric powder (2.5g)',
      '2 tbsp olive oil',
      'Pinch of black pepper',
      'Salt to taste',
    ],
    instructions: [
      'Preheat oven to 400°F',
      'Crush garlic, let sit 10 minutes',
      'Toss Brussels sprouts with oil, turmeric, garlic, pepper',
      'Spread on baking sheet',
      'Roast 20-25 minutes until crispy',
    ],
    prepTime: '30 minutes',
    notes: 'Don\'t overcook - keeps anti-cancer compounds active',
  },
  {
    id: 'kale-ginger-stir-fry',
    name: 'Kale & Ginger Stir-Fry',
    meal: 'dinner',
    protocolFoods: ['Kale', 'Ginger', 'Garlic'],
    ingredients: [
      '100g kale, chopped',
      '1 tsp fresh ginger, grated (3g)',
      '1 clove garlic, minced (3g)',
      '1 tbsp coconut oil',
      '1 tbsp coconut aminos or soy sauce',
      'Sesame seeds for garnish',
    ],
    instructions: [
      'Massage kale to break down cellulose',
      'Crush garlic, let sit 10 minutes',
      'Heat coconut oil in wok or large pan',
      'Add ginger and garlic, sauté 30 seconds',
      'Add kale, stir-fry 3-4 minutes',
      'Add coconut aminos, toss well',
      'Garnish with sesame seeds',
    ],
    prepTime: '15 minutes',
  },
  {
    id: 'green-tea-afternoon',
    name: 'Afternoon Green Tea',
    meal: 'snack',
    protocolFoods: ['Green Tea'],
    ingredients: [
      '1-2 tsp green tea leaves (or 2 green tea bags)',
      '8 oz water',
    ],
    instructions: [
      'Heat water to 160-180°F (NOT boiling)',
      'Steep green tea for 2-3 minutes',
      'Remove tea bags/strain',
      'Enjoy 2-3 cups throughout the day',
    ],
    prepTime: '5 minutes',
    notes: 'Don\'t boil water - destroys beneficial compounds. Take between meals for better iron absorption',
  },
  {
    id: 'evening-tea',
    name: 'Evening Colon Support Tea',
    meal: 'snack',
    protocolFoods: ['Colon Support Herbal Tea'],
    ingredients: [
      '1-2 tsp colon support tea blend',
      '8 oz hot water (200°F)',
    ],
    instructions: [
      'Heat water to just under boiling',
      'Steep tea for 5-7 minutes',
      'Strain and enjoy before bed',
    ],
    prepTime: '10 minutes',
    notes: 'Helps with digestion and promotes restful sleep',
  },
];

export default function MealPlanner() {
  const [selectedMeal, setSelectedMeal] = useState<string | null>(null);
  const [showShoppingList, setShowShoppingList] = useState(false);

  const { data: protocol } = useQuery({
    queryKey: ['protocol-today'],
    queryFn: api.getTodayProtocol,
    retry: false,
  });

  const selectedRecipe = RECIPES.find(r => r.id === selectedMeal);

  const shoppingList = {
    'Fresh Produce': [
      'Fresh ginger root (1-2 inches)',
      'Garlic bulb (1-2 heads)',
      'Kale (1 bunch)',
      'Broccoli (1 head)',
      'Cauliflower (1 head)',
      'Brussels sprouts (1 lb)',
      'Avocado (optional, for smoothies)',
    ],
    'Spices & Herbs': [
      'Turmeric powder (organic)',
      'Black pepper (fresh ground)',
      'Colon support tea blend (peppermint, chamomile, ginger, fennel) - or buy separately',
      'Green tea (loose leaf or bags)',
      'Salt',
    ],
    'Pantry': [
      'Olive oil (extra virgin)',
      'Coconut oil',
      'Coconut aminos or soy sauce',
      'Unsweetened almond milk',
      'Sesame seeds',
    ],
    'Optional': [
      'Stevia or monk fruit sweetener',
      'Chicken breast or salmon (protein)',
      'Eggs',
    ],
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Meal Planner</h1>
        <p className="mt-1 text-sm text-gray-500">Simple recipes to make protocol compliance easy</p>
      </div>

      {/* Quick Actions */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <div className="flex items-start">
          <svg className="h-6 w-6 text-blue-600 mr-3 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <div className="flex-1">
            <h3 className="font-semibold text-blue-900 mb-2">Compliance is Key</h3>
            <p className="text-sm text-blue-800 mb-3">
              These recipes make it easy to get all your protocol foods every day. Pick 2-3 recipes per day and you'll hit your targets.
            </p>
            <button
              onClick={() => setShowShoppingList(!showShoppingList)}
              className="bg-blue-600 text-white px-4 py-2 rounded-md text-sm hover:bg-blue-700"
            >
              {showShoppingList ? 'Hide' : 'Show'} Weekly Shopping List
            </button>
          </div>
        </div>
      </div>

      {/* Shopping List */}
      {showShoppingList && (
        <div className="bg-white shadow rounded-lg p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Weekly Shopping List</h2>
          <div className="grid md:grid-cols-2 gap-6">
            {Object.entries(shoppingList).map(([category, items]) => (
              <div key={category}>
                <h3 className="font-semibold text-primary mb-2">{category}</h3>
                <ul className="space-y-1">
                  {items.map((item, idx) => (
                    <li key={idx} className="flex items-start">
                      <span className="text-gray-400 mr-2">•</span>
                      <span className="text-gray-700">{item}</span>
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
          <div className="mt-6 bg-yellow-50 border border-yellow-200 rounded-md p-3">
            <p className="text-sm text-yellow-800">
              <span className="font-semibold">Tip:</span> Buy organic when possible, especially for cruciferous vegetables. Shop once per week to keep everything fresh.
            </p>
          </div>
        </div>
      )}

      {/* Recipe Categories */}
      <div className="space-y-6">
        {/* Breakfast */}
        <div className="bg-white shadow rounded-lg p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
            <span className="bg-orange-100 text-orange-800 px-2 py-1 rounded text-sm mr-2">Breakfast</span>
            Start Your Day Right
          </h2>
          <div className="grid md:grid-cols-2 gap-4">
            {RECIPES.filter(r => r.meal === 'breakfast').map(recipe => (
              <button
                key={recipe.id}
                onClick={() => setSelectedMeal(recipe.id)}
                className="text-left p-4 border-2 border-gray-200 rounded-lg hover:border-primary transition-colors"
              >
                <h3 className="font-semibold text-gray-900 mb-2">{recipe.name}</h3>
                <div className="flex flex-wrap gap-1 mb-2">
                  {recipe.protocolFoods.map(food => (
                    <span key={food} className="bg-green-100 text-green-800 text-xs px-2 py-1 rounded">
                      {food}
                    </span>
                  ))}
                </div>
                <p className="text-xs text-gray-500">⏱ {recipe.prepTime}</p>
              </button>
            ))}
          </div>
        </div>

        {/* Lunch */}
        <div className="bg-white shadow rounded-lg p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
            <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded text-sm mr-2">Lunch</span>
            Midday Fuel
          </h2>
          <div className="grid md:grid-cols-2 gap-4">
            {RECIPES.filter(r => r.meal === 'lunch').map(recipe => (
              <button
                key={recipe.id}
                onClick={() => setSelectedMeal(recipe.id)}
                className="text-left p-4 border-2 border-gray-200 rounded-lg hover:border-primary transition-colors"
              >
                <h3 className="font-semibold text-gray-900 mb-2">{recipe.name}</h3>
                <div className="flex flex-wrap gap-1 mb-2">
                  {recipe.protocolFoods.map(food => (
                    <span key={food} className="bg-green-100 text-green-800 text-xs px-2 py-1 rounded">
                      {food}
                    </span>
                  ))}
                </div>
                <p className="text-xs text-gray-500">⏱ {recipe.prepTime}</p>
              </button>
            ))}
          </div>
        </div>

        {/* Dinner */}
        <div className="bg-white shadow rounded-lg p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
            <span className="bg-purple-100 text-purple-800 px-2 py-1 rounded text-sm mr-2">Dinner</span>
            Evening Meals
          </h2>
          <div className="grid md:grid-cols-2 gap-4">
            {RECIPES.filter(r => r.meal === 'dinner').map(recipe => (
              <button
                key={recipe.id}
                onClick={() => setSelectedMeal(recipe.id)}
                className="text-left p-4 border-2 border-gray-200 rounded-lg hover:border-primary transition-colors"
              >
                <h3 className="font-semibold text-gray-900 mb-2">{recipe.name}</h3>
                <div className="flex flex-wrap gap-1 mb-2">
                  {recipe.protocolFoods.map(food => (
                    <span key={food} className="bg-green-100 text-green-800 text-xs px-2 py-1 rounded">
                      {food}
                    </span>
                  ))}
                </div>
                <p className="text-xs text-gray-500">⏱ {recipe.prepTime}</p>
              </button>
            ))}
          </div>
        </div>

        {/* Snacks & Teas */}
        <div className="bg-white shadow rounded-lg p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
            <span className="bg-green-100 text-green-800 px-2 py-1 rounded text-sm mr-2">Throughout Day</span>
            Teas & Beverages
          </h2>
          <div className="grid md:grid-cols-2 gap-4">
            {RECIPES.filter(r => r.meal === 'snack').map(recipe => (
              <button
                key={recipe.id}
                onClick={() => setSelectedMeal(recipe.id)}
                className="text-left p-4 border-2 border-gray-200 rounded-lg hover:border-primary transition-colors"
              >
                <h3 className="font-semibold text-gray-900 mb-2">{recipe.name}</h3>
                <div className="flex flex-wrap gap-1 mb-2">
                  {recipe.protocolFoods.map(food => (
                    <span key={food} className="bg-green-100 text-green-800 text-xs px-2 py-1 rounded">
                      {food}
                    </span>
                  ))}
                </div>
                <p className="text-xs text-gray-500">⏱ {recipe.prepTime}</p>
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Recipe Detail Modal */}
      {selectedRecipe && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto">
            <div className="p-6">
              <div className="flex justify-between items-start mb-4">
                <div>
                  <h2 className="text-2xl font-bold text-gray-900">{selectedRecipe.name}</h2>
                  <p className="text-sm text-gray-500">⏱ Prep time: {selectedRecipe.prepTime}</p>
                </div>
                <button
                  onClick={() => setSelectedMeal(null)}
                  className="text-gray-400 hover:text-gray-600"
                >
                  <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>

              <div className="mb-4">
                <h3 className="font-semibold text-gray-900 mb-2">Protocol Foods</h3>
                <div className="flex flex-wrap gap-2">
                  {selectedRecipe.protocolFoods.map(food => (
                    <span key={food} className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm">
                      ✓ {food}
                    </span>
                  ))}
                </div>
              </div>

              <div className="mb-4">
                <h3 className="font-semibold text-gray-900 mb-2">Ingredients</h3>
                <ul className="space-y-1">
                  {selectedRecipe.ingredients.map((ingredient, idx) => (
                    <li key={idx} className="flex items-start">
                      <span className="text-primary mr-2">•</span>
                      <span className="text-gray-700">{ingredient}</span>
                    </li>
                  ))}
                </ul>
              </div>

              <div className="mb-4">
                <h3 className="font-semibold text-gray-900 mb-2">Instructions</h3>
                <ol className="space-y-2">
                  {selectedRecipe.instructions.map((instruction, idx) => (
                    <li key={idx} className="flex items-start">
                      <span className="bg-primary text-white rounded-full w-6 h-6 flex items-center justify-center text-sm mr-3 flex-shrink-0">
                        {idx + 1}
                      </span>
                      <span className="text-gray-700 pt-0.5">{instruction}</span>
                    </li>
                  ))}
                </ol>
              </div>

              {selectedRecipe.notes && (
                <div className="bg-yellow-50 border border-yellow-200 rounded-md p-3">
                  <p className="text-sm text-yellow-800">
                    <span className="font-semibold">Note:</span> {selectedRecipe.notes}
                  </p>
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Daily Meal Plan Suggestion */}
      <div className="bg-gradient-to-r from-primary to-blue-500 rounded-lg p-6 text-white">
        <h2 className="text-xl font-bold mb-3">Sample Daily Plan</h2>
        <div className="space-y-2">
          <p><span className="font-semibold">Morning:</span> Colon Support Tea + Anti-Cancer Smoothie</p>
          <p><span className="font-semibold">Lunch:</span> Garlic Cauliflower Rice Bowl</p>
          <p><span className="font-semibold">Afternoon:</span> Green Tea (2-3 cups)</p>
          <p><span className="font-semibold">Dinner:</span> Brussels Sprouts with Turmeric OR Kale Ginger Stir-Fry</p>
          <p><span className="font-semibold">Evening:</span> Colon Support Tea</p>
        </div>
        <p className="mt-4 text-sm opacity-90">
          This hits all your protocol foods. Mix and match recipes to keep it interesting!
        </p>
      </div>
    </div>
  );
}
