import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '../lib/api';
import { useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

interface WeightEntry {
  date: string;
  weight_lbs: number;
  followed_protocol: boolean;
  notes?: string;
}

export default function Weight() {
  const queryClient = useQueryClient();
  const [weight, setWeight] = useState('');
  const [notes, setNotes] = useState('');
  const [followedProtocol, setFollowedProtocol] = useState(true);

  const { data: weightHistory } = useQuery<WeightEntry[]>({
    queryKey: ['weight-history'],
    queryFn: api.getWeightHistory,
  });

  const recordMutation = useMutation({
    mutationFn: ({ weight, notes }: { weight: number; notes?: string }) =>
      api.recordWeight(weight, notes),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['weight-history'] });
      queryClient.invalidateQueries({ queryKey: ['status'] });
      queryClient.invalidateQueries({ queryKey: ['compliance-stats'] });
      setWeight('');
      setNotes('');
      setFollowedProtocol(true);
    },
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const weightNum = parseFloat(weight);
    if (weightNum && weightNum > 0) {
      recordMutation.mutate({ weight: weightNum, notes });
    }
  };

  // Calculate stats
  const sortedHistory = weightHistory
    ? [...weightHistory].sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime())
    : [];

  const startingWeight = sortedHistory[0]?.weight_lbs;
  const currentWeight = sortedHistory[sortedHistory.length - 1]?.weight_lbs;
  const weightChange = currentWeight && startingWeight ? currentWeight - startingWeight : 0;
  const weightChangePercent = startingWeight ? ((weightChange / startingWeight) * 100) : 0;

  const handleExport = (format: 'excel' | 'csv') => {
    if (format === 'excel') {
      window.open('http://localhost:8000/api/exports/medical-report/excel?user_id=1', '_blank');
    } else {
      window.open('http://localhost:8000/api/exports/medical-report/csv?user_id=1&report_type=weight', '_blank');
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-start">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Weight Tracker</h1>
          <p className="mt-1 text-sm text-gray-500">Monitor your progress over time</p>
        </div>
        <div className="flex gap-2">
          <button
            onClick={() => handleExport('csv')}
            className="px-4 py-2 bg-secondary text-white rounded-md hover:bg-green-600 transition-colors text-sm"
          >
            Download CSV
          </button>
          <button
            onClick={() => handleExport('excel')}
            className="px-4 py-2 bg-primary text-white rounded-md hover:bg-blue-700 transition-colors text-sm"
          >
            Download Full Report
          </button>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-white shadow rounded-lg p-5">
          <h3 className="text-sm font-medium text-gray-500">Starting Weight</h3>
          <p className="text-2xl font-bold text-gray-900 mt-1">
            {startingWeight ? `${startingWeight.toFixed(1)} lbs` : 'N/A'}
          </p>
          {sortedHistory[0] && (
            <p className="text-xs text-gray-500 mt-1">
              {new Date(sortedHistory[0].date).toLocaleDateString()}
            </p>
          )}
        </div>

        <div className="bg-white shadow rounded-lg p-5">
          <h3 className="text-sm font-medium text-gray-500">Current Weight</h3>
          <p className="text-2xl font-bold text-primary mt-1">
            {currentWeight ? `${currentWeight.toFixed(1)} lbs` : 'N/A'}
          </p>
          {sortedHistory[sortedHistory.length - 1] && (
            <p className="text-xs text-gray-500 mt-1">
              {new Date(sortedHistory[sortedHistory.length - 1].date).toLocaleDateString()}
            </p>
          )}
        </div>

        <div className="bg-white shadow rounded-lg p-5">
          <h3 className="text-sm font-medium text-gray-500">Total Change</h3>
          <p className={`text-2xl font-bold mt-1 ${weightChange < 0 ? 'text-secondary' : weightChange > 0 ? 'text-orange-500' : 'text-gray-900'}`}>
            {weightChange !== 0 ? (
              <>
                {weightChange > 0 ? '+' : ''}{weightChange.toFixed(1)} lbs
              </>
            ) : 'N/A'}
          </p>
          {weightChangePercent !== 0 && (
            <p className={`text-xs mt-1 ${weightChange < 0 ? 'text-secondary' : 'text-orange-500'}`}>
              {weightChange > 0 ? '+' : ''}{weightChangePercent.toFixed(1)}%
            </p>
          )}
        </div>
      </div>

      {/* Record Weight Form */}
      <div className="bg-white shadow rounded-lg p-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Record New Weight</h2>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid md:grid-cols-2 gap-4">
            <div>
              <label htmlFor="weight" className="block text-sm font-medium text-gray-700 mb-1">
                Weight (lbs) *
              </label>
              <input
                type="number"
                id="weight"
                step="0.1"
                value={weight}
                onChange={(e) => setWeight(e.target.value)}
                placeholder="175.5"
                required
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-primary focus:border-primary"
              />
            </div>

            <div className="flex items-end">
              <label className="flex items-center cursor-pointer">
                <input
                  type="checkbox"
                  checked={followedProtocol}
                  onChange={(e) => setFollowedProtocol(e.target.checked)}
                  className="h-5 w-5 text-secondary border-gray-300 rounded focus:ring-secondary"
                />
                <span className="ml-2 text-sm text-gray-700">
                  Followed protocol today
                </span>
              </label>
            </div>
          </div>

          <div>
            <label htmlFor="weight-notes" className="block text-sm font-medium text-gray-700 mb-1">
              Notes (optional)
            </label>
            <textarea
              id="weight-notes"
              rows={2}
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
              placeholder="How are you feeling? Any observations..."
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-primary focus:border-primary"
            />
          </div>

          <button
            type="submit"
            disabled={recordMutation.isPending}
            className="w-full bg-primary text-white py-3 rounded-md hover:bg-primary/90 font-medium disabled:opacity-50 transition-colors"
          >
            {recordMutation.isPending ? 'Recording...' : 'Record Weight'}
          </button>

          {recordMutation.isSuccess && (
            <div className="bg-green-50 border border-green-200 rounded-md p-3">
              <p className="text-sm text-green-800 flex items-center">
                <svg className="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                Weight recorded successfully!
              </p>
            </div>
          )}

          {recordMutation.isError && (
            <div className="bg-red-50 border border-red-200 rounded-md p-3">
              <p className="text-sm text-red-800">
                Failed to record weight. Please try again.
              </p>
            </div>
          )}
        </form>
      </div>

      {/* Weight Chart */}
      {weightHistory && weightHistory.length > 0 && (
        <div className="bg-white shadow rounded-lg p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Weight Trend</h2>
          <ResponsiveContainer width="100%" height={400}>
            <LineChart data={sortedHistory}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis
                dataKey="date"
                tick={{ fontSize: 12 }}
                tickFormatter={(value) => new Date(value).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
              />
              <YAxis
                domain={['dataMin - 2', 'dataMax + 2']}
                tick={{ fontSize: 12 }}
                label={{ value: 'Weight (lbs)', angle: -90, position: 'insideLeft' }}
              />
              <Tooltip
                labelFormatter={(value) => new Date(value).toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric' })}
                formatter={(value: number) => [`${value.toFixed(1)} lbs`, 'Weight']}
              />
              <Line
                type="monotone"
                dataKey="weight_lbs"
                stroke="#0066CC"
                strokeWidth={2}
                dot={{ fill: '#0066CC', r: 4 }}
                activeDot={{ r: 6 }}
                name="Weight"
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}

      {/* Weight History Table */}
      {weightHistory && weightHistory.length > 0 && (
        <div className="bg-white shadow rounded-lg p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Recent Entries</h2>
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Date
                  </th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Weight
                  </th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Change
                  </th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Protocol
                  </th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Notes
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {[...sortedHistory].reverse().slice(0, 10).map((entry, idx, arr) => {
                  const prevEntry = arr[idx + 1];
                  const change = prevEntry ? entry.weight_lbs - prevEntry.weight_lbs : 0;

                  return (
                    <tr key={entry.date}>
                      <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-900">
                        {new Date(entry.date).toLocaleDateString()}
                      </td>
                      <td className="px-4 py-3 whitespace-nowrap text-sm font-medium text-gray-900">
                        {entry.weight_lbs.toFixed(1)} lbs
                      </td>
                      <td className="px-4 py-3 whitespace-nowrap text-sm">
                        {change !== 0 && (
                          <span className={change < 0 ? 'text-secondary' : 'text-orange-500'}>
                            {change > 0 ? '+' : ''}{change.toFixed(1)}
                          </span>
                        )}
                      </td>
                      <td className="px-4 py-3 whitespace-nowrap text-sm">
                        {entry.followed_protocol ? (
                          <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">
                            Yes
                          </span>
                        ) : (
                          <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-800">
                            No
                          </span>
                        )}
                      </td>
                      <td className="px-4 py-3 text-sm text-gray-500">
                        {entry.notes || '-'}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}
