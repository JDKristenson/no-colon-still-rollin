import { useQuery } from '@tanstack/react-query';
import { api } from '../lib/api';
import { useState } from 'react';

interface Food {
  name: string;
  servings_per_day: number;
  grams_per_serving: number;
}

export default function Compliance() {
  const [checkedFoods, setCheckedFoods] = useState<Record<string, boolean>>({});
  const [notes, setNotes] = useState('');

  const { data: protocol } = useQuery({
    queryKey: ['protocol-today'],
    queryFn: api.getTodayProtocol,
    retry: false,
  });

  const { data: stats } = useQuery({
    queryKey: ['compliance-stats'],
    queryFn: api.getComplianceStats,
  });

  const handleFoodCheck = (foodName: string) => {
    setCheckedFoods(prev => ({
      ...prev,
      [foodName]: !prev[foodName]
    }));
  };

  const allFoodsChecked = protocol?.foods.every((food: Food) => checkedFoods[food.name]) || false;
  const checkedCount = Object.values(checkedFoods).filter(Boolean).length;
  const totalCount = protocol?.foods.length || 0;
  const completionPercent = totalCount > 0 ? Math.round((checkedCount / totalCount) * 100) : 0;

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Daily Check-In</h1>
        <p className="mt-1 text-sm text-gray-500">Track your progress, one food at a time</p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-white shadow rounded-lg p-5">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <svg className="h-8 w-8 text-orange-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 18.657A8 8 0 016.343 7.343S7 9 9 10c0-2 .5-5 2.986-7C14 5 16.09 5.777 17.656 7.343A7.975 7.975 0 0120 13a7.975 7.975 0 01-2.343 5.657z" />
              </svg>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">Current Streak</p>
              <p className="text-2xl font-bold text-gray-900">{stats?.current_streak || 0} days</p>
            </div>
          </div>
        </div>

        <div className="bg-white shadow rounded-lg p-5">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <svg className="h-8 w-8 text-secondary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">7-Day Adherence</p>
              <p className="text-2xl font-bold text-gray-900">{stats?.average_adherence || 0}%</p>
            </div>
          </div>
        </div>

        <div className="bg-white shadow rounded-lg p-5">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <svg className="h-8 w-8 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">Total Days</p>
              <p className="text-2xl font-bold text-gray-900">{stats?.total_days || 0}</p>
            </div>
          </div>
        </div>
      </div>

      {!protocol ? (
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6 text-center">
          <svg className="h-12 w-12 text-yellow-400 mx-auto mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
          <h3 className="text-lg font-semibold text-yellow-900 mb-2">No Protocol for Today</h3>
          <p className="text-yellow-800 mb-4">Generate your protocol first to start tracking.</p>
          <a
            href="/protocol"
            className="inline-block bg-primary text-white px-6 py-2 rounded-md hover:bg-primary/90"
          >
            Go to Protocol
          </a>
        </div>
      ) : (
        <>
          {/* Progress Bar */}
          <div className="bg-white shadow rounded-lg p-6">
            <div className="flex justify-between items-center mb-3">
              <h2 className="text-lg font-semibold text-gray-900">Today's Progress</h2>
              <span className="text-2xl font-bold text-primary">{completionPercent}%</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-3">
              <div
                className="bg-secondary h-3 rounded-full transition-all duration-300"
                style={{ width: `${completionPercent}%` }}
              />
            </div>
            <p className="text-sm text-gray-600 mt-2">
              {checkedCount} of {totalCount} foods completed
            </p>
          </div>

          {/* Food Checklist */}
          <div className="bg-white shadow rounded-lg p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Today's Foods</h2>
            <div className="space-y-3">
              {protocol.foods.map((food: Food) => (
                <label
                  key={food.name}
                  className="flex items-start p-4 border border-gray-200 rounded-lg hover:bg-gray-50 cursor-pointer transition-colors"
                >
                  <input
                    type="checkbox"
                    checked={checkedFoods[food.name] || false}
                    onChange={() => handleFoodCheck(food.name)}
                    className="mt-1 h-5 w-5 text-secondary border-gray-300 rounded focus:ring-secondary"
                  />
                  <div className="ml-4 flex-1">
                    <div className="flex justify-between items-start">
                      <div>
                        <p className="font-semibold text-gray-900">{food.name}</p>
                        <p className="text-sm text-gray-600">
                          {food.servings_per_day} {food.servings_per_day === 1 ? 'serving' : 'servings'} • {food.grams_per_serving.toFixed(0)}g each
                        </p>
                      </div>
                      {checkedFoods[food.name] && (
                        <svg className="h-6 w-6 text-secondary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                      )}
                    </div>
                  </div>
                </label>
              ))}
            </div>
          </div>

          {/* Notes Section */}
          <div className="bg-white shadow rounded-lg p-6">
            <label htmlFor="notes" className="block text-sm font-medium text-gray-900 mb-2">
              Notes (optional)
            </label>
            <textarea
              id="notes"
              rows={3}
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
              placeholder="How are you feeling? Any observations about the foods or your progress..."
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-primary focus:border-primary"
            />
          </div>

          {/* Motivational Message */}
          {allFoodsChecked ? (
            <div className="bg-gradient-to-r from-secondary to-green-400 rounded-lg p-6 text-white">
              <div className="flex items-center">
                <svg className="h-10 w-10 mr-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <div>
                  <h3 className="text-xl font-bold">Perfect! 🎉</h3>
                  <p className="mt-1">You've checked off all your foods for today. Keep up the amazing work!</p>
                </div>
              </div>
            </div>
          ) : completionPercent > 0 ? (
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
              <p className="text-blue-900">
                <span className="font-semibold">You're making progress!</span> Every step counts. Remember, this journey is about forward momentum, not perfection. 💪
              </p>
            </div>
          ) : (
            <div className="bg-gray-50 border border-gray-200 rounded-lg p-6">
              <p className="text-gray-700">
                <span className="font-semibold">Ready to start?</span> Check off each food as you consume it throughout the day. You've got this! ✨
              </p>
            </div>
          )}

          {/* Save Button Note */}
          <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
            <div className="flex items-start">
              <svg className="h-5 w-5 text-yellow-600 mr-2 flex-shrink-0 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <p className="text-sm text-yellow-800">
                <span className="font-semibold">Coming soon:</span> Auto-save functionality. For now, use this checklist to track your daily progress. Your check-ins will be saved with your weight logs.
              </p>
            </div>
          </div>
        </>
      )}
    </div>
  );
}
