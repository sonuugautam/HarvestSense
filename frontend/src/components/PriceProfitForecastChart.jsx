import React from 'react';
import { 
  ResponsiveContainer, ComposedChart, Line, Area, 
  XAxis, YAxis, Tooltip, Legend, CartesianGrid, ReferenceLine 
} from 'recharts';
import { LineChart as ChartIcon, TrendingUp, Calendar, AlertCircle } from 'lucide-react';

export default function PriceProfitForecastChart({ timeline, cropInfo }) {
  if (!timeline || timeline.length === 0) return null;

  // Format data for Recharts
  const chartData = timeline.map((pt) => ({
    dayLabel: pt.day === 0 ? 'Today' : `Day +${pt.day}`,
    fullDate: pt.date,
    faostatBaseline: pt.faostat_baseline_price,
    marketPrice: pt.best_market_projected_price,
    netProfit: pt.best_market_net_profit,
    storageLossPct: pt.cumulative_storage_loss_pct,
    viableQuintals: pt.viable_quantity_quintals,
    marketName: pt.best_market_name
  }));

  // Identify peak profit day
  const peakPoint = chartData.reduce((prev, current) => 
    (prev.netProfit > current.netProfit) ? prev : current, chartData[0]
  );

  return (
    <div className="bg-white rounded-2xl p-5 sm:p-6 border border-slate-200 shadow-sm">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-4 mb-4 border-b border-slate-100 gap-2">
        <div className="flex items-center space-x-2.5">
          <div className="p-2 rounded-xl bg-emerald-100 text-emerald-700">
            <ChartIcon className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-base font-bold text-slate-900">Price & Net Profit Forecast Horizon</h2>
            <p className="text-xs text-slate-500">Evaluating temporal market price momentum against physical spoilage decay</p>
          </div>
        </div>

        <div className="flex items-center space-x-2 text-xs bg-emerald-50 px-3 py-1.5 rounded-xl border border-emerald-200">
          <TrendingUp className="w-4 h-4 text-emerald-700" />
          <span className="font-semibold text-emerald-900">
            Peak Profit Horizon: <span className="font-bold underline">{peakPoint.dayLabel} ({peakPoint.fullDate})</span>
          </span>
        </div>
      </div>

      {/* Chart */}
      <div className="h-72 w-full mt-2">
        <ResponsiveContainer width="100%" height="100%">
          <ComposedChart data={chartData} margin={{ top: 10, right: 20, left: 0, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" vertical={false} />
            <XAxis 
              dataKey="dayLabel" 
              tick={{ fontSize: 11, fill: '#64748b' }} 
              axisLine={{ stroke: '#cbd5e1' }}
            />
            <YAxis 
              yAxisId="left" 
              tick={{ fontSize: 11, fill: '#64748b' }} 
              axisLine={{ stroke: '#cbd5e1' }}
              tickFormatter={(v) => `₹${(v / 1000).toFixed(0)}k`}
            />
            <YAxis 
              yAxisId="right" 
              orientation="right" 
              tick={{ fontSize: 11, fill: '#ef4444' }} 
              axisLine={{ stroke: '#fca5a5' }}
              domain={[0, 'dataMax + 10']}
              tickFormatter={(v) => `${v}%`}
            />
            <Tooltip 
              content={({ active, payload }) => {
                if (!active || !payload || !payload.length) return null;
                const d = payload[0].payload;
                return (
                  <div className="bg-slate-900 text-white p-3 rounded-xl shadow-xl text-xs space-y-1.5 border border-slate-700">
                    <div className="font-bold text-slate-200 border-b border-slate-700 pb-1 flex justify-between">
                      <span>{d.dayLabel} ({d.fullDate})</span>
                      <span className="text-emerald-400">{d.marketName}</span>
                    </div>
                    <div className="flex justify-between text-slate-300">
                      <span>Expected Net Profit:</span>
                      <span className="font-mono font-bold text-emerald-400">₹{d.netProfit.toLocaleString()}</span>
                    </div>
                    <div className="flex justify-between text-slate-300">
                      <span>Market Selling Price:</span>
                      <span className="font-mono text-sky-300">₹{d.marketPrice.toLocaleString()}/q</span>
                    </div>
                    <div className="flex justify-between text-slate-300">
                      <span>FAOSTAT Baseline:</span>
                      <span className="font-mono text-slate-400">₹{d.faostatBaseline.toLocaleString()}/q</span>
                    </div>
                    <div className="flex justify-between text-slate-300 border-t border-slate-700 pt-1">
                      <span>Cumulative Spoilage:</span>
                      <span className="font-mono text-rose-400 font-bold">{d.storageLossPct}%</span>
                    </div>
                    <div className="flex justify-between text-slate-400 text-[10px]">
                      <span>Remaining Viable Crop:</span>
                      <span>{d.viableQuintals} quintals</span>
                    </div>
                  </div>
                );
              }}
            />
            <Legend 
              wrapperStyle={{ fontSize: 11, paddingTop: 10 }}
              formatter={(value) => {
                if (value === 'netProfit') return 'Expected Net Profit (₹)';
                if (value === 'marketPrice') return 'Market Price (₹/q)';
                if (value === 'faostatBaseline') return 'FAOSTAT Baseline Anchor (₹/q)';
                if (value === 'storageLossPct') return 'Cumulative Spoilage Loss (%)';
                return value;
              }}
            />
            
            <Area 
              yAxisId="left" 
              type="monotone" 
              dataKey="netProfit" 
              fill="#10b981" 
              fillOpacity={0.15} 
              stroke="#059669" 
              strokeWidth={3} 
            />
            <Line 
              yAxisId="left" 
              type="monotone" 
              dataKey="marketPrice" 
              stroke="#0284c7" 
              strokeWidth={2} 
              dot={{ r: 3 }} 
            />
            <Line 
              yAxisId="left" 
              type="monotone" 
              dataKey="faostatBaseline" 
              stroke="#94a3b8" 
              strokeDasharray="4 4" 
              strokeWidth={1.5} 
              dot={false} 
            />
            <Line 
              yAxisId="right" 
              type="monotone" 
              dataKey="storageLossPct" 
              stroke="#ef4444" 
              strokeWidth={2} 
              dot={{ r: 3 }} 
            />
          </ComposedChart>
        </ResponsiveContainer>
      </div>

      <div className="mt-3 p-3 rounded-xl bg-slate-50 border border-slate-200/80 text-xs text-slate-600 flex items-start space-x-2">
        <AlertCircle className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
        <p>
          <strong className="text-slate-800">Dynamic Inversion Warning:</strong> While market prices may trend upwards over time, perishable crops suffer cumulative physiological respiration loss. The net profit curve peaks at <span className="font-bold text-emerald-800">{peakPoint.dayLabel}</span> before spoilage decay erodes revenues faster than price increases.
        </p>
      </div>
    </div>
  );
}

