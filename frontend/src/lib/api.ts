const API_URL = 'http://localhost:8000/api';

export const api = {
  // Status/Dashboard
  async getStatus() {
    const res = await fetch(`${API_URL}/status/`);
    if (!res.ok) throw new Error('Failed to fetch status');
    return res.json();
  },

  // Protocol
  async getTodayProtocol() {
    const res = await fetch(`${API_URL}/protocol/today`);
    if (!res.ok) throw new Error('Failed to fetch protocol');
    return res.json();
  },

  async generateProtocol(weight?: number) {
    const res = await fetch(`${API_URL}/protocol/generate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user_id: 1, weight_lbs: weight }),
    });
    if (!res.ok) throw new Error('Failed to generate protocol');
    return res.json();
  },

  // Weight
  async getWeightHistory() {
    const res = await fetch(`${API_URL}/weight/history`);
    if (!res.ok) throw new Error('Failed to fetch weight history');
    return res.json();
  },

  async recordWeight(weight: number, notes?: string) {
    const res = await fetch(`${API_URL}/weight/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        user_id: 1,
        weight_lbs: weight,
        followed_protocol: true,
        notes: notes || '',
      }),
    });
    if (!res.ok) throw new Error('Failed to record weight');
    return res.json();
  },

  // Compliance
  async getComplianceHistory(days: number = 30) {
    const res = await fetch(`${API_URL}/compliance/history?user_id=1&days=${days}`);
    if (!res.ok) throw new Error('Failed to fetch compliance');
    return res.json();
  },

  async getComplianceStats() {
    const res = await fetch(`${API_URL}/compliance/stats?user_id=1`);
    if (!res.ok) throw new Error('Failed to fetch stats');
    return res.json();
  },

  // Foods
  async getAllFoods() {
    const res = await fetch(`${API_URL}/foods/`);
    if (!res.ok) throw new Error('Failed to fetch foods');
    return res.json();
  },
};
