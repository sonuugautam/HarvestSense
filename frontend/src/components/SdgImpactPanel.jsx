import React from 'react';
import { HeartHandshake, ShieldCheck, TrendingUp, Apple, Globe2, Target } from 'lucide-react';

export default function SdgImpactPanel({ metrics }) {
  if (!metrics || metrics.length === 0) return null;

  return (
    <div className="bg-gradient-to-r from-amber-950 via-slate-900 to-emerald-950 rounded-2xl p-6 text-white border border-amber-500/30 shadow-md">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-4 mb-5 border-b border-slate-800 gap-2">
        <div className="flex items-center space-x-2.5">
          <div className="p-2 rounded-xl bg-amber-500/20 text-amber-400">
            <Target className="w-5 h-5" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <h2 className="text-base font-bold text-white">United Nations SDG Alignment</h2>
              <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-amber-500/30 text-amber-300 border border-amber-500/40">
                Google Solution Challenge 2026
              </span>
            </div>
            <p className="text-xs text-slate-300">Sustainable Development Goal 2 (Zero Hunger) & Goal 12 (Responsible Consumption)</p>
          </div>
        </div>

        <div className="flex items-center space-x-1.5 text-xs text-amber-300 bg-amber-950/60 px-3 py-1.5 rounded-lg border border-amber-700/60 self-start sm:self-auto">
          <Globe2 className="w-3.5 h-3.5" />
          <span>Smallholder Resilience Engine</span>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {metrics.map((item, index) => {
          return (
            <div 
              key={index} 
              className="bg-slate-900/80 p-4 rounded-xl border border-slate-800 flex flex-col justify-between hover:border-slate-700 transition"
            >
              <div>
                <span className="text-[10px] font-bold uppercase tracking-wider text-amber-400 bg-amber-950/60 px-2 py-0.5 rounded border border-amber-800/60 inline-block mb-2">
                  {item.sdg_target}
                </span>
                <p className="text-xs text-slate-400 font-medium">{item.metric_name}</p>
                <p className="text-2xl font-black font-mono text-emerald-400 mt-1">
                  {item.value}
                </p>
              </div>

              <p className="text-xs text-slate-300 mt-3 pt-2.5 border-t border-slate-800 leading-relaxed">
                {item.impact_explanation}
              </p>
            </div>
          );
        })}
      </div>
    </div>
  );
}

