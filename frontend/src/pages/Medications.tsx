import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';

const API_URL = 'http://localhost:8000/api';

interface Medication {
  id: number;
  name: string;
  generic_name: string | null;
  dosage: string;
  frequency: string;
  active: boolean;
}

interface MedicationLogEntry {
  id: number;
  medication_id: number;
  medication_name: string;
  date: string;
  time: string;
  dosage: string;
  taken: boolean;
  notes: string;
}

export default function Medications() {
  const queryClient = useQueryClient();
  const [showAddForm, setShowAddForm] = useState(false);
  const [newMed, setNewMed] = useState({
    name: '',
    generic_name: '',
    dosage: '',
    frequency: ''
  });

  // Fetch medications list
  const { data: medications } = useQuery<Medication[]>({
    queryKey: ['medications'],
    queryFn: async () => {
      const res = await fetch(`${API_URL}/medications/list?user_id=1`);
      return res.json();
    },
  });

  // Fetch today's log
  const { data: todayLog } = useQuery<MedicationLogEntry[]>({
    queryKey: ['medications-today'],
    queryFn: async () => {
      const res = await fetch(`${API_URL}/medications/log/today?user_id=1`);
      return res.json();
    },
    refetchInterval: 10000, // Refresh every 10 seconds
  });

  // Add medication mutation
  const addMedMutation = useMutation({
    mutationFn: async (med: typeof newMed) => {
      const res = await fetch(`${API_URL}/medications/add`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: 1, ...med }),
      });
      return res.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['medications'] });
      setShowAddForm(false);
      setNewMed({ name: '', generic_name: '', dosage: '', frequency: '' });
    },
  });

  // Log medication dose mutation
  const logMedMutation = useMutation({
    mutationFn: async ({ medication_id, dosage }: { medication_id: number; dosage?: string }) => {
      const res = await fetch(`${API_URL}/medications/log`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_id: 1,
          medication_id,
          dosage,
          taken: true,
        }),
      });
      return res.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['medications-today'] });
    },
  });

  const handleAddMedication = () => {
    if (newMed.name && newMed.dosage && newMed.frequency) {
      addMedMutation.mutate(newMed);
    }
  };

  const handleLogMed = (med: Medication) => {
    logMedMutation.mutate({ medication_id: med.id, dosage: med.dosage });
  };

  // Check if medication was taken today
  const wasTakenToday = (medId: number) => {
    return todayLog?.some(log => log.medication_id === medId && log.taken) || false;
  };

  return (
    <div className="max-w-4xl mx-auto p-6">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">💊 Medications</h1>
        <p className="text-gray-600 mt-2">Track your medication adherence</p>
      </div>

      {/* Add Medication Section */}
      <div className="bg-white rounded-lg shadow-md p-6 mb-6">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-semibold">My Medications</h2>
          <button
            onClick={() => setShowAddForm(!showAddForm)}
            className="bg-primary text-white px-4 py-2 rounded hover:bg-blue-700"
          >
            {showAddForm ? 'Cancel' : '+ Add Medication'}
          </button>
        </div>

        {showAddForm && (
          <div className="mb-6 p-4 bg-gray-50 rounded">
            <h3 className="font-medium mb-3">Add New Medication</h3>
            <div className="space-y-3">
              <div>
                <label className="block text-sm font-medium mb-1">
                  Brand/Trade Name *
                </label>
                <input
                  type="text"
                  value={newMed.name}
                  onChange={(e) => setNewMed({ ...newMed, name: e.target.value })}
                  className="w-full border rounded px-3 py-2"
                  placeholder="e.g., Tylenol"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">
                  Generic Name (optional)
                </label>
                <input
                  type="text"
                  value={newMed.generic_name}
                  onChange={(e) => setNewMed({ ...newMed, generic_name: e.target.value })}
                  className="w-full border rounded px-3 py-2"
                  placeholder="e.g., acetaminophen"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">
                  Dosage *
                </label>
                <input
                  type="text"
                  value={newMed.dosage}
                  onChange={(e) => setNewMed({ ...newMed, dosage: e.target.value })}
                  className="w-full border rounded px-3 py-2"
                  placeholder="e.g., 500mg"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">
                  Frequency *
                </label>
                <input
                  type="text"
                  value={newMed.frequency}
                  onChange={(e) => setNewMed({ ...newMed, frequency: e.target.value })}
                  className="w-full border rounded px-3 py-2"
                  placeholder="e.g., 3x daily with meals"
                />
              </div>
              <button
                onClick={handleAddMedication}
                disabled={!newMed.name || !newMed.dosage || !newMed.frequency}
                className="bg-secondary text-white px-4 py-2 rounded hover:bg-green-700 disabled:bg-gray-300 disabled:cursor-not-allowed"
              >
                Save Medication
              </button>
            </div>
          </div>
        )}

        {/* Medications List */}
        {medications && medications.length > 0 ? (
          <div className="space-y-3">
            {medications.map((med) => {
              const takenToday = wasTakenToday(med.id);
              return (
                <div
                  key={med.id}
                  className={`flex justify-between items-center p-4 rounded border-2 ${
                    takenToday
                      ? 'bg-green-50 border-green-300'
                      : 'bg-white border-gray-200'
                  }`}
                >
                  <div className="flex-1">
                    <div className="flex items-center gap-2">
                      <h3 className="font-semibold text-lg">{med.name}</h3>
                      {takenToday && (
                        <span className="text-green-600 text-xl">✓</span>
                      )}
                    </div>
                    {med.generic_name && (
                      <p className="text-sm text-gray-500">({med.generic_name})</p>
                    )}
                    <p className="text-gray-700 mt-1">
                      <span className="font-medium">{med.dosage}</span> • {med.frequency}
                    </p>
                  </div>
                  <button
                    onClick={() => handleLogMed(med)}
                    disabled={logMedMutation.isPending || takenToday}
                    className={`px-6 py-2 rounded font-medium transition-all ${
                      takenToday
                        ? 'bg-gray-200 text-gray-500 cursor-not-allowed'
                        : 'bg-primary text-white hover:bg-blue-700 hover:scale-105'
                    }`}
                  >
                    {takenToday ? 'Logged Today' : 'Log Dose'}
                  </button>
                </div>
              );
            })}
          </div>
        ) : (
          <p className="text-gray-500 text-center py-8">
            No medications added yet. Click "+ Add Medication" to get started.
          </p>
        )}
      </div>

      {/* Today's Log */}
      {todayLog && todayLog.length > 0 && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-semibold mb-4">Today's Adherence Log</h3>
          <div className="space-y-2">
            {todayLog.map((log) => (
              <div
                key={log.id}
                className="flex justify-between items-center p-3 bg-gray-50 rounded"
              >
                <div>
                  <span className="font-medium text-gray-900">{log.medication_name}</span>
                  <span className="text-gray-500 ml-2">({log.dosage})</span>
                </div>
                <span className="text-gray-600">
                  {new Date(`2000-01-01T${log.time}`).toLocaleTimeString([], {
                    hour: 'numeric',
                    minute: '2-digit',
                  })}
                </span>
              </div>
            ))}
          </div>
          <div className="mt-4 pt-4 border-t">
            <div className="flex justify-between items-center">
              <span className="font-semibold">Adherence Rate:</span>
              <span className="text-primary font-bold text-lg">
                {medications && medications.length > 0
                  ? `${Math.round((todayLog.length / medications.length) * 100)}%`
                  : '0%'}
              </span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
