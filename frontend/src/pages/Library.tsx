import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '../lib/api';

export default function Library() {
  const [activeTab, setActiveTab] = useState<'search' | 'saved' | 'calculator'>('search');
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState<any[]>([]);
  const [isSearching, setIsSearching] = useState(false);
  const [selectedStudy, setSelectedStudy] = useState<any>(null);
  const [calculating, setCalculating] = useState(false);
  const [calculatorResult, setCalculatorResult] = useState<any>(null);
  const [doseForm, setDoseForm] = useState({
    study_dose_mg_kg: '',
    study_type: 'mouse',
    compound_name: '',
    food_name: '',
    compound_per_100g_food: '',
    human_weight_kg: '70'
  });

  const queryClient = useQueryClient();

  // Get saved studies
  const { data: savedStudies } = useQuery({
    queryKey: ['saved-studies'],
    queryFn: () => api.getSavedStudies(),
  });

  // Get library stats
  const { data: stats } = useQuery({
    queryKey: ['library-stats'],
    queryFn: api.getLibraryStats,
  });

  // Search mutation
  const handleSearch = async () => {
    if (!searchQuery.trim()) return;
    setIsSearching(true);
    try {
      const results = await api.searchPubMed(searchQuery, 20);
      setSearchResults(results);
    } catch (error) {
      console.error('Search failed:', error);
    } finally {
      setIsSearching(false);
    }
  };

  // Save study mutation
  const saveMutation = useMutation({
    mutationFn: (study: any) => api.saveStudy({
      pubmed_id: study.pubmed_id,
      title: study.title,
      authors: study.authors,
      journal: study.journal,
      year: study.year,
      abstract: study.abstract,
      doi: study.doi,
      url: study.url,
      cancer_type: 'colon',
      food_studied: extractFoodFromQuery(searchQuery),
    }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['saved-studies'] });
      queryClient.invalidateQueries({ queryKey: ['library-stats'] });
      alert('Study saved to your library!');
    },
  });

  // Delete study mutation
  const deleteMutation = useMutation({
    mutationFn: (pubmedId: string) => api.deleteStudy(pubmedId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['saved-studies'] });
      queryClient.invalidateQueries({ queryKey: ['library-stats'] });
    },
  });

  const extractFoodFromQuery = (query: string): string => {
    const foods = ['ginger', 'garlic', 'turmeric', 'broccoli', 'cauliflower', 'kale', 'brussels sprouts', 'green tea'];
    const lowerQuery = query.toLowerCase();
    for (const food of foods) {
      if (lowerQuery.includes(food)) return food;
    }
    return '';
  };

  const handleCalculateDose = async () => {
    if (!doseForm.study_dose_mg_kg || !doseForm.compound_name || !doseForm.food_name || !doseForm.compound_per_100g_food) {
      alert('Please fill in all required fields');
      return;
    }

    setCalculating(true);
    try {
      const response = await fetch('/api/library/dose-calculator', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          study_dose_mg_kg: parseFloat(doseForm.study_dose_mg_kg),
          study_type: doseForm.study_type,
          compound_name: doseForm.compound_name,
          food_name: doseForm.food_name,
          compound_per_100g_food: parseFloat(doseForm.compound_per_100g_food),
          human_weight_kg: parseFloat(doseForm.human_weight_kg)
        })
      });
      const result = await response.json();
      setCalculatorResult(result);
    } catch (error) {
      console.error('Calculation failed:', error);
      alert('Failed to calculate dose');
    } finally {
      setCalculating(false);
    }
  };

  const StudyCard = ({ study, isSaved = false }: { study: any; isSaved?: boolean }) => (
    <div className="bg-white shadow rounded-lg p-6 hover:shadow-lg transition-shadow">
      <div className="flex justify-between items-start">
        <div className="flex-1">
          <h3 className="text-lg font-semibold text-gray-900 mb-2">{study.title}</h3>
          <div className="text-sm text-gray-600 space-y-1">
            {study.authors && <p><span className="font-medium">Authors:</span> {study.authors}</p>}
            {study.journal && <p><span className="font-medium">Journal:</span> {study.journal}</p>}
            {study.year && <p><span className="font-medium">Year:</span> {study.year}</p>}
          </div>
          {study.abstract && (
            <p className="mt-3 text-sm text-gray-700 line-clamp-3">{study.abstract}</p>
          )}
        </div>
        <div className="ml-4 flex flex-col gap-2">
          {!isSaved && !study.saved && (
            <button
              onClick={() => saveMutation.mutate(study)}
              className="px-4 py-2 bg-primary text-white rounded-md hover:bg-blue-700 transition-colors"
              disabled={saveMutation.isPending}
            >
              {saveMutation.isPending ? 'Saving...' : 'Save'}
            </button>
          )}
          {(isSaved || study.saved) && (
            <button
              onClick={() => deleteMutation.mutate(study.pubmed_id)}
              className="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 transition-colors"
              disabled={deleteMutation.isPending}
            >
              Remove
            </button>
          )}
          <button
            onClick={() => setSelectedStudy(study)}
            className="px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300 transition-colors"
          >
            Details
          </button>
          {study.url && (
            <a
              href={study.url}
              target="_blank"
              rel="noopener noreferrer"
              className="px-4 py-2 bg-secondary text-white rounded-md hover:bg-green-600 transition-colors text-center"
            >
              View
            </a>
          )}
        </div>
      </div>
    </div>
  );

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Research Library</h1>
        <p className="mt-1 text-sm text-gray-500">
          Explore the science behind your protocol. Knowledge is power in your fight!
        </p>
      </div>

      {/* Stats Cards */}
      {stats && (
        <div className="grid grid-cols-1 gap-6 sm:grid-cols-3">
          <div className="bg-white overflow-hidden shadow rounded-lg">
            <div className="p-5">
              <div className="text-center">
                <dt className="text-sm font-medium text-gray-500">Total Studies</dt>
                <dd className="text-3xl font-semibold text-primary">{stats.total_studies}</dd>
              </div>
            </div>
          </div>
          <div className="bg-white overflow-hidden shadow rounded-lg">
            <div className="p-5">
              <div className="text-center">
                <dt className="text-sm font-medium text-gray-500">Recent Studies</dt>
                <dd className="text-3xl font-semibold text-secondary">{stats.recent_studies}</dd>
                <p className="text-xs text-gray-500 mt-1">(since 2020)</p>
              </div>
            </div>
          </div>
          <div className="bg-white overflow-hidden shadow rounded-lg">
            <div className="p-5">
              <div className="text-center">
                <dt className="text-sm font-medium text-gray-500">Foods Researched</dt>
                <dd className="text-3xl font-semibold text-keto">{stats.by_food?.length || 0}</dd>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Tabs */}
      <div className="border-b border-gray-200">
        <nav className="-mb-px flex space-x-8">
          <button
            onClick={() => setActiveTab('search')}
            className={`${
              activeTab === 'search'
                ? 'border-primary text-primary'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            } whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm`}
          >
            Search PubMed
          </button>
          <button
            onClick={() => setActiveTab('saved')}
            className={`${
              activeTab === 'saved'
                ? 'border-primary text-primary'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            } whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm`}
          >
            My Library ({savedStudies?.length || 0})
          </button>
          <button
            onClick={() => setActiveTab('calculator')}
            className={`${
              activeTab === 'calculator'
                ? 'border-primary text-primary'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            } whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm`}
          >
            🧪 Dose Calculator
          </button>
        </nav>
      </div>

      {/* Search Tab */}
      {activeTab === 'search' && (
        <div className="space-y-6">
          <div className="bg-white shadow rounded-lg p-6">
            <div className="space-y-4">
              <div>
                <label htmlFor="search" className="block text-sm font-medium text-gray-700 mb-2">
                  Search PubMed Research
                </label>
                <p className="text-xs text-gray-500 mb-3">
                  Try: "ginger AND colon cancer", "turmeric curcumin colorectal", "green tea EGCG cancer"
                </p>
                <div className="flex gap-3">
                  <input
                    type="text"
                    id="search"
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
                    placeholder="e.g., ginger AND colon cancer"
                    className="flex-1 px-4 py-2 border border-gray-300 rounded-md focus:ring-primary focus:border-primary"
                  />
                  <button
                    onClick={handleSearch}
                    disabled={isSearching || !searchQuery.trim()}
                    className="px-6 py-2 bg-primary text-white rounded-md hover:bg-blue-700 transition-colors disabled:bg-gray-300"
                  >
                    {isSearching ? 'Searching...' : 'Search'}
                  </button>
                </div>
              </div>

              {/* Quick Search Buttons */}
              <div className="flex flex-wrap gap-2">
                <p className="text-xs text-gray-500 w-full">Quick searches:</p>
                {['ginger colon cancer', 'turmeric colorectal cancer', 'green tea EGCG cancer', 'cruciferous vegetables cancer'].map((query) => (
                  <button
                    key={query}
                    onClick={() => {
                      setSearchQuery(query);
                      api.searchPubMed(query, 20).then(setSearchResults);
                      setIsSearching(false);
                    }}
                    className="px-3 py-1 text-xs bg-gray-100 text-gray-700 rounded-full hover:bg-gray-200"
                  >
                    {query}
                  </button>
                ))}
              </div>
            </div>
          </div>

          {/* Search Results */}
          {searchResults.length > 0 && (
            <div className="space-y-4">
              <h2 className="text-xl font-semibold text-gray-900">
                Found {searchResults.length} studies
              </h2>
              {searchResults.map((study) => (
                <StudyCard key={study.pubmed_id} study={study} />
              ))}
            </div>
          )}
        </div>
      )}

      {/* Saved Tab */}
      {activeTab === 'saved' && (
        <div className="space-y-4">
          {savedStudies && savedStudies.length > 0 ? (
            <>
              <h2 className="text-xl font-semibold text-gray-900">
                Your saved research ({savedStudies.length} studies)
              </h2>
              {savedStudies.map((study: any) => (
                <StudyCard key={study.pubmed_id} study={study} isSaved={true} />
              ))}
            </>
          ) : (
            <div className="bg-white shadow rounded-lg p-12 text-center">
              <p className="text-gray-500">No saved studies yet.</p>
              <p className="text-sm text-gray-400 mt-2">
                Search PubMed and save studies to build your research library!
              </p>
            </div>
          )}
        </div>
      )}

      {/* Dose Calculator Tab */}
      {activeTab === 'calculator' && (
        <div className="space-y-6">
          <div className="bg-white shadow rounded-lg p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-2">Animal Study to Human Dose Calculator</h2>
            <p className="text-sm text-gray-600 mb-6">
              Convert research doses from animal studies (mice, rats, etc.) to human equivalent doses using FDA-approved allometric scaling.
            </p>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Left Column - Study Info */}
              <div className="space-y-4">
                <h3 className="font-semibold text-gray-900">Study Information</h3>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Study Type *
                  </label>
                  <select
                    value={doseForm.study_type}
                    onChange={(e) => setDoseForm({ ...doseForm, study_type: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-primary focus:border-primary"
                  >
                    <option value="mouse">Mouse</option>
                    <option value="rat">Rat</option>
                    <option value="rabbit">Rabbit</option>
                    <option value="dog">Dog</option>
                    <option value="monkey">Monkey</option>
                    <option value="petri_dish">Petri Dish / In Vitro</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Study Dose (mg/kg) *
                  </label>
                  <input
                    type="number"
                    step="0.1"
                    value={doseForm.study_dose_mg_kg}
                    onChange={(e) => setDoseForm({ ...doseForm, study_dose_mg_kg: e.target.value })}
                    placeholder="e.g., 50"
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-primary focus:border-primary"
                  />
                  <p className="text-xs text-gray-500 mt-1">Dose given to animals in the study</p>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Your Weight (kg) *
                  </label>
                  <input
                    type="number"
                    step="0.1"
                    value={doseForm.human_weight_kg}
                    onChange={(e) => setDoseForm({ ...doseForm, human_weight_kg: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-primary focus:border-primary"
                  />
                </div>
              </div>

              {/* Right Column - Food/Compound Info */}
              <div className="space-y-4">
                <h3 className="font-semibold text-gray-900">Food & Compound Details</h3>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Compound Name *
                  </label>
                  <input
                    type="text"
                    value={doseForm.compound_name}
                    onChange={(e) => setDoseForm({ ...doseForm, compound_name: e.target.value })}
                    placeholder="e.g., curcumin, gingerol"
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-primary focus:border-primary"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Food Source *
                  </label>
                  <input
                    type="text"
                    value={doseForm.food_name}
                    onChange={(e) => setDoseForm({ ...doseForm, food_name: e.target.value })}
                    placeholder="e.g., turmeric powder, fresh ginger"
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-primary focus:border-primary"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Compound per 100g Food (mg) *
                  </label>
                  <input
                    type="number"
                    step="0.1"
                    value={doseForm.compound_per_100g_food}
                    onChange={(e) => setDoseForm({ ...doseForm, compound_per_100g_food: e.target.value })}
                    placeholder="e.g., 3000"
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-primary focus:border-primary"
                  />
                  <p className="text-xs text-gray-500 mt-1">
                    How much compound is in 100g of the food
                  </p>
                </div>
              </div>
            </div>

            <button
              onClick={handleCalculateDose}
              disabled={calculating}
              className="w-full mt-6 px-6 py-3 bg-primary text-white rounded-md hover:bg-blue-700 transition-colors disabled:bg-gray-300 font-semibold"
            >
              {calculating ? 'Calculating...' : 'Calculate Human Dose'}
            </button>
          </div>

          {/* Results Display */}
          {calculatorResult && (
            <div className="bg-white shadow rounded-lg p-6">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">📊 Results</h2>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* Study Details */}
                <div className="bg-blue-50 p-4 rounded-lg">
                  <h3 className="font-semibold text-gray-900 mb-2">Study Details</h3>
                  <div className="space-y-1 text-sm">
                    <p><span className="font-medium">Compound:</span> {calculatorResult.compound}</p>
                    <p><span className="font-medium">Food Source:</span> {calculatorResult.food_source}</p>
                    <p><span className="font-medium">Study Type:</span> {calculatorResult.study_details.study_type}</p>
                    <p><span className="font-medium">Study Dose:</span> {calculatorResult.study_details.dose_mg_kg} mg/kg</p>
                    <p><span className="font-medium">Method:</span> {calculatorResult.study_details.method}</p>
                  </div>
                </div>

                {/* Human Equivalent Doses */}
                <div className="bg-green-50 p-4 rounded-lg">
                  <h3 className="font-semibold text-gray-900 mb-2">Human Equivalent Doses</h3>
                  <div className="space-y-1 text-sm">
                    <p><span className="font-medium">Your Weight:</span> {calculatorResult.human_equivalent.weight_kg} kg</p>
                    <p className="text-lg font-bold text-primary mt-2">
                      Calculated: {calculatorResult.human_equivalent.calculated_dose_mg} mg
                    </p>
                    <p className="text-lg font-bold text-secondary">
                      Conservative: {calculatorResult.human_equivalent.conservative_dose_mg} mg
                    </p>
                  </div>
                </div>

                {/* Daily Food Amounts - Calculated */}
                <div className="bg-purple-50 p-4 rounded-lg">
                  <h3 className="font-semibold text-gray-900 mb-2">Daily Amount (Calculated Dose)</h3>
                  <div className="space-y-1 text-sm">
                    <p className="text-2xl font-bold text-purple-700">
                      {calculatorResult.daily_food_amounts.calculated.grams}g
                    </p>
                    <p className="text-lg text-gray-700">
                      ({calculatorResult.daily_food_amounts.calculated.tablespoons} tbsp)
                    </p>
                    <p className="text-xs text-gray-600 mt-2">
                      {calculatorResult.daily_food_amounts.calculated.note}
                    </p>
                  </div>
                </div>

                {/* Daily Food Amounts - Conservative */}
                <div className="bg-orange-50 p-4 rounded-lg">
                  <h3 className="font-semibold text-gray-900 mb-2">
                    Daily Amount (Conservative - Recommended to Start)
                  </h3>
                  <div className="space-y-1 text-sm">
                    <p className="text-2xl font-bold text-orange-700">
                      {calculatorResult.daily_food_amounts.conservative.grams}g
                    </p>
                    <p className="text-lg text-gray-700">
                      ({calculatorResult.daily_food_amounts.conservative.tablespoons} tbsp)
                    </p>
                    <p className="text-xs text-gray-600 mt-2">
                      {calculatorResult.daily_food_amounts.conservative.note}
                    </p>
                  </div>
                </div>
              </div>

              {/* Recommendation */}
              <div className="mt-6 p-4 bg-yellow-50 border-l-4 border-yellow-400 rounded">
                <p className="font-semibold text-gray-900 mb-2">💡 Recommendation</p>
                <p className="text-sm text-gray-700">{calculatorResult.recommendation}</p>
                <p className="text-xs text-gray-600 mt-2">⚠️ {calculatorResult.safety_note}</p>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Study Details Modal */}
      {selectedStudy && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg max-w-3xl w-full max-h-[80vh] overflow-y-auto p-6">
            <div className="flex justify-between items-start mb-4">
              <h2 className="text-2xl font-bold text-gray-900">{selectedStudy.title}</h2>
              <button
                onClick={() => setSelectedStudy(null)}
                className="text-gray-400 hover:text-gray-600"
              >
                <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            <div className="space-y-4">
              {selectedStudy.authors && (
                <div>
                  <h3 className="font-semibold text-gray-900">Authors</h3>
                  <p className="text-gray-700">{selectedStudy.authors}</p>
                </div>
              )}
              {selectedStudy.journal && (
                <div>
                  <h3 className="font-semibold text-gray-900">Journal</h3>
                  <p className="text-gray-700">{selectedStudy.journal} ({selectedStudy.year})</p>
                </div>
              )}
              {selectedStudy.abstract && (
                <div>
                  <h3 className="font-semibold text-gray-900">Abstract</h3>
                  <p className="text-gray-700 whitespace-pre-wrap">{selectedStudy.abstract}</p>
                </div>
              )}
              {selectedStudy.doi && (
                <div>
                  <h3 className="font-semibold text-gray-900">DOI</h3>
                  <p className="text-gray-700">{selectedStudy.doi}</p>
                </div>
              )}
              {selectedStudy.url && (
                <a
                  href={selectedStudy.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-block px-6 py-3 bg-secondary text-white rounded-md hover:bg-green-600 transition-colors"
                >
                  View on PubMed →
                </a>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
