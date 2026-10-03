import React from 'react';
import { 
  BarChart3, Calendar, Users, Compass, 
  Megaphone, ShieldCheck, CheckCircle2, Clock 
} from 'lucide-react';

const AGENT_METADATA = [
  {
    id: "comps",
    name: "Market & Comps Agent",
    icon: BarChart3,
    role: "Benchmarks historical titles, box office scale, and genre lessons",
    color: "text-blue-400 border-blue-500/30 bg-blue-950/20"
  },
  {
    id: "calendar",
    name: "Calendar & Clash Agent",
    icon: Calendar,
    role: "Calculates festival multipliers, IPL overlap, and screen clash risk",
    color: "text-emerald-400 border-emerald-500/30 bg-emerald-950/20"
  },
  {
    id: "audience",
    name: "Audience & Sentiment Agent",
    icon: Users,
    role: "Profiles multiplex vs single-screen split and sentiment hooks",
    color: "text-purple-400 border-purple-500/30 bg-purple-950/20"
  },
  {
    id: "strategy",
    name: "Strategy & Distribution Agent",
    icon: Compass,
    role: "Ranks release corridors and enforces 8-week MAI OTT holdback",
    color: "text-amber-400 border-amber-500/30 bg-amber-950/20"
  },
  {
    id: "marketing",
    name: "30/60/90 Playbook Agent",
    icon: Megaphone,
    role: "Builds phased asset drop calendar: Teasers, Songs, Trailer & Tours",
    color: "text-rose-400 border-rose-500/30 bg-rose-950/20"
  },
  {
    id: "critic",
    name: "Executive Critic & Verifier",
    icon: ShieldCheck,
    role: "Audits claims against ground truth, flags inferences & halts hallucinations",
    color: "text-teal-400 border-teal-500/30 bg-teal-950/20"
  }
];

export default function AgentProgressTracker({ logs = [], isRunning = false }) {
  return (
    <div className="bg-studio-800/90 border border-studio-700 rounded-2xl p-6 shadow-xl mb-8">
      <div className="flex items-center justify-between mb-5 pb-4 border-b border-studio-700/70">
        <div className="flex items-center space-x-2">
          <div className="w-2.5 h-2.5 rounded-full bg-studio-accent animate-ping" />
          <h3 className="font-display font-bold text-sm tracking-wide text-white uppercase">
            Autonomous Multi-Agent Pipeline Status
          </h3>
        </div>
        <div className="text-xs text-slate-400 flex items-center space-x-1.5">
          <Clock className="w-3.5 h-3.5 text-slate-500" />
          <span>Sequencing 6 Specialized Agents</span>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {AGENT_METADATA.map((agent, index) => {
          const Icon = agent.icon;
          const matchingLog = logs.find(l => l.agent.toLowerCase().includes(agent.name.toLowerCase().split(' ')[0]));
          const isDone = !!matchingLog || !isRunning;

          return (
            <div 
              key={agent.id}
              className={`p-4 rounded-xl border transition-all ${
                isDone 
                  ? 'bg-studio-900/80 border-studio-700' 
                  : isRunning && index === logs.length
                  ? 'bg-studio-accent/10 border-studio-accent animate-pulse'
                  : 'bg-studio-900/40 border-studio-800 opacity-60'
              }`}
            >
              <div className="flex items-start justify-between mb-2">
                <div className="flex items-center space-x-2.5">
                  <div className={`p-2 rounded-lg border ${agent.color}`}>
                    <Icon className="w-4 h-4" />
                  </div>
                  <div>
                    <h4 className="font-bold text-xs text-white leading-tight">{agent.name}</h4>
                    <span className="text-[10px] text-slate-400">Agent {index + 1} of 6</span>
                  </div>
                </div>

                {isDone ? (
                  <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
                ) : isRunning && index === logs.length ? (
                  <div className="w-4 h-4 border-2 border-studio-accent border-t-transparent rounded-full animate-spin shrink-0" />
                ) : (
                  <div className="w-2 h-2 rounded-full bg-slate-700 shrink-0" />
                )}
              </div>

              <p className="text-[11px] text-slate-400 mt-2 leading-relaxed">
                {matchingLog ? matchingLog.message : agent.role}
              </p>

              {matchingLog && (
                <div className="mt-2.5 pt-2 border-t border-studio-800 text-[10px] text-slate-500 flex justify-between">
                  <span>Latency: {matchingLog.elapsed_seconds}s</span>
                  <span className="text-emerald-400 font-medium">Audited Output</span>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
