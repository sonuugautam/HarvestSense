import React from 'react';
import { Sprout, Info, ShieldCheck, Activity, Cpu, ArrowUpRight } from 'lucide-react';

export default function Navbar({ onOpenProvenance, isOptimizing }) {
  return (
    <header className="sticky top-0 z-50 bg-slate-900/95 backdrop-blur-md border-b border-slate-800 text-white shadow-lg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          
          {/* Logo & Branding */}
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-emerald-600 to-teal-400 flex items-center justify-center shadow-md shadow-emerald-900/30">
              <Sprout className="w-6 h-6 text-white" />
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <span className="font-extrabold text-lg sm:text-xl tracking-tight bg-gradient-to-r from-emerald-400 via-teal-300 to-sky-300 bg-clip-text text-transparent">
                  HarvestSense
                </span>
                <span className="text-xs px-2 py-0.5 rounded-full font-medium bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
                  Multi-Agent AI
                </span>
              </div>
              <p className="text-xs text-slate-400 hidden sm:block">
                Crop to Market Optimizer • Google Solution Challenge
              </p>
            </div>
          </div>

          {/* Active Cooperating Agents Indicator */}
          <div className="hidden lg:flex items-center space-x-2 bg-slate-800/80 px-3 py-1.5 rounded-xl border border-slate-700/60 text-xs">
            <div className="flex items-center space-x-1.5 text-slate-400 font-medium pr-1">
              <Cpu className="w-3.5 h-3.5 text-emerald-400" />
              <span>Agents:</span>
            </div>
            
            <span className="inline-flex items-center px-2 py-0.5 rounded-md bg-emerald-950/60 text-emerald-300 border border-emerald-800/60 font-mono">
              <span className={`w-1.5 h-1.5 rounded-full bg-emerald-400 mr-1.5 ${isOptimizing ? 'animate-ping' : ''}`} />
              Farmer
            </span>
            <span className="inline-flex items-center px-2 py-0.5 rounded-md bg-sky-950/60 text-sky-300 border border-sky-800/60 font-mono">
              <span className={`w-1.5 h-1.5 rounded-full bg-sky-400 mr-1.5 ${isOptimizing ? 'animate-ping' : ''}`} />
              Market
            </span>
            <span className="inline-flex items-center px-2 py-0.5 rounded-md bg-amber-950/60 text-amber-300 border border-amber-800/60 font-mono">
              <span className={`w-1.5 h-1.5 rounded-full bg-amber-400 mr-1.5 ${isOptimizing ? 'animate-ping' : ''}`} />
              Logistics
            </span>
            <span className="inline-flex items-center px-2 py-0.5 rounded-md bg-purple-950/60 text-purple-300 border border-purple-800/60 font-mono">
              <span className={`w-1.5 h-1.5 rounded-full bg-purple-400 mr-1.5 ${isOptimizing ? 'animate-ping' : ''}`} />
              Consensus
            </span>
          </div>

          {/* SDG 2 Badge & Provenance Button */}
          <div className="flex items-center space-x-2 sm:space-x-3">
            <div className="hidden md:flex items-center px-2.5 py-1 rounded-lg bg-amber-500/15 border border-amber-500/30 text-amber-300 text-xs font-semibold">
              <span className="w-2 h-2 rounded-full bg-amber-400 mr-1.5 animate-pulse" />
              SDG 2: Zero Hunger
            </div>

            <button
              onClick={onOpenProvenance}
              className="inline-flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-medium border border-slate-700 transition shadow-sm"
              title="View FAOSTAT primary data citations and model transparency"
            >
              <Info className="w-3.5 h-3.5 text-emerald-400" />
              <span>Data Provenance</span>
            </button>
          </div>

        </div>
      </div>
    </header>
  );
}

