import React, { useState } from 'react';
import { 
  Bot, UserCheck, TrendingUp, Truck, CheckCircle2, 
  AlertTriangle, Info, ChevronDown, ChevronUp, Terminal 
} from 'lucide-react';

export default function AgentDeliberationFeed({ logs }) {
  const [selectedAgent, setSelectedAgent] = useState('ALL');
  const [expandedIndices, setExpandedIndices] = useState({});

  if (!logs || logs.length === 0) return null;

  const toggleExpand = (index) => {
    setExpandedIndices(prev => ({
      ...prev,
      [index]: !prev[index]
    }));
  };

  const filteredLogs = selectedAgent === 'ALL' 
    ? logs 
    : logs.filter(l => l.agent.toLowerCase().includes(selectedAgent.toLowerCase()));

  const getAgentTheme = (agent) => {
    if (agent.includes('Farmer')) {
      return {
        icon: UserCheck,
        badgeBg: 'bg-emerald-100 text-emerald-800 border-emerald-300',
        dotBg: 'bg-emerald-500',
        ringColor: 'ring-emerald-400'
      };
    }
    if (agent.includes('Market')) {
      return {
        icon: TrendingUp,
        badgeBg: 'bg-sky-100 text-sky-800 border-sky-300',
        dotBg: 'bg-sky-500',
        ringColor: 'ring-sky-400'
      };
    }
    if (agent.includes('Logistics')) {
      return {
        icon: Truck,
        badgeBg: 'bg-amber-100 text-amber-800 border-amber-300',
        dotBg: 'bg-amber-500',
        ringColor: 'ring-amber-400'
      };
    }
    return {
      icon: Bot,
      badgeBg: 'bg-purple-100 text-purple-800 border-purple-300',
      dotBg: 'bg-purple-500',
      ringColor: 'ring-purple-400'
    };
  };

  return (
    <div className="bg-white rounded-2xl p-5 sm:p-6 border border-slate-200 shadow-sm">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-4 mb-4 border-b border-slate-100 gap-3">
        <div className="flex items-center space-x-2.5">
          <div className="p-2 rounded-xl bg-purple-100 text-purple-700">
            <Terminal className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-base font-bold text-slate-900">Multi-Agent Deliberation Logs</h2>
            <p className="text-xs text-slate-500">Transparent collaborative decision trace & consensus exchange</p>
          </div>
        </div>

        {/* Filter Pills */}
        <div className="flex flex-wrap items-center gap-1.5 text-xs">
          {['ALL', 'Farmer', 'Market', 'Logistics', 'Coordinator'].map((agentName) => (
            <button
              key={agentName}
              onClick={() => setSelectedAgent(agentName)}
              className={`px-2.5 py-1 rounded-lg font-medium transition cursor-pointer ${
                selectedAgent === agentName
                  ? 'bg-slate-900 text-white shadow-sm'
                  : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
              }`}
            >
              {agentName}
            </button>
          ))}
        </div>
      </div>

      {/* Logs Feed */}
      <div className="space-y-3 max-h-[460px] overflow-y-auto pr-1">
        {filteredLogs.map((log, index) => {
          const theme = getAgentTheme(log.agent);
          const AgentIcon = theme.icon;
          const isExpanded = !!expandedIndices[index];
          const isConsensus = log.badge_type === 'consensus';

          return (
            <div 
              key={index} 
              className={`p-3.5 rounded-xl border text-xs transition ${
                isConsensus 
                  ? 'bg-gradient-to-r from-purple-50 via-emerald-50 to-teal-50 border-purple-300 shadow-sm' 
                  : 'bg-slate-50/70 border-slate-200 hover:border-slate-300'
              }`}
            >
              <div className="flex items-start justify-between gap-2">
                <div className="flex items-center space-x-2">
                  <span className={`inline-flex items-center px-2 py-0.5 rounded-md border text-[11px] font-bold ${theme.badgeBg}`}>
                    <AgentIcon className="w-3 h-3 mr-1" />
                    {log.agent}
                  </span>
                  <span className="text-[11px] font-semibold text-slate-500 uppercase tracking-wider">
                    {log.phase}
                  </span>
                </div>

                {log.detail && (
                  <button
                    onClick={() => toggleExpand(index)}
                    className="text-slate-400 hover:text-slate-700 flex items-center space-x-0.5 text-[11px]"
                  >
                    <span>{isExpanded ? 'Hide data' : 'View data'}</span>
                    {isExpanded ? <ChevronUp className="w-3 h-3" /> : <ChevronDown className="w-3 h-3" />}
                  </button>
                )}
              </div>

              {/* Message */}
              <p className={`mt-2 font-medium leading-relaxed ${isConsensus ? 'text-purple-950 font-bold' : 'text-slate-800'}`}>
                {log.message}
              </p>

              {/* Collapsible raw data snapshot */}
              {isExpanded && log.detail && (
                <div className="mt-2.5 p-2.5 rounded-lg bg-slate-900 text-slate-200 font-mono text-[11px] overflow-x-auto">
                  <div className="text-slate-400 text-[10px] mb-1 font-sans">
                    Agent Internal Snapshot:
                  </div>
                  <pre>{JSON.stringify(log.detail, null, 2)}</pre>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}

