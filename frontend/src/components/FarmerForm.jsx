import React from 'react';
import { 
  Tractor, Calendar, Layers, Warehouse, Clock, 
  Fuel, Truck, Play, RefreshCw, AlertCircle 
} from 'lucide-react';

export default function FarmerForm({ 
  crops, 
  formData, 
  onChange, 
  onSubmit, 
  isLoading 
}) {
  const selectedCrop = crops.find(c => c.id === formData.crop_id) || crops[0] || {};

  const handleInputChange = (field, value) => {
    onChange({ ...formData, [field]: value });
  };

  return (
    <div className="bg-white rounded-2xl p-5 sm:p-6 border border-slate-200 shadow-sm">
      <div className="flex items-center justify-between pb-4 mb-5 border-b border-slate-100">
        <div className="flex items-center space-x-2.5">
          <div className="p-2 rounded-xl bg-emerald-100 text-emerald-700">
            <Tractor className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-base font-bold text-slate-900">Farmer Harvest Profile</h2>
            <p className="text-xs text-slate-500">Configure harvest metrics for multi-agent evaluation</p>
          </div>
        </div>

        {selectedCrop.perishability_class && (
          <span className={`text-xs px-2.5 py-1 rounded-full font-bold ${
            selectedCrop.perishability_class === 'HIGH'
              ? 'bg-rose-100 text-rose-800 border border-rose-200'
              : selectedCrop.perishability_class === 'MEDIUM'
              ? 'bg-amber-100 text-amber-800 border border-amber-200'
              : 'bg-emerald-100 text-emerald-800 border border-emerald-200'
          }`}>
            {selectedCrop.perishability_class} Perishability
          </span>
        )}
      </div>

      <form onSubmit={(e) => { e.preventDefault(); onSubmit(); }} className="space-y-4">
        
        {/* Row 1: Crop & Quantity */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1.5">
              Crop Commodity
            </label>
            <select
              value={formData.crop_id}
              onChange={(e) => handleInputChange('crop_id', e.target.value)}
              className="w-full px-3 py-2 text-sm bg-slate-50 border border-slate-300 rounded-xl focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 font-medium text-slate-900"
            >
              {crops.map((c) => (
                <option key={c.id} value={c.id}>
                  {c.name} (FAO #{c.fao_item_code})
                </option>
              ))}
            </select>
            <div className="mt-1 flex items-center justify-between text-[11px] text-slate-500">
              <span>FAO Baseline: ₹{selectedCrop.baseline_price_per_quintal || 0}/q</span>
              <span>Shelf life: {selectedCrop.shelf_life_days_ambient || 0}d (ambient)</span>
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1.5">
              Harvest Quantity (Quintals)
            </label>
            <div className="relative">
              <input
                type="number"
                min="0.5"
                step="0.5"
                value={formData.quantity_quintals}
                onChange={(e) => handleInputChange('quantity_quintals', parseFloat(e.target.value) || 0)}
                className="w-full px-3 py-2 text-sm bg-slate-50 border border-slate-300 rounded-xl focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 font-semibold text-slate-900 pr-16"
              />
              <span className="absolute right-3 top-2.5 text-xs text-slate-400 font-medium">
                Quintals
              </span>
            </div>
            <p className="mt-1 text-[11px] text-slate-500">
              = {((formData.quantity_quintals || 0) * 100).toLocaleString()} kg ({((formData.quantity_quintals || 0) / 10).toFixed(2)} metric tonnes)
            </p>
          </div>
        </div>

        {/* Row 2: Quality Grade & Storage Facility */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1.5">
              Produce Quality Grade
            </label>
            <select
              value={formData.quality_grade}
              onChange={(e) => handleInputChange('quality_grade', e.target.value)}
              className="w-full px-3 py-2 text-sm bg-slate-50 border border-slate-300 rounded-xl focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 font-medium text-slate-900"
            >
              <option value="Grade A">Grade A (Premium / Export Quality - +15-20%)</option>
              <option value="Grade B">Grade B (Standard Commercial Market Quality)</option>
              <option value="Grade C">Grade C (Fair Average / Secondary Processing - -15-25%)</option>
            </select>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1.5">
              On-Farm Storage Available
            </label>
            <select
              value={formData.storage_type}
              onChange={(e) => handleInputChange('storage_type', e.target.value)}
              className="w-full px-3 py-2 text-sm bg-slate-50 border border-slate-300 rounded-xl focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 font-medium text-slate-900"
            >
              <option value="ambient">Standard Farm Shed (Ambient - ₹0/q/day, 1.0x decay)</option>
              <option value="ventilated">Ventilated Slatted Shed (₹0.50/q/day, 0.4x decay)</option>
              <option value="hermetic_bag">PICS Hermetic Storage Bags (₹0.25/q/day, 0.2x decay)</option>
              <option value="cold_storage">Cold Storage Chilling Unit (₹2.50/q/day, 0.1x decay)</option>
              <option value="warehouse">State Warehousing / Silo (₹0.40/q/day, 0.1x decay)</option>
            </select>
          </div>
        </div>

        {/* Row 3: Location & Harvest Date */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1.5">
              Farm Location / District Block
            </label>
            <input
              type="text"
              value={formData.farmer_location}
              onChange={(e) => handleInputChange('farmer_location', e.target.value)}
              className="w-full px-3 py-2 text-sm bg-slate-50 border border-slate-300 rounded-xl focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 font-medium text-slate-900"
              placeholder="e.g. Nashik Valley / Dindori Block"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1.5">
              Harvest Date
            </label>
            <input
              type="date"
              value={formData.harvest_date}
              onChange={(e) => handleInputChange('harvest_date', e.target.value)}
              className="w-full px-3 py-2 text-sm bg-slate-50 border border-slate-300 rounded-xl focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 font-medium text-slate-900"
            />
          </div>
        </div>

        {/* Row 4: Sliders for Planning Horizon & Fuel Modifier */}
        <div className="p-3.5 bg-slate-50 rounded-xl border border-slate-200/80 space-y-3">
          <div>
            <div className="flex items-center justify-between text-xs font-semibold text-slate-700 mb-1">
              <span className="flex items-center space-x-1.5">
                <Clock className="w-3.5 h-3.5 text-slate-500" />
                <span>Decision Horizon Window:</span>
              </span>
              <span className="text-emerald-700 font-bold bg-emerald-100/60 px-2 py-0.5 rounded">
                Up to {formData.max_wait_days} Days Ahead
              </span>
            </div>
            <input
              type="range"
              min="0"
              max="14"
              value={formData.max_wait_days}
              onChange={(e) => handleInputChange('max_wait_days', parseInt(e.target.value))}
              className="w-full accent-emerald-600 cursor-pointer"
            />
            <div className="flex justify-between text-[10px] text-slate-400">
              <span>Day 0 (Sell Today)</span>
              <span>Day 7 (1 Week)</span>
              <span>Day 14 (2 Weeks)</span>
            </div>
          </div>

          <div>
            <div className="flex items-center justify-between text-xs font-semibold text-slate-700 mb-1">
              <span className="flex items-center space-x-1.5">
                <Fuel className="w-3.5 h-3.5 text-slate-500" />
                <span>Transport Fuel Cost Modifier:</span>
              </span>
              <span className="text-slate-700 font-bold bg-slate-200/70 px-2 py-0.5 rounded">
                {formData.fuel_price_modifier === 1.0 
                  ? 'Standard (1.0x)' 
                  : `${formData.fuel_price_modifier > 1 ? '+' : ''}${Math.round((formData.fuel_price_modifier - 1.0) * 100)}%`}
              </span>
            </div>
            <input
              type="range"
              min="0.8"
              max="1.5"
              step="0.05"
              value={formData.fuel_price_modifier}
              onChange={(e) => handleInputChange('fuel_price_modifier', parseFloat(e.target.value))}
              className="w-full accent-emerald-600 cursor-pointer"
            />
          </div>
        </div>

        {/* Submit Optimization CTA */}
        <button
          type="submit"
          disabled={isLoading}
          className="w-full py-3 px-4 rounded-xl font-bold text-sm text-white bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 shadow-md shadow-emerald-700/20 active:scale-[0.99] transition flex items-center justify-center space-x-2 disabled:opacity-60 cursor-pointer"
        >
          {isLoading ? (
            <>
              <RefreshCw className="w-4 h-4 animate-spin" />
              <span>Agents Negotiating Optimal Plan...</span>
            </>
          ) : (
            <>
              <Play className="w-4 h-4 fill-current" />
              <span>Run Multi-Agent Optimization</span>
            </>
          )}
        </button>

      </form>
    </div>
  );
}

