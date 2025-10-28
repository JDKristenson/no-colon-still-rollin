// Use relative URL - Vite proxy will forward to backend
const API_URL = '/api';

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

  // Library
  async searchPubMed(query: string, maxResults: number = 20) {
    const res = await fetch(`${API_URL}/library/search?query=${encodeURIComponent(query)}&max_results=${maxResults}`);
    if (!res.ok) throw new Error('Failed to search PubMed');
    return res.json();
  },

  async getSavedStudies(foodName?: string) {
    const url = foodName
      ? `${API_URL}/library/saved?food_name=${encodeURIComponent(foodName)}`
      : `${API_URL}/library/saved`;
    const res = await fetch(url);
    if (!res.ok) throw new Error('Failed to fetch saved studies');
    return res.json();
  },

  async saveStudy(study: any) {
    const res = await fetch(`${API_URL}/library/save`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(study),
    });
    if (!res.ok) throw new Error('Failed to save study');
    return res.json();
  },

  async deleteStudy(pubmedId: string) {
    const res = await fetch(`${API_URL}/library/${pubmedId}`, {
      method: 'DELETE',
    });
    if (!res.ok) throw new Error('Failed to delete study');
    return res.json();
  },

  async getLibraryStats() {
    const res = await fetch(`${API_URL}/library/stats`);
    if (!res.ok) throw new Error('Failed to fetch library stats');
    return res.json();
  },
};
