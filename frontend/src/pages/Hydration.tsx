import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';

const API_URL = '/api';

interface HydrationData {
  date: string;
  total_oz: number;
  goal_oz: number;
  progress_percent: number;
  remaining_oz: number;
  logs: Array<{
    id: number;
    time: string;
    amount_oz: number;
  }>;
}

export default function Hydration() {
  const queryClient = useQueryClient();
  const [showGoalInput, setShowGoalInput] = useState(false);
  const [newGoal, setNewGoal] = useState('64');

  // Fetch today's hydration data
  const { data, isLoading } = useQuery<HydrationData>({
    queryKey: ['hydration-today'],
    queryFn: async () => {
      const res = await fetch(`${API_URL}/hydration/today?user_id=1`);
      return res.json();
    },
    refetchInterval: 5000, // Refresh every 5 seconds
  });

  // Log water intake
  const logWaterMutation = useMutation({
    mutationFn: async (amount_oz: number) => {
      const res = await fetch(`${API_URL}/hydration/log`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: 1, amount_oz }),
      });
      return res.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['hydration-today'] });
    },
  });

  // Update goal
  const updateGoalMutation = useMutation({
    mutationFn: async (goal_oz: number) => {
      const res = await fetch(`${API_URL}/hydration/goal`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: 1, daily_goal_oz: goal_oz }),
      });
      return res.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['hydration-today'] });
      setShowGoalInput(false);
    },
  });

  const handleLogCup = () => {
    logWaterMutation.mutate(8);
  };

  const handleUpdateGoal = () => {
    const goal = parseFloat(newGoal);
    if (goal > 0 && goal <= 200) {
      updateGoalMutation.mutate(goal);
    }
  };

  if (isLoading) {
    return <div className="p-8">Loading...</div>;
  }

  const progress = data?.progress_percent || 0;
  const cupsNeeded = Math.ceil((data?.remaining_oz || 0) / 8);

  return (
    <div className="max-w-4xl mx-auto p-6">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">💧 Hydration Tracker</h1>
        <p className="text-gray-600 mt-2">Stay hydrated to support your healing!</p>
      </div>

      {/* Progress Card */}
      <div className="bg-white rounded-lg shadow-md p-6 mb-6">
        <div className="flex justify-between items-center mb-4">
          <div>
            <h2 className="text-2xl font-bold text-primary">
              {data?.total_oz || 0} oz
            </h2>
            <p className="text-sm text-gray-600">of {data?.goal_oz || 64} oz goal</p>
          </div>
          <button
            onClick={() => setShowGoalInput(!showGoalInput)}
            className="text-sm text-primary hover:underline"
          >
            Change Goal
          </button>
        </div>

        {showGoalInput && (
          <div className="mb-4 p-3 bg-gray-50 rounded">
            <label className="block text-sm font-medium mb-2">
              Daily Goal (oz)
            </label>
            <div className="flex gap-2">
              <input
                type="number"
                value={newGoal}
                onChange={(e) => setNewGoal(e.target.value)}
                className="border rounded px-3 py-2 w-24"
                min="1"
                max="200"
              />
              <button
                onClick={handleUpdateGoal}
                className="bg-primary text-white px-4 py-2 rounded hover:bg-blue-700"
              >
                Update
              </button>
              <button
                onClick={() => setShowGoalInput(false)}
                className="px-4 py-2 rounded border hover:bg-gray-100"
              >
                Cancel
              </button>
            </div>
          </div>
        )}

        {/* Progress Bar */}
        <div className="relative h-8 bg-gray-200 rounded-full overflow-hidden">
          <div
            className="absolute h-full bg-gradient-to-r from-blue-400 to-blue-600 transition-all duration-500"
            style={{ width: `${Math.min(progress, 100)}%` }}
          />
          <div className="absolute inset-0 flex items-center justify-center text-sm font-medium text-gray-700">
            {progress.toFixed(0)}%
          </div>
        </div>

        {progress >= 100 ? (
          <p className="text-center mt-4 text-secondary font-medium">
            🎉 Goal reached! Great job staying hydrated!
          </p>
        ) : (
          <p className="text-center mt-4 text-gray-600">
            {cupsNeeded} more cup{cupsNeeded !== 1 ? 's' : ''} to reach your goal
          </p>
        )}
      </div>

      {/* Add Water Button */}
      <div className="bg-white rounded-lg shadow-md p-6 mb-6">
        <h3 className="text-lg font-semibold mb-4">Log Water Intake</h3>

        <button
          onClick={handleLogCup}
          disabled={logWaterMutation.isPending}
          className="group w-full max-w-xs mx-auto block"
        >
          <div className="text-center p-8 bg-gradient-to-b from-blue-100 to-blue-200 rounded-2xl border-4 border-blue-300 hover:from-blue-200 hover:to-blue-300 hover:border-blue-400 transition-all transform hover:scale-105 active:scale-95">
            <div className="text-6xl mb-2">💧</div>
            <div className="text-2xl font-bold text-blue-700">+8 oz</div>
            <div className="text-sm text-gray-600 mt-1">Click to log 1 cup</div>
          </div>
        </button>

        <div className="mt-4 grid grid-cols-3 gap-2 max-w-xs mx-auto">
          <button
            onClick={() => logWaterMutation.mutate(4)}
            className="px-3 py-2 bg-blue-50 hover:bg-blue-100 rounded text-sm border border-blue-200"
          >
            +4 oz
          </button>
          <button
            onClick={() => logWaterMutation.mutate(8)}
            className="px-3 py-2 bg-blue-50 hover:bg-blue-100 rounded text-sm border border-blue-200"
          >
            +8 oz
          </button>
          <button
            onClick={() => logWaterMutation.mutate(16)}
            className="px-3 py-2 bg-blue-50 hover:bg-blue-100 rounded text-sm border border-blue-200"
          >
            +16 oz
          </button>
        </div>
      </div>

      {/* Today's Log */}
      {data?.logs && data.logs.length > 0 && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-semibold mb-4">Today's Log</h3>
          <div className="space-y-2">
            {data.logs.map((log) => (
              <div
                key={log.id}
                className="flex justify-between items-center p-3 bg-gray-50 rounded"
              >
                <span className="text-gray-700">
                  {new Date(`2000-01-01T${log.time}`).toLocaleTimeString([], {
                    hour: 'numeric',
                    minute: '2-digit',
                  })}
                </span>
                <span className="font-medium text-blue-600">
                  {log.amount_oz} oz
                </span>
              </div>
            ))}
          </div>
          <div className="mt-4 pt-4 border-t">
            <div className="flex justify-between font-semibold">
              <span>Total Today:</span>
              <span className="text-primary">{data.total_oz} oz</span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
