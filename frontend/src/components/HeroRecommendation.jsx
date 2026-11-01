import React from 'react';
import { 
  CheckCircle2, TrendingUp, Truck, ShieldAlert, Award, 
  ArrowRight, DollarSign, Calendar, MapPin, Scale, ChevronRight 
} from 'lucide-react';

export default function HeroRecommendation({ plan, farmerProfile, cropInfo }) {
  if (!plan) return null;

  const isLiftPositive = plan.profit_lift_vs_local_today > 0;

  return (
    <div className="bg-gradient-to-br from-emerald-900 via-slate-900 to-slate-950 rounded-3xl p-6 sm:p-8 text-white shadow-xl border border-emerald-500/30 relative overflow-hidden">
      
      {/* Decorative Glow */}
      <div className="absolute top-0 right-0 -mr-20 -mt-20 w-80 h-80 bg-emerald-500/10 rounded-full blur-3xl pointer-events-none" />
      <div className="absolute bottom-0 left-0 -ml-20 -mb-20 w-80 h-80 bg-teal-500/10 rounded-full blur-3xl pointer-events-none" />

      {/* Top Header Badge */}
      <div className="relative z-10 flex flex-wrap items-center justify-between gap-3 pb-6 border-b border-slate-800">
        <div className="flex items-center space-x-2.5">
          <span className="flex h-3 w-3 relative">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
            <span className="relative inline-flex rounded-full h-3 w-3 bg-emerald-500"></span>
          </span>
          <span className="text-xs font-bold uppercase tracking-wider text-emerald-400 bg-emerald-950/80 px-3 py-1 rounded-full border border-emerald-500/30">
            Recommended Sell Plan • Rank #1
          </span>
        </div>

        <div className="flex items-center space-x-2 text-xs font-medium text-slate-300">
          <Award className="w-4 h-4 text-amber-400" />
          <span>Multi-Agent Utility Score:</span>
          <span className="text-emerald-400 font-bold text-sm bg-slate-800/80 px-2 py-0.5 rounded border border-slate-700">
            {plan.utility_score}/100
          </span>
        </div>
      </div>

      {/* Core Recommendation Grid */}
      <div className="relative z-10 grid grid-cols-1 lg:grid-cols-12 gap-6 mt-6">
        
        {/* Left Col: Target Market & Date */}
        <div className="lg:col-span-7 space-y-4">
          <div>
            <span className="text-xs font-medium text-emerald-300/80 uppercase tracking-wider">
              Optimal Market Destination
            </span>
            <h1 className="text-2xl sm:text-3xl font-black text-white tracking-tight mt-1 flex items-center space-x-2">
              <span>{plan.market_name}</span>
            </h1>
            <div className="flex flex-wrap items-center gap-2 mt-2 text-xs text-slate-300">
              <span className="px-2.5 py-1 rounded-md bg-slate-800/90 border border-slate-700 flex items-center space-x-1">
                <MapPin className="w-3.5 h-3.5 text-emerald-400" />
                <span>{plan.distance_km} km ({plan.transit_hours} hrs transit)</span>
              </span>
              <span className="px-2.5 py-1 rounded-md bg-slate-800/90 border border-slate-700">
                {plan.market_type}
              </span>
            </div>
          </div>

          {/* Sell Date & Timing Callout */}
          <div className="p-4 rounded-2xl bg-emerald-950/40 border border-emerald-500/30 flex items-start space-x-3.5">
            <div className="p-2 rounded-xl bg-emerald-500/20 text-emerald-300 shrink-0">
              <Calendar className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <h2 className="text-sm font-bold text-white">
                  Sell Date: {plan.sell_date}
                </h2>
                <span className="text-xs px-2 py-0.5 rounded font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
                  {plan.sell_day === 0 ? 'Today (Day 0)' : `Day +${plan.sell_day}`}
                </span>
              </div>
              <p className="text-xs text-slate-300 mt-1 leading-relaxed">
                {plan.sell_day === 0 
                  ? 'Immediate dispatch captures current high buyer demand and zero holding degradation.' 
                  : `Holding for ${plan.sell_day} days aligns arrival with peak wholesale bidding cycle, outpacing storage decay.`}
              </p>
            </div>
          </div>

          {/* Logistics Vehicle Selection */}
          <div className="p-4 rounded-2xl bg-slate-800/50 border border-slate-700/80 flex items-center justify-between text-xs">
            <div className="flex items-center space-x-3">
              <div className="p-2 rounded-xl bg-sky-500/20 text-sky-300 shrink-0">
                <Truck className="w-5 h-5" />
              </div>
              <div>
                <p className="font-semibold text-slate-200">Recommended Vehicle Fleet</p>
                <p className="text-slate-400">{plan.vehicle_name}</p>
              </div>
            </div>
            <div className="text-right">
              <span className="font-mono text-emerald-400 font-bold">₹{plan.transport_cost.toLocaleString()}</span>
              <p className="text-[10px] text-slate-400">Total Freight</p>
            </div>
          </div>

        </div>

        {/* Right Col: Profit & Financial Breakdown Card */}
        <div className="lg:col-span-5 flex flex-col justify-between bg-slate-950/70 p-6 rounded-2xl border border-emerald-500/20">
          
          <div>
            <div className="flex items-center justify-between text-xs text-slate-400">
              <span>Expected Net Profit</span>
              <span className="text-emerald-400 font-medium">{plan.net_profit_margin_pct}% net margin</span>
            </div>
            
            <div className="mt-2 flex items-baseline space-x-2">
              <span className="text-3xl sm:text-4xl font-black text-emerald-400 font-mono tracking-tight">
                ₹{plan.net_profit.toLocaleString()}
              </span>
            </div>

            {/* Profit Lift Callout */}
            <div className={`mt-3 p-2.5 rounded-xl text-xs font-semibold flex items-center space-x-2 ${
              isLiftPositive 
                ? 'bg-emerald-500/20 text-emerald-200 border border-emerald-500/30' 
                : 'bg-slate-800 text-slate-300'
            }`}>
              <TrendingUp className="w-4 h-4 text-emerald-400 shrink-0" />
              <span>
                {isLiftPositive ? `+₹${plan.profit_lift_vs_local_today.toLocaleString()} Extra Profit` : 'Standard Baseline'}
              </span>
              <span className="text-[11px] font-normal text-slate-300">
                vs local taluka distress sale
              </span>
            </div>
          </div>

          {/* Financial Breakdown Table */}
          <div className="mt-5 pt-4 border-t border-slate-800 space-y-2 text-xs">
            <div className="flex justify-between text-slate-300">
              <span className="text-slate-400">Delivered Quantity:</span>
              <span className="font-mono font-medium">{plan.delivered_sellable_quintals} q ({(plan.delivered_sellable_quintals * 100).toFixed(0)} kg)</span>
            </div>
            <div className="flex justify-between text-slate-300">
              <span className="text-slate-400">Wholesale Price:</span>
              <span className="font-mono font-medium text-emerald-300">₹{plan.effective_market_price_per_q.toLocaleString()}/q</span>
            </div>
            <div className="flex justify-between text-slate-300">
              <span className="text-slate-400">Gross Expected Revenue:</span>
              <span className="font-mono font-medium">₹{plan.gross_revenue.toLocaleString()}</span>
            </div>
            <div className="flex justify-between text-slate-300">
              <span className="text-slate-400">Transport & Handling:</span>
              <span className="font-mono font-medium text-rose-300">-₹{plan.transport_cost.toLocaleString()}</span>
            </div>
            <div className="flex justify-between text-slate-300">
              <span className="text-slate-400">Mandi Cess / Market Taxes:</span>
              <span className="font-mono font-medium text-rose-300">-₹{plan.market_cess_fees.toLocaleString()}</span>
            </div>
            {plan.storage_cost > 0 && (
              <div className="flex justify-between text-slate-300">
                <span className="text-slate-400">Storage Holding Fees:</span>
                <span className="font-mono font-medium text-rose-300">-₹{plan.storage_cost.toLocaleString()}</span>
              </div>
            )}
          </div>

          {/* Spoilage Meter */}
          <div className="mt-5 pt-4 border-t border-slate-800">
            <div className="flex justify-between items-center text-xs mb-1.5">
              <span className="text-slate-400 flex items-center space-x-1">
                <ShieldAlert className="w-3.5 h-3.5 text-amber-400" />
                <span>Total Post-Harvest Spoilage:</span>
              </span>
              <span className={`font-mono font-bold ${
                plan.total_spoilage_loss_pct < 5 ? 'text-emerald-400' : 'text-amber-400'
              }`}>
                {plan.total_spoilage_loss_pct}% ({plan.spoilage_loss_kg} kg loss)
              </span>
            </div>
            
            <div className="w-full bg-slate-800 h-2 rounded-full overflow-hidden flex">
              <div 
                className="bg-amber-400 h-full transition-all duration-500" 
                style={{ width: `${Math.min(100, plan.storage_spoilage_loss_pct * 3)}%` }}
                title={`Storage loss: ${plan.storage_spoilage_loss_pct}%`}
              />
              <div 
                className="bg-rose-500 h-full transition-all duration-500" 
                style={{ width: `${Math.min(100, plan.transit_spoilage_loss_pct * 3)}%` }}
                title={`Transit loss: ${plan.transit_spoilage_loss_pct}%`}
              />
            </div>
            <div className="flex justify-between text-[10px] text-slate-500 mt-1">
              <span>Storage loss: {plan.storage_spoilage_loss_pct}%</span>
              <span>Transit loss: {plan.transit_spoilage_loss_pct}%</span>
            </div>
          </div>

        </div>

      </div>

      {/* Transparent Multi-Agent Consensus Reason */}
      <div className="relative z-10 mt-6 pt-5 border-t border-slate-800 flex items-start space-x-3 text-xs text-slate-300 bg-slate-900/60 p-4 rounded-xl border border-slate-800">
        <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
        <div>
          <span className="font-bold text-white mr-1.5">Consensus Verdict:</span>
          <span>{plan.recommendation_verdict}.</span>
          <span className="text-slate-400 ml-1">
            Produce arrives in <strong className="text-slate-200">{plan.quality_grade_at_sale}</strong> condition.
            The wholesale auction spread at {plan.market_name} exceeds transport fees by ₹{plan.profit_lift_vs_local_today.toLocaleString()}, maximizing smallholder disposable income.
          </span>
        </div>
      </div>

    </div>
  );
}

