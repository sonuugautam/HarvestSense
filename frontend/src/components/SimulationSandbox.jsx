import React, { useState } from 'react';
import { Sliders, Play, RotateCcw, TrendingUp, TrendingDown, ShieldAlert, CheckCircle2 } from 'lucide-react';
import { runSimulation } from '../services/api';

export default function SimulationSandbox({ baseRequest, baselinePlan }) {
  const [simDay, setSimDay] = useState(baselinePlan?.sell_day || 0);
  const [simStorage, setSimStorage] = useState(baseRequest?.storage_type || 'ambient');
  const [fuelShock, setFuelShock] = useState(0); // -20 to +40%
  const [priceShock, setPriceShock] = useState(0); // -20 to +30%
  const [isSimulating, setIsSimulating] = useState(false);
  const [simResult, setSimResult] = useState(null);

  if (!baselinePlan || !baseRequest) return null;

  const handleRunSimulation = async () => {
    setIsSimulating(true);
    try {
      const payload = {
        base_request: baseRequest,
        simulated_wait_day: simDay,
        simulated_storage_type: simStorage,
        fuel_price_shock_pct: fuelShock,
        market_price_shock_pct: priceShock
      };
      const res = await runSimulation(payload);
      setSimResult(res);
    } catch (err) {
      console.error('Simulation error:', err);
    } finally {
      setIsSimulating(false);
    }
  };

  const handleReset = () => {
    setSimDay(baselinePlan.sell_day || 0);
    setSimStorage(baseRequest.storage_type || 'ambient');
    setFuelShock(0);
    setPriceShock(0);
    setSimResult(null);
  };

  return (
    <div className="bg-white rounded-2xl p-5 sm:p-6 border border-slate-200 shadow-sm">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-4 mb-4 border-b border-slate-100 gap-2">
        <div className="flex items-center space-x-2.5">
          <div className="p-2 rounded-xl bg-amber-100 text-amber-700">
            <Sliders className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-base font-bold text-slate-900">Interactive "What-If" Simulation Sandbox</h2>
            <p className="text-xs text-slate-500">Stress-test selling plans under fuel price shocks, storage upgrades, and market volatility</p>
          </div>
        </div>

        <button
          onClick={handleReset}
          className="text-xs text-slate-500 hover:text-slate-800 flex items-center space-x-1 self-start sm:self-auto cursor-pointer"
        >
          <RotateCcw className="w-3.5 h-3.5" />
          <span>Reset Parameters</span>
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        {/* Controls Column */}
        <div className="lg:col-span-7 space-y-4">
          
          {/* Slider 1: Simulated Sell Day */}
          <div className="p-3.5 bg-slate-50 rounded-xl border border-slate-200">
            <div className="flex justify-between items-center text-xs font-semibold text-slate-700 mb-1">
              <span>Simulated Selling Day:</span>
              <span className="font-bold text-amber-800 bg-amber-100 px-2 py-0.5 rounded">
                {simDay === 0 ? 'Today (Day 0)' : `Day +${simDay}`}
              </span>
            </div>
            <input
              type="range"
              min="0"
              max={baseRequest.max_wait_days || 7}
              value={simDay}
              onChange={(e) => setSimDay(parseInt(e.target.value))}
              className="w-full accent-amber-600 cursor-pointer"
            />
            <div className="flex justify-between text-[10px] text-slate-400 mt-0.5">
              <span>Immediate Sale</span>
              <span>Wait {baseRequest.max_wait_days || 7} Days</span>
            </div>
          </div>

          {/* Selector 2: Alternative Storage Facility */}
          <div className="p-3.5 bg-slate-50 rounded-xl border border-slate-200">
            <label className="block text-xs font-semibold text-slate-700 mb-1.5">
              Simulate Alternative Storage Facility:
            </label>
            <select
              value={simStorage}
              onChange={(e) => setSimStorage(e.target.value)}
              className="w-full px-3 py-1.5 text-xs bg-white border border-slate-300 rounded-lg font-medium text-slate-800 focus:ring-2 focus:ring-amber-500"
            >
              <option value="ambient">Standard Farm Shed (Ambient - ₹0 fee, standard decay)</option>
              <option value="ventilated">Improved Ventilated Shed (₹0.50/q, 60% decay cut)</option>
              <option value="hermetic_bag">PICS Hermetic Triple-Layer Bags (₹0.25/q)</option>
              <option value="cold_storage">Commercial Cold Storage (₹2.50/q, 90% decay cut)</option>
              <option value="warehouse">State Warehouse / Silo (₹0.40/q)</option>
            </select>
          </div>

          {/* Row: Fuel Shock & Price Shock */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div className="p-3 bg-slate-50 rounded-xl border border-slate-200">
              <div className="flex justify-between text-xs font-semibold text-slate-700 mb-1">
                <span>Fuel Cost Shock:</span>
                <span className={`font-mono font-bold ${fuelShock > 0 ? 'text-rose-600' : 'text-slate-600'}`}>
                  {fuelShock > 0 ? `+${fuelShock}%` : `${fuelShock}%`}
                </span>
              </div>
              <input
                type="range"
                min="-20"
                max="50"
                step="5"
                value={fuelShock}
                onChange={(e) => setFuelShock(parseInt(e.target.value))}
                className="w-full accent-amber-600 cursor-pointer"
              />
            </div>

            <div className="p-3 bg-slate-50 rounded-xl border border-slate-200">
              <div className="flex justify-between text-xs font-semibold text-slate-700 mb-1">
                <span>Market Price Volatility:</span>
                <span className={`font-mono font-bold ${priceShock >= 0 ? 'text-emerald-600' : 'text-rose-600'}`}>
                  {priceShock > 0 ? `+${priceShock}%` : `${priceShock}%`}
                </span>
              </div>
              <input
                type="range"
                min="-25"
                max="30"
                step="5"
                value={priceShock}
                onChange={(e) => setPriceShock(parseInt(e.target.value))}
                className="w-full accent-amber-600 cursor-pointer"
              />
            </div>
          </div>

          <button
            onClick={handleRunSimulation}
            disabled={isSimulating}
            className="w-full py-2.5 px-4 rounded-xl font-bold text-xs text-white bg-slate-900 hover:bg-slate-800 transition flex items-center justify-center space-x-1.5 shadow-sm cursor-pointer disabled:opacity-60"
          >
            <Play className="w-3.5 h-3.5 fill-current" />
            <span>{isSimulating ? 'Simulating Dynamic Scenario...' : 'Execute What-If Simulation'}</span>
          </button>

        </div>

        {/* Results Column */}
        <div className="lg:col-span-5 bg-slate-50 rounded-xl p-4 border border-slate-200 flex flex-col justify-between">
          
          {simResult ? (
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold text-slate-700 uppercase tracking-wider">
                  Simulation Outcome
                </span>
                <span className={`text-xs px-2.5 py-0.5 rounded-full font-bold ${
                  simResult.delta_net_profit >= 0 
                    ? 'bg-emerald-100 text-emerald-800 border border-emerald-300' 
                    : 'bg-rose-100 text-rose-800 border border-rose-300'
                }`}>
                  {simResult.verdict}
                </span>
              </div>

              {/* Profit Comparison Delta */}
              <div className="p-3 bg-white rounded-xl border border-slate-200 shadow-sm">
                <div className="flex justify-between items-center text-xs text-slate-500 mb-1">
                  <span>Net Profit Impact:</span>
                  <span className="font-mono text-slate-600">Baseline: ₹{simResult.baseline_recommended.net_profit.toLocaleString()}</span>
                </div>
                <div className="flex items-baseline space-x-2">
                  <span className={`text-2xl font-black font-mono ${
                    simResult.delta_net_profit >= 0 ? 'text-emerald-600' : 'text-rose-600'
                  }`}>
                    {simResult.delta_net_profit >= 0 ? '+' : ''}₹{simResult.delta_net_profit.toLocaleString()}
                  </span>
                  <span className="text-xs text-slate-500">
                    ({simResult.simulated_plan.net_profit.toLocaleString()} total)
                  </span>
                </div>
              </div>

              {/* Spoilage Delta */}
              <div className="p-3 bg-white rounded-xl border border-slate-200 shadow-sm">
                <div className="flex justify-between items-center text-xs text-slate-500 mb-1">
                  <span>Spoilage Rate Change:</span>
                  <span className="font-mono text-slate-600">Baseline: {simResult.baseline_recommended.total_spoilage_loss_pct}%</span>
                </div>
                <div className="flex items-baseline space-x-2">
                  <span className={`text-xl font-bold font-mono ${
                    simResult.delta_spoilage_pct <= 0 ? 'text-emerald-600' : 'text-rose-600'
                  }`}>
                    {simResult.delta_spoilage_pct > 0 ? '+' : ''}{simResult.delta_spoilage_pct}%
                  </span>
                  <span className="text-xs text-slate-500">
                    ({simResult.simulated_plan.total_spoilage_loss_pct}% simulated)
                  </span>
                </div>
              </div>

              {/* Parameters Summary */}
              <div className="text-[11px] text-slate-500 space-y-1">
                <div>• Storage: <strong className="text-slate-700">{simResult.simulated_storage_used}</strong></div>
                <div>• Timing: <strong className="text-slate-700">Day +{simResult.simulated_day} ({simResult.simulated_plan.sell_date})</strong></div>
                <div>• Fuel shock: <strong className="text-slate-700">{simResult.fuel_price_shock_pct}%</strong></div>
              </div>

            </div>
          ) : (
            <div className="h-full flex flex-col items-center justify-center text-center p-6 text-slate-400 space-y-2">
              <Sliders className="w-8 h-8 text-slate-300 stroke-[1.5]" />
              <p className="text-xs font-medium text-slate-600">No Simulation Active</p>
              <p className="text-[11px] text-slate-400 leading-relaxed">
                Adjust sliders to test alternative wait days, fuel spikes, or cold storage upgrades, then click "Execute What-If Simulation".
              </p>
            </div>
          )}

        </div>

      </div>
    </div>
  );
}

