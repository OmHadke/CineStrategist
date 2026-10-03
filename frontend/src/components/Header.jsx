import React from 'react';
import { Film, ShieldCheck, Sparkles, Database, Calendar } from 'lucide-react';

export default function Header({ systemHealth, onSelectPreset }) {
  return (
    <header className="border-b border-studio-700 bg-studio-900/90 backdrop-blur sticky top-0 z-50 no-print">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        
        {/* Brand */}
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-studio-accent to-red-700 flex items-center justify-center shadow-lg shadow-red-950/50">
            <Film className="w-5 h-5 text-white" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <span className="font-display font-bold text-xl tracking-tight text-white">CineStrategist</span>
              <span className="text-[10px] uppercase tracking-wider font-semibold px-2 py-0.5 rounded bg-studio-accent/20 text-studio-accent border border-studio-accent/30">
                Studio Edition
              </span>
            </div>
            <p className="text-xs text-slate-400">Multi-Agent Theatrical Release & Marketing Intelligence</p>
          </div>
        </div>

        {/* Live System Status Badges */}
        <div className="hidden md:flex items-center space-x-3 text-xs">
          <div className="flex items-center space-x-1.5 px-2.5 py-1 rounded-full bg-studio-800 border border-studio-700 text-slate-300">
            <Sparkles className="w-3.5 h-3.5 text-amber-400" />
            <span>AI: <strong className="text-white font-medium">{systemHealth?.llm_provider ? 'Active' : 'Offline Engine'}</strong></span>
          </div>

          <div className="flex items-center space-x-1.5 px-2.5 py-1 rounded-full bg-studio-800 border border-studio-700 text-slate-300">
            <Database className="w-3.5 h-3.5 text-blue-400" />
            <span>Curated Benchmarks: <strong className="text-white font-medium">{systemHealth?.total_curated_benchmarks || '10+'} Films</strong></span>
          </div>

          <div className="flex items-center space-x-1.5 px-2.5 py-1 rounded-full bg-studio-800 border border-studio-700 text-slate-300">
            <Calendar className="w-3.5 h-3.5 text-emerald-400" />
            <span>Festivals & Holidays: <strong className="text-white font-medium">{systemHealth?.total_festivals_tracked || '10+'} Tracked</strong></span>
          </div>

          <div className="flex items-center space-x-1.5 px-2.5 py-1 rounded-full bg-emerald-950/60 border border-emerald-800/60 text-emerald-300">
            <ShieldCheck className="w-3.5 h-3.5" />
            <span>Anti-Hallucination Critic Active</span>
          </div>
        </div>
      </div>
    </header>
  );
}
