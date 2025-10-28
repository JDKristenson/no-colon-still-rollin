import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import Protocol from './pages/Protocol';
import Compliance from './pages/Compliance';
import Weight from './pages/Weight';
import MealPlanner from './pages/MealPlanner';
import './index.css';

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <div className="min-h-screen bg-background">
          <nav className="bg-white border-b border-gray-200 shadow-sm">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
              <div className="flex justify-between h-16">
                <div className="flex items-center space-x-8">
                  <h1 className="text-xl font-bold text-primary">No Colon, Still Rollin'</h1>
                  <div className="flex space-x-4">
                    <Link to="/" className="text-gray-700 hover:text-primary px-3 py-2 rounded-md text-sm font-medium">
                      Dashboard
                    </Link>
                    <Link to="/protocol" className="text-gray-700 hover:text-primary px-3 py-2 rounded-md text-sm font-medium">
                      Protocol
                    </Link>
                    <Link to="/meals" className="text-gray-700 hover:text-primary px-3 py-2 rounded-md text-sm font-medium">
                      Meals
                    </Link>
                    <Link to="/compliance" className="text-gray-700 hover:text-primary px-3 py-2 rounded-md text-sm font-medium">
                      Check-In
                    </Link>
                    <Link to="/weight" className="text-gray-700 hover:text-primary px-3 py-2 rounded-md text-sm font-medium">
                      Weight
                    </Link>
                  </div>
                </div>
              </div>
            </div>
          </nav>

          <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/protocol" element={<Protocol />} />
              <Route path="/meals" element={<MealPlanner />} />
              <Route path="/compliance" element={<Compliance />} />
              <Route path="/weight" element={<Weight />} />
            </Routes>
          </main>
        </div>
      </BrowserRouter>
    </QueryClientProvider>
  );
}

export default App;
