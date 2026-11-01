import React from 'react';
import { X, ExternalLink, ShieldCheck, Database, Layers, CheckCircle } from 'lucide-react';

export default function ProvenanceModal({ isOpen, onClose }) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/70 backdrop-blur-sm animate-fadeIn">
      <div className="bg-white rounded-3xl max-w-2xl w-full border border-slate-200 shadow-2xl overflow-hidden flex flex-col max-h-[90vh]">
        
        {/* Header */}
        <div className="p-5 sm:p-6 bg-slate-900 text-white flex items-center justify-between border-b border-slate-800">
          <div className="flex items-center space-x-2.5">
            <div className="p-2 rounded-xl bg-emerald-500/20 text-emerald-400">
              <Database className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-base font-bold">Data Provenance & Ethical AI Integrity</h2>
              <p className="text-xs text-slate-400">Transparent distinction between historical, modeled, and logistics data</p>
            </div>
          </div>
          <button 
            onClick={onClose}
            className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition cursor-pointer"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Content Body */}
        <div className="p-5 sm:p-6 space-y-5 overflow-y-auto text-xs text-slate-700 leading-relaxed">
          
          {/* Section 1: FAOSTAT */}
          <div className="p-4 rounded-2xl bg-emerald-50/60 border border-emerald-200">
            <div className="flex items-center justify-between mb-2">
              <div className="flex items-center space-x-2">
                <span className="w-2.5 h-2.5 rounded-full bg-emerald-500" />
                <h3 className="font-bold text-slate-900 text-sm">
                  1. Primary Agricultural Data Source: FAOSTAT
                </h3>
              </div>
              <a 
                href="https://www.fao.org/faostat/en/#data/PP" 
                target="_blank" 
                rel="noreferrer"
                className="text-emerald-700 hover:text-emerald-900 font-semibold flex items-center space-x-1"
              >
                <span>fao.org/faostat</span>
                <ExternalLink className="w-3 h-3" />
              </a>
            </div>
            <p className="text-slate-600 mb-2">
              All crop commodity baselines, producer prices, and monthly seasonality cycles are derived directly from the <strong>Food and Agriculture Organization of the United Nations (FAO)</strong> Corporate Statistical Database, specifically the <strong>Producer Prices (Domain PP)</strong>.
            </p>
            <div className="grid grid-cols-2 gap-2 text-[11px] font-mono bg-white p-2.5 rounded-xl border border-emerald-200/80">
              <div>• Tomatoes: FAO Code #388</div>
              <div>• Potatoes: FAO Code #116</div>
              <div>• Onions (Dry): FAO Code #403</div>
              <div>• Maize: FAO Code #56</div>
              <div>• Wheat: FAO Code #15</div>
              <div>• Green Chillies: FAO Code #401</div>
            </div>
          </div>

          {/* Section 2: Synthetic Local Market Spreads */}
          <div className="p-4 rounded-2xl bg-sky-50/60 border border-sky-200">
            <div className="flex items-center space-x-2 mb-2">
              <span className="w-2.5 h-2.5 rounded-full bg-sky-500" />
              <h3 className="font-bold text-slate-900 text-sm">
                2. Labeled Synthetic Market Spreads & Auction Dynamics
              </h3>
            </div>
            <p className="text-slate-600">
              Because real-time APMC mandi spot prices are highly fragmented and not publicly accessible via free low-latency APIs for smallholders, local market wholesale auction prices and quality-grade spreads are <strong>mathematically modeled around the FAOSTAT national baseline anchor</strong>.
            </p>
            <ul className="mt-2 list-disc list-inside text-slate-600 space-y-1">
              <li>Urban Metro Terminals: Modeled with retail demand premiums (+18% to +26%).</li>
              <li>Local Rural Taluka Mandis: Modeled with middleman discounting (-8% to -12%).</li>
              <li>Day-of-Week Liquidity Cycles: Modeled on weekend supermarket buying surges.</li>
            </ul>
          </div>

          {/* Section 3: Logistics & Post-Harvest Decay Models */}
          <div className="p-4 rounded-2xl bg-amber-50/60 border border-amber-200">
            <div className="flex items-center space-x-2 mb-2">
              <span className="w-2.5 h-2.5 rounded-full bg-amber-500" />
              <h3 className="font-bold text-slate-900 text-sm">
                3. Agricultural Logistics & Transit Spoilage Models
              </h3>
            </div>
            <p className="text-slate-600">
              Freight expenses (base booking, per-km rates, labor, mandi cess) and transit vibration/heat loss parameters are calibrated from <strong>World Bank and FAO post-harvest loss empirical research</strong> for smallholder supply chains.
            </p>
          </div>

          {/* Commitment Notice */}
          <div className="p-3 bg-slate-100 rounded-xl flex items-start space-x-2 text-[11px] text-slate-600">
            <ShieldCheck className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
            <p>
              <strong>Integrity Pledge:</strong> HarvestSense never fabricates live market telemetry or claims unverified real-time access. All data layers are explicitly labeled across every card, table, and projection graph.
            </p>
          </div>

        </div>

        {/* Footer */}
        <div className="p-4 bg-slate-50 border-t border-slate-200 flex justify-end">
          <button
            onClick={onClose}
            className="px-4 py-2 rounded-xl text-xs font-bold text-white bg-slate-900 hover:bg-slate-800 transition cursor-pointer"
          >
            Acknowledge & Close
          </button>
        </div>

      </div>
    </div>
  );
}

