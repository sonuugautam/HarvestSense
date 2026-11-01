import React from 'react';
import { Sparkles, ArrowRight, Bookmark } from 'lucide-react';

export default function ScenarioSelector({ scenarios, activeScenarioId, onSelectScenario }) {
  if (!scenarios || scenarios.length === 0) return null;

  return (
    <div className="bg-white rounded-2xl p-4 sm:p-5 border border-slate-200 shadow-sm mb-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-3 mb-3 border-b border-slate-100 gap-2">
        <div className="flex items-center space-x-2">
          <div className="p-1.5 rounded-lg bg-emerald-50 text-emerald-600">
            <Sparkles className="w-4 h-4" />
          </div>
          <div>
            <h2 className="text-sm font-bold text-slate-900">Preloaded Realistic Agricultural Scenarios</h2>
            <p className="text-xs text-slate-500">1-click simulation testbeds demonstrating smallholder challenges</p>
          </div>
        </div>
        <span className="text-xs font-medium text-emerald-700 bg-emerald-50 px-2.5 py-1 rounded-full border border-emerald-200 self-start sm:self-auto">
          Instant Live Demo
        </span>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-2.5">
        {scenarios.map((sc) => {
          const isActive = activeScenarioId === sc.id;
          return (
            <button
              key={sc.id}
              onClick={() => onSelectScenario(sc)}
              className={`text-left p-3 rounded-xl border transition flex flex-col justify-between relative group ${
                isActive
                  ? 'bg-emerald-50/80 border-emerald-500 shadow-sm ring-1 ring-emerald-500/30'
                  : 'bg-slate-50/60 hover:bg-slate-100/80 border-slate-200 hover:border-slate-300'
              }`}
            >
              <div>
                <span className={`inline-block text-[10px] font-semibold px-2 py-0.5 rounded-md mb-1.5 ${
                  isActive ? 'bg-emerald-200/80 text-emerald-900' : 'bg-slate-200/70 text-slate-700'
                }`}>
                  {sc.badge}
                </span>
                <p className="text-xs font-bold text-slate-900 leading-snug line-clamp-2">
                  {sc.title}
                </p>
              </div>

              <div className="mt-3 pt-2 border-t border-slate-200/60 flex items-center justify-between text-[11px] font-medium text-slate-500 group-hover:text-emerald-700">
                <span>{sc.params.quantity_quintals} q • {sc.params.storage_type}</span>
                <ArrowRight className={`w-3.5 h-3.5 transition-transform ${isActive ? 'translate-x-0.5 text-emerald-600' : 'text-slate-400 group-hover:translate-x-0.5'}`} />
              </div>
            </button>
          );
        })}
      </div>
    </div>
  );
}

