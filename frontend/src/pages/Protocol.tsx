import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '../lib/api';
import { useState } from 'react';

interface Food {
  name: string;
  amount_grams: number;
  servings_per_day: number;
  grams_per_serving: number;
  timing: string;
  timing_notes: string;
  preparation: string;
  preparation_notes: string;
  net_carbs: number;
  protein: number;
  fat: number;
  reason: string;
  mechanisms: string[];
  safety_notes: string;
}

interface Protocol {
  date: string;
  user_id: number;
  weight_lbs: number;
  foods: Food[];
  total_net_carbs: number;
  total_protein: number;
  total_fat: number;
  total_calories: number;
  keto_compatible: boolean;
  keto_score: number;
}

export default function Protocol() {
  const queryClient = useQueryClient();
  const [isGenerating, setIsGenerating] = useState(false);

  const { data: protocol, isLoading, error } = useQuery<Protocol>({
    queryKey: ['protocol-today'],
    queryFn: api.getTodayProtocol,
    retry: false,
  });

  const generateMutation = useMutation({
    mutationFn: api.generateProtocol,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['protocol-today'] });
      setIsGenerating(false);
    },
  });

  const handleGenerate = () => {
    setIsGenerating(true);
    generateMutation.mutate(undefined);
  };

  if (isLoading) {
    return <div className="text-center py-12">Loading protocol...</div>;
  }

  if (error || !protocol) {
    return (
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Daily Protocol</h1>
          <p className="mt-1 text-sm text-gray-500">No protocol found for today</p>
        </div>
        <div className="bg-white shadow rounded-lg p-6 text-center">
          <p className="text-gray-600 mb-4">Generate your personalized anti-cancer food protocol for today.</p>
          <button
            onClick={handleGenerate}
            disabled={isGenerating}
            className="bg-primary text-white px-6 py-3 rounded-md hover:bg-primary/90 disabled:opacity-50"
          >
            {isGenerating ? 'Generating...' : 'Generate Today\'s Protocol'}
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-start">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Daily Protocol</h1>
          <p className="mt-1 text-sm text-gray-500">
            {new Date(protocol.date).toLocaleDateString('en-US', {
              weekday: 'long',
              year: 'numeric',
              month: 'long',
              day: 'numeric'
            })}
          </p>
        </div>
        <button
          onClick={handleGenerate}
          disabled={isGenerating}
          className="bg-secondary text-white px-4 py-2 rounded-md hover:bg-secondary/90 text-sm disabled:opacity-50"
        >
          {isGenerating ? 'Regenerating...' : 'Regenerate Protocol'}
        </button>
      </div>

      {/* Daily Summary */}
      <div className="bg-white shadow rounded-lg p-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Daily Summary</h2>
        <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
          <div>
            <p className="text-sm text-gray-500">Weight</p>
            <p className="text-xl font-semibold text-gray-900">{protocol.weight_lbs} lbs</p>
          </div>
          <div>
            <p className="text-sm text-gray-500">Net Carbs</p>
            <p className="text-xl font-semibold text-gray-900">{protocol.total_net_carbs.toFixed(1)}g</p>
          </div>
          <div>
            <p className="text-sm text-gray-500">Protein</p>
            <p className="text-xl font-semibold text-gray-900">{protocol.total_protein.toFixed(1)}g</p>
          </div>
          <div>
            <p className="text-sm text-gray-500">Fat</p>
            <p className="text-xl font-semibold text-gray-900">{protocol.total_fat.toFixed(1)}g</p>
          </div>
          <div>
            <p className="text-sm text-gray-500">Keto Score</p>
            <p className={`text-xl font-semibold ${protocol.keto_compatible ? 'text-keto' : 'text-orange-500'}`}>
              {(protocol.keto_score * 100).toFixed(0)}%
            </p>
          </div>
        </div>
      </div>

      {/* Food Cards */}
      <div className="space-y-4">
        <h2 className="text-lg font-semibold text-gray-900">Your Foods for Today</h2>
        {protocol.foods.map((food, idx) => (
          <div key={idx} className="bg-white shadow rounded-lg p-6">
            <div className="flex justify-between items-start mb-4">
              <div>
                <h3 className="text-xl font-bold text-primary">{food.name}</h3>
                <p className="text-sm text-gray-500 mt-1">
                  {food.servings_per_day} {food.servings_per_day === 1 ? 'serving' : 'servings'} per day • {food.grams_per_serving.toFixed(0)}g each
                </p>
              </div>
              <div className="text-right">
                <p className="text-2xl font-bold text-gray-900">{food.amount_grams.toFixed(0)}g</p>
                <p className="text-xs text-gray-500">total daily</p>
              </div>
            </div>

            <div className="grid md:grid-cols-2 gap-6">
              <div className="space-y-4">
                {/* Timing */}
                <div>
                  <div className="flex items-center mb-2">
                    <svg className="h-5 w-5 text-secondary mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    <h4 className="font-semibold text-gray-900">Timing</h4>
                  </div>
                  <p className="text-gray-700">{food.timing}</p>
                  {food.timing_notes && (
                    <p className="text-sm text-gray-600 mt-1">{food.timing_notes}</p>
                  )}
                </div>

                {/* Preparation */}
                <div>
                  <div className="flex items-center mb-2">
                    <svg className="h-5 w-5 text-orange-500 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                    </svg>
                    <h4 className="font-semibold text-gray-900">Preparation</h4>
                  </div>
                  <p className="text-gray-700">{food.preparation}</p>
                  {food.preparation_notes && (
                    <p className="text-sm text-gray-600 mt-1">{food.preparation_notes}</p>
                  )}
                </div>

                {/* Macros */}
                <div>
                  <h4 className="font-semibold text-gray-900 mb-2">Nutrition per Serving</h4>
                  <div className="flex space-x-4 text-sm">
                    <div>
                      <span className="text-gray-500">Carbs:</span>
                      <span className="ml-1 font-medium text-gray-900">{(food.net_carbs / food.servings_per_day).toFixed(1)}g</span>
                    </div>
                    <div>
                      <span className="text-gray-500">Protein:</span>
                      <span className="ml-1 font-medium text-gray-900">{(food.protein / food.servings_per_day).toFixed(1)}g</span>
                    </div>
                    <div>
                      <span className="text-gray-500">Fat:</span>
                      <span className="ml-1 font-medium text-gray-900">{(food.fat / food.servings_per_day).toFixed(1)}g</span>
                    </div>
                  </div>
                </div>
              </div>

              <div className="space-y-4">
                {/* Why This Food */}
                <div>
                  <div className="flex items-center mb-2">
                    <svg className="h-5 w-5 text-primary mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    <h4 className="font-semibold text-gray-900">Why This Food?</h4>
                  </div>
                  <p className="text-gray-700">{food.reason}</p>
                </div>

                {/* Mechanisms */}
                {food.mechanisms && food.mechanisms.length > 0 && (
                  <div>
                    <h4 className="font-semibold text-gray-900 mb-2">Active Mechanisms</h4>
                    <ul className="list-disc list-inside space-y-1">
                      {food.mechanisms.map((mechanism, i) => (
                        <li key={i} className="text-sm text-gray-700">{mechanism}</li>
                      ))}
                    </ul>
                  </div>
                )}

                {/* Safety Notes */}
                {food.safety_notes && (
                  <div className="bg-blue-50 border border-blue-200 rounded-md p-3">
                    <div className="flex items-start">
                      <svg className="h-5 w-5 text-blue-600 mr-2 flex-shrink-0 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                      <div>
                        <h4 className="font-semibold text-blue-900 text-sm mb-1">Safety Notes</h4>
                        <p className="text-sm text-blue-800">{food.safety_notes}</p>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Research Note */}
      <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
        <p className="text-sm text-gray-600">
          <span className="font-semibold">Evidence-Based Protocol:</span> All foods and dosages are calculated based on FDA-standard measurements and peer-reviewed research.
          Consult with your healthcare team before making dietary changes.
        </p>
      </div>
    </div>
  );
}
