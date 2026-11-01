import React from 'react';
import { Layers, ArrowUpRight, TrendingUp, ShieldAlert, Award } from 'lucide-react';

export default function MarketComparisonTable({ recommendedPlan, alternativePlans }) {
  const allPlans = [recommendedPlan, ...(alternativePlans || [])].filter(Boolean);

  if (allPlans.length === 0) return null;

  return (
    <div className="bg-white rounded-2xl p-5 sm:p-6 border border-slate-200 shadow-sm">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-4 mb-4 border-b border-slate-100 gap-2">
        <div className="flex items-center space-x-2.5">
          <div className="p-2 rounded-xl bg-sky-100 text-sky-700">
            <Layers className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-base font-bold text-slate-900">Alternative Market & Timing Comparisons</h2>
            <p className="text-xs text-slate-500">Cross-market arbitrage and multi-criteria ranked options</p>
          </div>
        </div>

        <span className="text-xs font-medium text-slate-500 self-start sm:self-auto">
          Showing top {allPlans.length} evaluated permutations
        </span>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-left text-xs border-collapse">
          <thead>
            <tr className="bg-slate-50/80 border-b border-slate-200 text-slate-600 font-semibold">
              <th className="py-3 px-3">Rank</th>
              <th className="py-3 px-3">Market Destination</th>
              <th className="py-3 px-3">Timing</th>
              <th className="py-3 px-3">Distance / Transit</th>
              <th className="py-3 px-3">Price / Quintal</th>
              <th className="py-3 px-3">Transport Fees</th>
              <th className="py-3 px-3">Total Spoilage</th>
              <th className="py-3 px-3 text-right">Expected Net Profit</th>
              <th className="py-3 px-3 text-right">Profit Lift</th>
              <th className="py-3 px-3 text-center">Score</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {allPlans.map((plan, index) => {
              const isWinner = plan.rank === 1;
              const isLiftPositive = plan.profit_lift_vs_local_today > 0;

              return (
                <tr 
                  key={index}
                  className={`hover:bg-slate-50/90 transition ${
                    isWinner ? 'bg-emerald-50/50 font-medium' : ''
                  }`}
                >
                  {/* Rank */}
                  <td className="py-3 px-3 whitespace-nowrap">
                    {isWinner ? (
                      <span className="inline-flex items-center px-2 py-0.5 rounded-full text-[11px] font-extrabold bg-emerald-600 text-white shadow-sm">
                        #1 Optimal
                      </span>
                    ) : (
                      <span className="text-slate-500 font-bold px-2">
                        #{plan.rank}
                      </span>
                    )}
                  </td>

                  {/* Market */}
                  <td className="py-3 px-3 whitespace-nowrap">
                    <div className="font-bold text-slate-900">{plan.market_name}</div>
                    <div className="text-[10px] text-slate-500">{plan.market_type}</div>
                  </td>

                  {/* Timing */}
                  <td className="py-3 px-3 whitespace-nowrap">
                    <span className={`inline-block px-2 py-0.5 rounded font-semibold ${
                      plan.sell_day === 0 
                        ? 'bg-slate-100 text-slate-700' 
                        : 'bg-emerald-100/70 text-emerald-800'
                    }`}>
                      {plan.sell_day === 0 ? 'Today' : `Day +${plan.sell_day}`}
                    </span>
                    <div className="text-[10px] text-slate-400 mt-0.5">{plan.sell_date}</div>
                  </td>

                  {/* Distance */}
                  <td className="py-3 px-3 whitespace-nowrap text-slate-600">
                    <div>{plan.distance_km} km</div>
                    <div className="text-[10px] text-slate-400">{plan.transit_hours} hrs • {plan.vehicle_name?.split('(')[0]}</div>
                  </td>

                  {/* Price */}
                  <td className="py-3 px-3 whitespace-nowrap font-mono font-semibold text-slate-800">
                    ₹{plan.effective_market_price_per_q.toLocaleString()}
                  </td>

                  {/* Transport */}
                  <td className="py-3 px-3 whitespace-nowrap font-mono text-slate-600">
                    ₹{(plan.transport_cost + plan.market_cess_fees).toLocaleString()}
                  </td>

                  {/* Spoilage */}
                  <td className="py-3 px-3 whitespace-nowrap">
                    <span className={`font-mono font-semibold ${
                      plan.total_spoilage_loss_pct > 12 
                        ? 'text-rose-600' 
                        : plan.total_spoilage_loss_pct > 6 
                        ? 'text-amber-600' 
                        : 'text-emerald-700'
                    }`}>
                      {plan.total_spoilage_loss_pct}%
                    </span>
                    <span className="text-[10px] text-slate-400 block">
                      ({plan.spoilage_loss_kg} kg loss)
                    </span>
                  </td>

                  {/* Net Profit */}
                  <td className="py-3 px-3 whitespace-nowrap text-right font-mono font-bold text-slate-900">
                    <span className={isWinner ? 'text-emerald-700 font-extrabold text-sm' : ''}>
                      ₹{plan.net_profit.toLocaleString()}
                    </span>
                    <div className="text-[10px] text-slate-400 font-sans">
                      {plan.net_profit_margin_pct}% margin
                    </div>
                  </td>

                  {/* Profit Lift */}
                  <td className="py-3 px-3 whitespace-nowrap text-right font-mono font-semibold">
                    <span className={isLiftPositive ? 'text-emerald-600' : 'text-slate-400'}>
                      {isLiftPositive ? `+₹${plan.profit_lift_vs_local_today.toLocaleString()}` : '₹0'}
                    </span>
                  </td>

                  {/* Utility Score */}
                  <td className="py-3 px-3 whitespace-nowrap text-center">
                    <span className={`inline-block px-2 py-0.5 rounded font-mono font-bold text-[11px] ${
                      isWinner 
                        ? 'bg-emerald-100 text-emerald-800 border border-emerald-300' 
                        : 'bg-slate-100 text-slate-700'
                    }`}>
                      {plan.utility_score}
                    </span>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}

