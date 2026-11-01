import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import ScenarioSelector from './components/ScenarioSelector';
import FarmerForm from './components/FarmerForm';
import HeroRecommendation from './components/HeroRecommendation';
import AgentDeliberationFeed from './components/AgentDeliberationFeed';
import MarketComparisonTable from './components/MarketComparisonTable';
import PriceProfitForecastChart from './components/PriceProfitForecastChart';
import SimulationSandbox from './components/SimulationSandbox';
import SdgImpactPanel from './components/SdgImpactPanel';
import ProvenanceModal from './components/ProvenanceModal';

import { 
  fetchCrops, fetchMarkets, fetchScenarios, runOptimization 
} from './services/api';

import { 
  Bot, Layers, TrendingUp, Sliders, Target, 
  Terminal, ShieldCheck, Heart, AlertCircle 
} from 'lucide-react';

export default function App() {
  const [crops, setCrops] = useState([]);
  const [markets, setMarkets] = useState([]);
  const [scenarios, setScenarios] = useState([]);
  const [activeScenarioId, setActiveScenarioId] = useState('nashik_tomatoes');
  const [activeTab, setActiveTab] = useState('all'); // 'all', 'deliberation', 'comparison', 'forecast', 'simulation'

  const [formData, setFormData] = useState({
    crop_id: 'tomatoes',
    quantity_quintals: 18.0,
    harvest_date: new Date().toISOString().split('T')[0],
    quality_grade: 'Grade A',
    farmer_location: 'Dindori Block, Nashik Valley',
    storage_type: 'ambient',
    max_wait_days: 6,
    preferred_vehicle: null,
    fuel_price_modifier: 1.0
  });

  const [optimizationResult, setOptimizationResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [isProvenanceOpen, setIsProvenanceOpen] = useState(false);

  // Initial load
  useEffect(() => {
    async function init() {
      try {
        const [cropsData, marketsData, scenariosData] = await Promise.all([
          fetchCrops(),
          fetchMarkets(),
          fetchScenarios()
        ]);
        setCrops(cropsData);
        setMarkets(marketsData);
        setScenarios(scenariosData);

        // Preload first scenario
        if (scenariosData && scenariosData.length > 0) {
          const firstSc = scenariosData[0];
          setActiveScenarioId(firstSc.id);
          setFormData({
            ...firstSc.params,
            harvest_date: new Date().toISOString().split('T')[0]
          });
          // Trigger first optimization
          executeOptimization({
            ...firstSc.params,
            harvest_date: new Date().toISOString().split('T')[0]
          });
        }
      } catch (err) {
        console.error('Failed to initialize HarvestSense data:', err);
        setError('Failed to load system baseline data. Please ensure the backend is running.');
      }
    }
    init();
  }, []);

  const executeOptimization = async (paramsToRun) => {
    setIsLoading(true);
    setError(null);
    try {
      const payload = paramsToRun || formData;
      const result = await runOptimization(payload);
      setOptimizationResult(result);
    } catch (err) {
      console.error('Optimization error:', err);
      setError(err.message || 'Failed to complete multi-agent optimization');
    } finally {
      setIsLoading(false);
    }
  };

  const handleSelectScenario = (scenario) => {
    setActiveScenarioId(scenario.id);
    const updatedForm = {
      ...scenario.params,
      harvest_date: new Date().toISOString().split('T')[0]
    };
    setFormData(updatedForm);
    executeOptimization(updatedForm);
  };

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 flex flex-col font-sans">
      
      {/* Top Navigation */}
      <Navbar 
        onOpenProvenance={() => setIsProvenanceOpen(true)}
        isOptimizing={isLoading}
      />

      {/* Main Container */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6 space-y-6">
        
        {/* Error Alert */}
        {error && (
          <div className="p-4 rounded-2xl bg-rose-50 border border-rose-200 text-rose-800 text-xs flex items-center space-x-2">
            <AlertCircle className="w-4 h-4 text-rose-600 shrink-0" />
            <span>{error}</span>
          </div>
        )}

        {/* Preloaded Realistic Scenarios Selector */}
        <ScenarioSelector
          scenarios={scenarios}
          activeScenarioId={activeScenarioId}
          onSelectScenario={handleSelectScenario}
        />

        {/* Top Grid: Farmer Inputs & Hero Recommendation */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
          <div className="lg:col-span-5">
            <FarmerForm
              crops={crops}
              formData={formData}
              onChange={setFormData}
              onSubmit={() => executeOptimization(formData)}
              isLoading={isLoading}
            />
          </div>

          <div className="lg:col-span-7">
            {optimizationResult ? (
              <HeroRecommendation
                plan={optimizationResult.recommended_plan}
                farmerProfile={optimizationResult.farmer_profile}
                cropInfo={optimizationResult.crop_info}
              />
            ) : (
              <div className="h-full bg-white rounded-3xl p-8 border border-slate-200 flex flex-col items-center justify-center text-center">
                <Bot className="w-12 h-12 text-slate-300 animate-pulse mb-3" />
                <h3 className="text-base font-bold text-slate-800">Ready to Optimize</h3>
                <p className="text-xs text-slate-500 max-w-sm mt-1">
                  Adjust farmer parameters and click "Run Multi-Agent Optimization" to trigger cooperative planning.
                </p>
              </div>
            )}
          </div>
        </div>

        {/* Section Navigation Tabs */}
        {optimizationResult && (
          <div className="flex items-center justify-between border-b border-slate-200 pb-3 pt-2">
            <div className="flex flex-wrap items-center gap-2 text-xs">
              <button
                onClick={() => setActiveTab('all')}
                className={`px-3 py-1.5 rounded-xl font-bold transition cursor-pointer flex items-center space-x-1.5 ${
                  activeTab === 'all'
                    ? 'bg-slate-900 text-white shadow-sm'
                    : 'bg-white text-slate-600 hover:bg-slate-100 border border-slate-200'
                }`}
              >
                <Layers className="w-3.5 h-3.5" />
                <span>Full Executive Overview</span>
              </button>

              <button
                onClick={() => setActiveTab('deliberation')}
                className={`px-3 py-1.5 rounded-xl font-bold transition cursor-pointer flex items-center space-x-1.5 ${
                  activeTab === 'deliberation'
                    ? 'bg-slate-900 text-white shadow-sm'
                    : 'bg-white text-slate-600 hover:bg-slate-100 border border-slate-200'
                }`}
              >
                <Terminal className="w-3.5 h-3.5 text-purple-600" />
                <span>Agent Deliberation Logs</span>
              </button>

              <button
                onClick={() => setActiveTab('comparison')}
                className={`px-3 py-1.5 rounded-xl font-bold transition cursor-pointer flex items-center space-x-1.5 ${
                  activeTab === 'comparison'
                    ? 'bg-slate-900 text-white shadow-sm'
                    : 'bg-white text-slate-600 hover:bg-slate-100 border border-slate-200'
                }`}
              >
                <Layers className="w-3.5 h-3.5 text-sky-600" />
                <span>Alternative Markets</span>
              </button>

              <button
                onClick={() => setActiveTab('forecast')}
                className={`px-3 py-1.5 rounded-xl font-bold transition cursor-pointer flex items-center space-x-1.5 ${
                  activeTab === 'forecast'
                    ? 'bg-slate-900 text-white shadow-sm'
                    : 'bg-white text-slate-600 hover:bg-slate-100 border border-slate-200'
                }`}
              >
                <TrendingUp className="w-3.5 h-3.5 text-emerald-600" />
                <span>14-Day Price Forecast</span>
              </button>

              <button
                onClick={() => setActiveTab('simulation')}
                className={`px-3 py-1.5 rounded-xl font-bold transition cursor-pointer flex items-center space-x-1.5 ${
                  activeTab === 'simulation'
                    ? 'bg-slate-900 text-white shadow-sm'
                    : 'bg-white text-slate-600 hover:bg-slate-100 border border-slate-200'
                }`}
              >
                <Sliders className="w-3.5 h-3.5 text-amber-600" />
                <span>What-If Sandbox</span>
              </button>
            </div>
          </div>
        )}

        {/* Tab / Section Content */}
        {optimizationResult && (
          <div className="space-y-6">
            
            {/* View 1: Deliberation Logs */}
            {(activeTab === 'all' || activeTab === 'deliberation') && (
              <AgentDeliberationFeed logs={optimizationResult.agent_logs} />
            )}

            {/* View 2: Alternative Market Comparison Table */}
            {(activeTab === 'all' || activeTab === 'comparison') && (
              <MarketComparisonTable
                recommendedPlan={optimizationResult.recommended_plan}
                alternativePlans={optimizationResult.alternative_plans}
              />
            )}

            {/* View 3: Temporal Price & Profit Forecast Horizon */}
            {(activeTab === 'all' || activeTab === 'forecast') && (
              <PriceProfitForecastChart
                timeline={optimizationResult.price_profit_timeline}
                cropInfo={optimizationResult.crop_info}
              />
            )}

            {/* View 4: Interactive What-If Simulation Sandbox */}
            {(activeTab === 'all' || activeTab === 'simulation') && (
              <SimulationSandbox
                baseRequest={formData}
                baselinePlan={optimizationResult.recommended_plan}
              />
            )}

            {/* SDG 2 Impact Section */}
            <SdgImpactPanel metrics={optimizationResult.sdg2_impact_metrics} />

          </div>
        )}

      </main>

      {/* Provenance Transparency Modal */}
      <ProvenanceModal
        isOpen={isProvenanceOpen}
        onClose={() => setIsProvenanceOpen(false)}
      />

      {/* Footer */}
      <footer className="bg-white border-t border-slate-200 py-6 mt-12 text-xs text-slate-500">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center space-x-2">
            <span className="font-extrabold text-slate-900">HarvestSense</span>
            <span>• Google Solution Challenge 2026</span>
            <span>• Aligned with SDG 2 (Zero Hunger)</span>
          </div>

          <div className="flex items-center space-x-4 text-[11px]">
            <span>Primary Data: FAOSTAT (Domain PP)</span>
            <button
              onClick={() => setIsProvenanceOpen(true)}
              className="text-emerald-700 hover:underline cursor-pointer font-medium"
            >
              Provenance & Methodology
            </button>
          </div>
        </div>
      </footer>

    </div>
  );
}
