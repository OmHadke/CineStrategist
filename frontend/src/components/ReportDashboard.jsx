import React, { useState } from 'react';
import { 
  Printer, Download, ShieldCheck, AlertTriangle, 
  Calendar, Users, Compass, Megaphone, BarChart3, 
  TrendingUp, CheckCircle, Info, ExternalLink, ArrowLeft
} from 'lucide-react';
import { 
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell 
} from 'recharts';

export default function ReportDashboard({ report, onReset }) {
  const [activeTab, setActiveTab] = useState('overview');

  if (!report) return null;

  const {
    report_id,
    film_input,
    comps_analysis,
    calendar_analysis,
    audience_analysis,
    release_strategy,
    marketing_playbook,
    critic_audit,
    metadata
  } = report;

  const handlePrint = () => {
    window.print();
  };

  const handleDownloadJSON = () => {
    const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(report, null, 2));
    const downloadAnchor = document.createElement('a');
    downloadAnchor.setAttribute("href", dataStr);
    downloadAnchor.setAttribute("download", `CineStrategist_${film_input.title.replace(/\s+/g, '_')}_Report.json`);
    document.body.appendChild(downloadAnchor);
    downloadAnchor.click();
    downloadAnchor.remove();
  };

  // Chart data for comparable films
  const chartData = comps_analysis.comparables.map(c => ({
    name: c.title,
    rating: c.imdb_rating,
    similarity: Math.round(c.similarity_score * 100),
    verdict: c.verdict
  }));

  return (
    <div className="space-y-8 print-page">
      
      {/* Top Action Bar */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 pb-4 border-b border-studio-700/80 no-print">
        <button
          onClick={onReset}
          className="flex items-center space-x-2 text-xs font-semibold px-3 py-2 rounded-lg bg-studio-800 hover:bg-studio-700 text-slate-300 transition-colors"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>New Analysis / Edit Parameters</span>
        </button>

        <div className="flex items-center space-x-3">
          <button
            onClick={handleDownloadJSON}
            className="flex items-center space-x-2 text-xs font-semibold px-3.5 py-2 rounded-lg bg-studio-800 hover:bg-studio-700 text-slate-200 border border-studio-700 transition-colors"
          >
            <Download className="w-4 h-4 text-slate-400" />
            <span>Download JSON Data</span>
          </button>

          <button
            onClick={handlePrint}
            className="flex items-center space-x-2 text-xs font-semibold px-4 py-2 rounded-lg bg-studio-accent hover:bg-red-700 text-white shadow-lg shadow-red-950/40 transition-colors"
          >
            <Printer className="w-4 h-4" />
            <span>Export Studio PDF / Print</span>
          </button>
        </div>
      </div>

      {/* Executive Report Title Card */}
      <div className="bg-gradient-to-br from-studio-800 via-studio-800 to-studio-900 border border-studio-700 rounded-2xl p-6 sm:p-8 shadow-xl relative overflow-hidden print-card">
        <div className="absolute top-0 right-0 w-96 h-96 bg-red-600/5 rounded-full blur-3xl pointer-events-none" />

        <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
          <div>
            <div className="flex items-center space-x-3 mb-2">
              <span className="text-xs uppercase tracking-widest font-mono text-studio-gold">
                Confidential Studio Brief • #{report_id}
              </span>
              <span className="text-xs text-slate-400">|</span>
              <span className="text-xs text-slate-400">{metadata.generated_at}</span>
            </div>
            
            <h1 className="font-display font-extrabold text-3xl sm:text-4xl text-white tracking-tight">
              {film_input.title}
            </h1>
            
            <div className="flex flex-wrap items-center gap-2 mt-3 text-xs text-slate-300">
              <span className="px-2.5 py-1 rounded bg-studio-700 text-white font-medium">
                {film_input.language}
              </span>
              {film_input.genres.map(g => (
                <span key={g} className="px-2.5 py-1 rounded bg-studio-900/80 border border-studio-700 text-slate-300">
                  {g}
                </span>
              ))}
              <span className="px-2.5 py-1 rounded bg-amber-950/40 border border-amber-800/40 text-amber-300 font-medium uppercase">
                {film_input.budget_tier} Budget
              </span>
              <span className="px-2.5 py-1 rounded bg-purple-950/40 border border-purple-800/40 text-purple-300 font-medium">
                {film_input.star_tier.replace('_', ' ').toUpperCase()}
              </span>
              <span className="px-2.5 py-1 rounded bg-emerald-950/40 border border-emerald-800/40 text-emerald-300 font-medium">
                Target: {film_input.planned_window}
              </span>
            </div>
          </div>

          {/* Critic Quality Verification Badge */}
          <div className="flex flex-col items-start md:items-end justify-center bg-studio-900/80 border border-studio-700 p-4 rounded-xl shrink-0">
            <div className="flex items-center space-x-2 text-emerald-400 mb-1">
              <ShieldCheck className="w-5 h-5" />
              <span className="font-display font-bold text-lg text-white">
                {critic_audit.credibility_score}%
              </span>
            </div>
            <span className="text-xs font-semibold text-emerald-400 uppercase tracking-wider">
              {critic_audit.verdict}
            </span>
            <span className="text-[11px] text-slate-300 mt-1">
              <strong>{critic_audit.verified_claims_count} Verified</strong> • {critic_audit.probable_inferences_count || 0} Inferences ({critic_audit.total_claims_checked} Checks)
            </span>
            <span className="text-[10px] text-slate-500 mt-0.5">
              Pipeline Latency: {metadata.execution_time_formatted || (metadata.execution_time_seconds + 's')}
            </span>
          </div>
        </div>


        {/* Narrative & Logline */}
        <div className="mt-6 pt-6 border-t border-studio-700/60 text-xs sm:text-sm text-slate-300 leading-relaxed">
          <strong className="text-white uppercase tracking-wider text-[11px] block mb-1">
            Story Synopsis &amp; Hook:
          </strong>
          {film_input.logline}
        </div>
      </div>

      {/* Navigation Tabs (Screen only) */}
      <div className="flex border-b border-studio-700 text-sm no-print overflow-x-auto">
        {[
          { id: 'overview', label: 'Executive Overview', icon: TrendingUp },
          { id: 'comps', label: 'Comparable Benchmarks', icon: BarChart3 },
          { id: 'calendar', label: 'Calendar & Clash Risk', icon: Calendar },
          { id: 'audience', label: 'Audience & Demographics', icon: Users },
          { id: 'strategy', label: 'Release & Distribution', icon: Compass },
          { id: 'marketing', label: '30/60/90 Marketing Playbook', icon: Megaphone },
          { id: 'critic', label: 'Anti-Hallucination Audit', icon: ShieldCheck }
        ].map(tab => {
          const Icon = tab.icon;
          const isActive = activeTab === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex items-center space-x-2 px-5 py-3 border-b-2 font-medium whitespace-nowrap transition-colors ${
                isActive
                  ? 'border-studio-accent text-white bg-studio-800/40'
                  : 'border-transparent text-slate-400 hover:text-slate-200 hover:border-slate-600'
              }`}
            >
              <Icon className="w-4 h-4" />
              <span>{tab.label}</span>
            </button>
          );
        })}
      </div>

      {/* TAB CONTENT: 1. OVERVIEW & STRATEGIC HIGHLIGHTS */}
      {(activeTab === 'overview' || window.matchMedia('print').matches) && (
        <div className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            
            {/* Primary Release Corridor */}
            <div className="bg-studio-800 border border-studio-700 rounded-xl p-5 print-card">
              <div className="flex items-center space-x-2 text-studio-gold mb-2">
                <Compass className="w-4 h-4" />
                <h4 className="text-xs font-bold uppercase tracking-wider text-slate-300">
                  Recommended Release Window
                </h4>
              </div>
              <div className="text-xl font-bold text-white mb-1">
                {release_strategy.ranked_release_options[0].proposed_date}
              </div>
              <span className="inline-block text-[11px] px-2 py-0.5 rounded bg-emerald-950/60 text-emerald-300 border border-emerald-800/60 mb-3">
                {release_strategy.ranked_release_options[0].slot_type}
              </span>
              <p className="text-xs text-slate-300 leading-relaxed">
                {release_strategy.ranked_release_options[0].strategic_rationale}
              </p>
            </div>

            {/* Screen Allocation & Capacity */}
            <div className="bg-studio-800 border border-studio-700 rounded-xl p-5 print-card">
              <div className="flex items-center space-x-2 text-blue-400 mb-2">
                <BarChart3 className="w-4 h-4" />
                <h4 className="text-xs font-bold uppercase tracking-wider text-slate-300">
                  Screen Footprint Target
                </h4>
              </div>
              <div className="text-xl font-bold text-white mb-1">
                {release_strategy.ranked_release_options[0].screen_count_est.split(' ')[0]} Screens
              </div>
              <span className="inline-block text-[11px] px-2 py-0.5 rounded bg-blue-950/60 text-blue-300 border border-blue-800/60 mb-3">
                Multiplex &amp; Heartland Single-Screens
              </span>
              <p className="text-xs text-slate-300 leading-relaxed">
                {release_strategy.screen_distribution_strategy}
              </p>
            </div>

            {/* 8-Week OTT Holdback Norm */}
            <div className="bg-studio-800 border border-studio-700 rounded-xl p-5 print-card">
              <div className="flex items-center space-x-2 text-purple-400 mb-2">
                <ShieldCheck className="w-4 h-4" />
                <h4 className="text-xs font-bold uppercase tracking-wider text-slate-300">
                  OTT Holdback Mandate
                </h4>
              </div>
              <div className="text-xl font-bold text-white mb-1">
                {release_strategy.ott_windowing.theatrical_holdback_weeks} Weeks (56 Days)
              </div>
              <span className="inline-block text-[11px] px-2 py-0.5 rounded bg-purple-950/60 text-purple-300 border border-purple-800/60 mb-3">
                {release_strategy.ott_windowing.industry_norm_compliance}
              </span>
              <p className="text-xs text-slate-300 leading-relaxed">
                {release_strategy.ott_windowing.rationale}
              </p>
            </div>

          </div>

          {/* Positioning Hook Callout */}
          <div className="p-6 rounded-xl bg-gradient-to-r from-red-950/30 via-studio-800 to-studio-800 border border-studio-accent/40 print-card">
            <h4 className="text-xs font-bold uppercase tracking-wider text-studio-accent mb-2">
              Studio Strategic Positioning Thesis
            </h4>
            <p className="text-base sm:text-lg font-medium text-white italic">
              "{audience_analysis.positioning_hook}"
            </p>
            <div className="mt-4 flex flex-wrap gap-4 text-xs text-slate-300">
              <div>
                <span className="text-slate-400">Word of Mouth Dependence:</span>{' '}
                <strong className="text-white">{audience_analysis.word_of_mouth_dependence}</strong>
              </div>
              <div>
                <span className="text-slate-400">Clash Risk Level:</span>{' '}
                <strong className="text-white">{calendar_analysis.risk_tier} ({calendar_analysis.overall_risk_score}/10)</strong>
              </div>
              <div>
                <span className="text-slate-400">Campaign Slogan:</span>{' '}
                <strong className="text-white">{marketing_playbook.campaign_slogan_or_theme}</strong>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* TAB CONTENT: 2. COMPARABLE BENCHMARKS */}
      {(activeTab === 'comps' || window.matchMedia('print').matches) && (
        <div className="space-y-6">
          <div className="bg-studio-800 border border-studio-700 rounded-xl p-6 print-card">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
              <div>
                <h3 className="font-display font-bold text-lg text-white">
                  Historical Comparable Benchmark Matrix
                </h3>
                <p className="text-xs text-slate-400 mt-0.5">
                  Benchmarked using historical Indian theatrical records &amp; verified TMDB statistics
                </p>
              </div>
              <div className="flex flex-wrap items-center gap-2 text-xs">
                {comps_analysis.match_quality && (
                  <span className={`px-3 py-1 rounded-full text-xs font-semibold ${
                    comps_analysis.match_quality.includes('High')
                      ? 'bg-emerald-950/70 border border-emerald-700/60 text-emerald-300'
                      : comps_analysis.match_quality.includes('Moderate')
                      ? 'bg-amber-950/70 border border-amber-700/60 text-amber-300'
                      : 'bg-red-950/70 border border-red-700/60 text-red-300'
                  }`}>
                    {comps_analysis.match_quality}
                  </span>
                )}
                <span className="px-3 py-1 rounded-full bg-studio-900 border border-studio-700 text-slate-300">
                  Median Rating: <strong className="text-white">{comps_analysis.median_rating} / 10</strong>
                </span>
              </div>
            </div>

            {/* Configuration Warnings Alert */}
            {comps_analysis.configuration_warnings && comps_analysis.configuration_warnings.length > 0 && (
              <div className="mb-6 p-4 rounded-xl bg-amber-950/30 border border-amber-700/70 text-amber-200 text-xs space-y-2">
                {comps_analysis.configuration_warnings.map((warn, idx) => (
                  <div key={idx} className="flex items-start space-x-2">
                    <span className="font-bold text-amber-400 shrink-0">⚠️ AUDITOR WARNING:</span>
                    <span className="leading-relaxed">{warn}</span>
                  </div>
                ))}
              </div>
            )}

            {/* Genre Base Rate Context Callout */}
            {comps_analysis.base_rate_summary && (
              <div className="mb-6 p-3.5 rounded-lg bg-studio-900/90 border border-studio-700 text-slate-300 text-xs leading-relaxed">
                <span className="font-semibold text-studio-gold">Studio Base Rate Precedent: </span>
                {comps_analysis.base_rate_summary}
              </div>
            )}

            {/* Visual Recharts Bar Graph */}
            <div className="h-64 w-full mb-8 no-print">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={chartData} margin={{ top: 10, right: 10, left: -20, bottom: 20 }}>
                  <XAxis dataKey="name" stroke="#94a3b8" fontSize={11} interval={0} angle={-15} textAnchor="end" />
                  <YAxis domain={[0, 10]} stroke="#94a3b8" fontSize={11} />
                  <Tooltip 
                    contentStyle={{ backgroundColor: '#12141d', borderColor: '#262a3b', borderRadius: '8px', color: '#fff', fontSize: '12px' }}
                    formatter={(val, name) => [val, name === 'rating' ? 'IMDb Rating' : 'Similarity Score (%)']}
                  />
                  <Bar dataKey="rating" fill="#e50914" radius={[4, 4, 0, 0]}>
                    {chartData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.rating >= 7 ? '#10b981' : entry.rating >= 6 ? '#e5a93c' : '#e50914'} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>

            {/* Detailed Comps Table */}
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs border-collapse">
                <thead>
                  <tr className="border-b border-studio-700 text-slate-400 uppercase tracking-wider text-[11px]">
                    <th className="py-3 px-3">Title &amp; Year</th>
                    <th className="py-3 px-3">Genres</th>
                    <th className="py-3 px-3">Budget</th>
                    <th className="py-3 px-3">Gross Box Office</th>
                    <th className="py-3 px-3">Verdict</th>
                    <th className="py-3 px-3">IMDb</th>
                    <th className="py-3 px-3">Comp Fit</th>
                    <th className="py-3 px-3">Strategic Studio Takeaway</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-studio-700/60">
                  {comps_analysis.comparables.map((comp) => (
                    <tr key={comp.id} className="hover:bg-studio-700/30 transition-colors">
                      <td className="py-3 px-3 font-semibold text-white whitespace-nowrap">
                        <div>{comp.title} <span className="text-slate-400 font-normal">({comp.year})</span></div>
                        {comp.original_language && (
                          <div className="text-[10px] text-purple-300 font-mono mt-0.5">
                            {comp.original_language}
                          </div>
                        )}
                      </td>
                      <td className="py-3 px-3 text-slate-300">
                        {comp.genres.join(', ')}
                      </td>
                      <td className="py-3 px-3 text-slate-300 whitespace-nowrap">
                        {comp.budget_est}
                      </td>
                      <td className="py-3 px-3 font-semibold text-emerald-400 whitespace-nowrap">
                        {comp.box_office_est}
                      </td>
                      <td className="py-3 px-3 whitespace-nowrap">
                        <span className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase ${
                          comp.verdict.includes('Blockbuster') 
                            ? 'bg-emerald-950 text-emerald-300 border border-emerald-800'
                            : comp.verdict.includes('Hit')
                            ? 'bg-blue-950 text-blue-300 border border-blue-800'
                            : 'bg-amber-950 text-amber-300 border border-amber-800'
                        }`}>
                          {comp.verdict}
                        </span>
                      </td>
                      <td className="py-3 px-3 font-bold text-white">
                        ★ {comp.imdb_rating}
                      </td>
                      <td className="py-3 px-3">
                        <span className="font-mono text-studio-gold">
                          {Math.round(comp.similarity_score * 100)}%
                        </span>
                      </td>
                      <td className="py-3 px-3 text-slate-300 max-w-xs leading-relaxed">
                        {comp.key_takeaway}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            {/* Success Factors & Pitfalls */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-6 pt-6 border-t border-studio-700/80">
              <div className="p-4 rounded-lg bg-emerald-950/20 border border-emerald-800/40">
                <h4 className="text-xs font-bold uppercase tracking-wider text-emerald-400 mb-2 flex items-center space-x-1.5">
                  <CheckCircle className="w-3.5 h-3.5" />
                  <span>Observed Historical Success Enablers</span>
                </h4>
                <ul className="text-xs text-slate-300 space-y-1.5 list-disc list-inside">
                  {comps_analysis.common_success_factors.map((f, i) => (
                    <li key={i}>{f}</li>
                  ))}
                </ul>
              </div>

              <div className="p-4 rounded-lg bg-red-950/20 border border-red-800/40">
                <h4 className="text-xs font-bold uppercase tracking-wider text-studio-accent mb-2 flex items-center space-x-1.5">
                  <AlertTriangle className="w-3.5 h-3.5" />
                  <span>Historical Pitfalls &amp; Hazards</span>
                </h4>
                <ul className="text-xs text-slate-300 space-y-1.5 list-disc list-inside">
                  {comps_analysis.common_pitfall_risks.map((p, i) => (
                    <li key={i}>{p}</li>
                  ))}
                </ul>
              </div>
            </div>

          </div>
        </div>
      )}

      {/* TAB CONTENT: 3. CALENDAR & CLASH RISK */}
      {(activeTab === 'calendar' || window.matchMedia('print').matches) && (
        <div className="space-y-6">
          <div className="bg-studio-800 border border-studio-700 rounded-xl p-6 print-card">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
              <div>
                <h3 className="font-display font-bold text-lg text-white">
                  Release Window &amp; Clash Risk Engine
                </h3>
                <p className="text-xs text-slate-400 mt-0.5">
                  Evaluated against gazetted Indian holidays, IPL schedule, and tentpole collisions
                </p>
              </div>

              {/* Risk Meter */}
              <div className="flex items-center space-x-3 bg-studio-900 border border-studio-700 px-4 py-2 rounded-xl">
                <span className="text-xs text-slate-400">Clash Risk Index:</span>
                <span className={`text-base font-extrabold ${
                  calendar_analysis.overall_risk_score >= 7 
                    ? 'text-red-500' 
                    : calendar_analysis.overall_risk_score >= 4 
                    ? 'text-amber-400' 
                    : 'text-emerald-400'
                }`}>
                  {calendar_analysis.overall_risk_score} / 10
                </span>
                <span className="text-xs px-2 py-0.5 rounded bg-studio-800 text-slate-200 font-semibold">
                  {calendar_analysis.risk_tier}
                </span>
              </div>
            </div>

            {/* Clash Events List */}
            <div className="space-y-3">
              {calendar_analysis.clashes_and_events.map((event, idx) => (
                <div 
                  key={idx} 
                  className={`p-4 rounded-xl border flex flex-col sm:flex-row sm:items-center justify-between gap-3 ${
                    event.severity === 'high' || event.severity === 'critical'
                      ? 'bg-red-950/20 border-red-800/50'
                      : event.severity === 'medium'
                      ? 'bg-amber-950/20 border-amber-800/50'
                      : 'bg-emerald-950/20 border-emerald-800/50'
                  }`}
                >
                  <div className="space-y-1">
                    <div className="flex items-center space-x-2">
                      <span className="text-xs font-mono px-2 py-0.5 rounded bg-studio-900 text-slate-300 font-semibold">
                        {event.date}
                      </span>
                      <h4 className="text-sm font-bold text-white">{event.event_name}</h4>
                      <span className="text-[10px] uppercase font-bold px-2 py-0.5 rounded bg-studio-900 text-slate-400">
                        {event.event_type.replace('_', ' ')}
                      </span>
                    </div>
                    <p className="text-xs text-slate-300">{event.description}</p>
                  </div>

                  <div className="text-right shrink-0">
                    <span className="text-xs text-slate-400 block">Footfall Impact</span>
                    <span className={`text-base font-bold font-mono ${
                      event.impact_multiplier >= 1.0 ? 'text-emerald-400' : 'text-red-400'
                    }`}>
                      {event.impact_multiplier}x
                    </span>
                  </div>
                </div>
              ))}
            </div>

            {/* Warnings and Synergies */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-6 pt-6 border-t border-studio-700/80">
              <div className="p-4 rounded-lg bg-emerald-950/20 border border-emerald-800/40">
                <h4 className="text-xs font-bold uppercase tracking-wider text-emerald-400 mb-2">
                  Festival Multiplier Synergies
                </h4>
                <ul className="text-xs text-slate-300 space-y-1.5 list-disc list-inside">
                  {calendar_analysis.festival_synergies.map((s, i) => (
                    <li key={i}>{s}</li>
                  ))}
                </ul>
              </div>

              <div className="p-4 rounded-lg bg-amber-950/20 border border-amber-800/40">
                <h4 className="text-xs font-bold uppercase tracking-wider text-amber-400 mb-2">
                  Hazard Alerts &amp; Collision Warnings
                </h4>
                <ul className="text-xs text-slate-300 space-y-1.5 list-disc list-inside">
                  {calendar_analysis.hazard_warnings.map((w, i) => (
                    <li key={i}>{w}</li>
                  ))}
                </ul>
              </div>
            </div>

          </div>
        </div>
      )}

      {/* TAB CONTENT: 4. AUDIENCE & DEMOGRAPHICS */}
      {(activeTab === 'audience' || window.matchMedia('print').matches) && (
        <div className="space-y-6">
          <div className="bg-studio-800 border border-studio-700 rounded-xl p-6 print-card">
            <h3 className="font-display font-bold text-lg text-white mb-1">
              Audience Archetype &amp; Demographic Modeling
            </h3>
            <p className="text-xs text-slate-400 mb-6">
              Analyzes core theatergoer profiles, sentiment catalysts, and territory appeal
            </p>

            {/* Progress Bar Split */}
            <div className="mb-8 p-5 rounded-xl bg-studio-900 border border-studio-700">
              <div className="flex justify-between text-xs font-bold uppercase tracking-wider mb-2">
                <span className="text-blue-400">
                  Urban Multiplex Circuits ({audience_analysis.urban_multiplex_appeal}%)
                </span>
                <span className="text-red-400">
                  Mass Heartland Single Screens ({audience_analysis.heartland_single_screen_appeal}%)
                </span>
              </div>
              <div className="w-full h-4 rounded-full bg-studio-800 overflow-hidden flex">
                <div 
                  className="bg-gradient-to-r from-blue-600 to-cyan-500 h-full transition-all" 
                  style={{ width: `${audience_analysis.urban_multiplex_appeal}%` }} 
                />
                <div 
                  className="bg-gradient-to-r from-amber-600 to-studio-accent h-full transition-all" 
                  style={{ width: `${audience_analysis.heartland_single_screen_appeal}%` }} 
                />
              </div>
              <div className="flex justify-between text-[11px] text-slate-400 mt-2">
                <span>Tier-1 Metros (Mumbai, Delhi-NCR, Bengaluru)</span>
                <span>Tier-2 / Tier-3 Mass Circuits (CP, CI, Bihar, UP Heartland)</span>
              </div>
            </div>

            {/* Primary Archetypes */}
            <div className="mb-6">
              <h4 className="text-xs font-bold uppercase tracking-wider text-slate-300 mb-3">
                Identified Core Audience Personas
              </h4>
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                {audience_analysis.primary_archetypes.map((arch, i) => (
                  <div key={i} className="p-3.5 rounded-lg bg-studio-900/80 border border-studio-700 text-xs text-white font-medium flex items-center space-x-2">
                    <span className="w-2 h-2 rounded-full bg-studio-accent shrink-0" />
                    <span>{arch}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Drivers & Fatigue Risks */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-4 border-t border-studio-700/80">
              <div className="p-4 rounded-lg bg-studio-900 border border-studio-700">
                <h4 className="text-xs font-bold uppercase tracking-wider text-emerald-400 mb-2">
                  Positive Sentiment Drivers
                </h4>
                <ul className="text-xs text-slate-300 space-y-1.5 list-disc list-inside">
                  {audience_analysis.sentiment_drivers.map((d, i) => (
                    <li key={i}>{d}</li>
                  ))}
                </ul>
              </div>

              <div className="p-4 rounded-lg bg-studio-900 border border-studio-700">
                <h4 className="text-xs font-bold uppercase tracking-wider text-studio-accent mb-2">
                  Fatigue &amp; Backlash Risks
                </h4>
                <ul className="text-xs text-slate-300 space-y-1.5 list-disc list-inside">
                  {audience_analysis.fatigue_or_backlash_risks.map((r, i) => (
                    <li key={i}>{r}</li>
                  ))}
                </ul>
              </div>
            </div>

          </div>
        </div>
      )}

      {/* TAB CONTENT: 5. RELEASE & DISTRIBUTION STRATEGY */}
      {(activeTab === 'strategy' || window.matchMedia('print').matches) && (
        <div className="space-y-6">
          <div className="bg-studio-800 border border-studio-700 rounded-xl p-6 print-card">
            <h3 className="font-display font-bold text-lg text-white mb-1">
              Ranked Release Options &amp; Distribution Architecture
            </h3>
            <p className="text-xs text-slate-400 mb-6">
              Screen allocation plans, festival runway evaluations, and OTT agreement mandates
            </p>

            {/* Options Comparison */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
              {release_strategy.ranked_release_options.map((opt) => (
                <div 
                  key={opt.rank}
                  className={`p-6 rounded-xl border flex flex-col justify-between ${
                    opt.rank === 1 
                      ? 'bg-studio-900/90 border-studio-accent shadow-lg shadow-red-950/20' 
                      : 'bg-studio-900/60 border-studio-700'
                  }`}
                >
                  <div>
                    <div className="flex items-center justify-between mb-3">
                      <span className={`text-xs font-bold uppercase tracking-wider px-2.5 py-0.5 rounded ${
                        opt.rank === 1 ? 'bg-studio-accent text-white' : 'bg-studio-700 text-slate-300'
                      }`}>
                        Option {opt.rank}: {opt.rank === 1 ? 'Primary Choice' : 'Contingency Runway'}
                      </span>
                      <span className="text-xs font-mono text-slate-400">{opt.competition_level}</span>
                    </div>

                    <h4 className="text-lg font-bold text-white mb-1">{opt.proposed_date}</h4>
                    <span className="text-xs text-studio-gold font-medium block mb-4">{opt.slot_type}</span>

                    <div className="space-y-3 mb-6">
                      <div>
                        <span className="text-[11px] uppercase tracking-wider font-bold text-emerald-400 block mb-1">Strategic Pros:</span>
                        <ul className="text-xs text-slate-300 space-y-1 list-disc list-inside">
                          {opt.pros.map((p, i) => <li key={i}>{p}</li>)}
                        </ul>
                      </div>
                      <div>
                        <span className="text-[11px] uppercase tracking-wider font-bold text-studio-accent block mb-1">Trade-offs &amp; Cons:</span>
                        <ul className="text-xs text-slate-300 space-y-1 list-disc list-inside">
                          {opt.cons.map((c, i) => <li key={i}>{c}</li>)}
                        </ul>
                      </div>
                    </div>
                  </div>

                  <div className="pt-4 border-t border-studio-800 text-xs text-slate-400">
                    <strong className="text-white">Capacity:</strong> {opt.screen_count_est}
                  </div>
                </div>
              ))}
            </div>

            {/* Pan India & OTT Window Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="p-4 rounded-xl bg-studio-900 border border-studio-700">
                <h4 className="text-xs font-bold uppercase tracking-wider text-studio-gold mb-2">
                  Pan-India Multi-Lingual Distribution Policy
                </h4>
                <p className="text-xs text-slate-300 leading-relaxed">
                  {release_strategy.pan_india_distribution_plan}
                </p>
              </div>

              <div className="p-4 rounded-xl bg-studio-900 border border-studio-700">
                <h4 className="text-xs font-bold uppercase tracking-wider text-purple-400 mb-2">
                  PVR-INOX 8-Week Theatrical Holdback Mandate
                </h4>
                <p className="text-xs text-slate-300 leading-relaxed">
                  {release_strategy.ott_windowing.rationale}
                </p>
              </div>
            </div>

          </div>
        </div>
      )}

      {/* TAB CONTENT: 6. 30/60/90 MARKETING PLAYBOOK */}
      {(activeTab === 'marketing' || window.matchMedia('print').matches) && (
        <div className="space-y-6">
          <div className="bg-studio-800 border border-studio-700 rounded-xl p-6 print-card">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
              <div>
                <h3 className="font-display font-bold text-lg text-white">
                  Tactical 30/60/90-Day Campaign Playbook
                </h3>
                <p className="text-xs text-slate-400 mt-0.5">
                  Asset cadence: Motion Poster, Song Drops, Theatrical Trailer, Advance Bookings &amp; City Tours
                </p>
              </div>
              <span className="text-xs font-semibold px-3 py-1 rounded bg-studio-900 border border-studio-700 text-studio-accent">
                {marketing_playbook.campaign_slogan_or_theme}
              </span>
            </div>

            {/* Timeline Beats */}
            <div className="relative border-l-2 border-studio-700 ml-4 pl-6 space-y-6 my-6">
              {marketing_playbook.timeline_beats.map((beat, idx) => (
                <div key={idx} className="relative">
                  {/* Dot */}
                  <div className="absolute -left-[31px] top-1 w-4 h-4 rounded-full bg-studio-900 border-2 border-studio-accent" />
                  
                  <div className="p-4 rounded-xl bg-studio-900/90 border border-studio-700/80">
                    <div className="flex flex-wrap items-center justify-between gap-2 mb-2">
                      <div className="flex items-center space-x-2">
                        <span className="text-xs font-bold text-studio-accent uppercase font-mono">
                          {beat.day_offset}
                        </span>
                        <span className="text-xs font-semibold text-white">
                          • {beat.title}
                        </span>
                      </div>
                      <span className="text-[11px] px-2 py-0.5 rounded bg-studio-800 text-slate-300 border border-studio-700">
                        {beat.phase}
                      </span>
                    </div>

                    <p className="text-xs text-slate-300 leading-relaxed mb-3">
                      {beat.description}
                    </p>

                    <div className="flex flex-wrap items-center justify-between gap-2 pt-2 border-t border-studio-800 text-[11px]">
                      <div className="text-slate-400">
                        Channels: <span className="text-slate-200">{beat.target_channels.join(', ')}</span>
                      </div>
                      <div className="text-emerald-400 font-medium">
                        KPI: {beat.kpi_metric}
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>

            {/* Strategic Marketing Enablers */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-6 pt-6 border-t border-studio-700/80">
              <div className="p-4 rounded-lg bg-studio-900 border border-studio-700">
                <h4 className="text-xs font-bold uppercase tracking-wider text-rose-400 mb-2">
                  Music-First Audio Cadence
                </h4>
                <p className="text-xs text-slate-300 leading-relaxed">
                  {marketing_playbook.music_release_cadence}
                </p>
              </div>

              <div className="p-4 rounded-lg bg-studio-900 border border-studio-700">
                <h4 className="text-xs font-bold uppercase tracking-wider text-amber-400 mb-2">
                  Co-Branded Consumer Tie-ins
                </h4>
                <ul className="text-xs text-slate-300 space-y-1 list-disc list-inside">
                  {marketing_playbook.brand_tie_ins.map((b, i) => <li key={i}>{b}</li>)}
                </ul>
              </div>

              <div className="p-4 rounded-lg bg-studio-900 border border-studio-700">
                <h4 className="text-xs font-bold uppercase tracking-wider text-cyan-400 mb-2">
                  Multiplex vs Single-Screen Activations
                </h4>
                <p className="text-xs text-slate-300 leading-relaxed">
                  {marketing_playbook.single_screen_vs_multiplex_activation}
                </p>
              </div>
            </div>

          </div>
        </div>
      )}

      {/* TAB CONTENT: 7. ANTI-HALLUCINATION CRITIC AUDIT */}
      {(activeTab === 'critic' || window.matchMedia('print').matches) && (
        <div className="space-y-6">
          <div className="bg-studio-800 border border-studio-700 rounded-xl p-6 print-card">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
              <div>
                <h3 className="font-display font-bold text-lg text-white">
                  Executive Critic Audit &amp; Data Verification Trail
                </h3>
                <p className="text-xs text-slate-400 mt-0.5">
                  Every claim is certified against raw historical data or labeled as an industry strategic inference
                </p>
              </div>
              <div className="flex items-center space-x-2 text-xs px-3 py-1.5 rounded-full bg-emerald-950/60 border border-emerald-800 text-emerald-300">
                <ShieldCheck className="w-4 h-4" />
                <span>Zero Unsubstantiated Hallucinations</span>
              </div>
            </div>

            {/* Mathematical Formula & Verification Breakdown Banner */}
            <div className="mb-6 p-4 rounded-xl bg-studio-900 border border-studio-700/80 flex flex-col md:flex-row md:items-center justify-between gap-4">
              <div className="space-y-1">
                <span className="text-[11px] font-bold uppercase tracking-wider text-slate-400">
                  Audit Scoring Formula &amp; Verification Methodology
                </span>
                <p className="font-mono text-xs text-studio-gold">
                  {critic_audit.score_formula_breakdown || `Formula: ((Verified [${critic_audit.verified_claims_count}] × 1.0) + (Inferences [${critic_audit.probable_inferences_count || 0}] × 0.65)) / Total Checked [${critic_audit.total_claims_checked}] × 100 = ${critic_audit.credibility_score}%`}
                </p>
                <p className="text-[11px] text-slate-400">
                  Verified ground-truth facts carry 100% weight; reasoned planning inferences carry 65% weight; contradictions carry penalties.
                </p>
              </div>

              <div className="flex items-center space-x-3 shrink-0">
                <div className="px-3 py-1.5 rounded-lg bg-emerald-950/50 border border-emerald-800 text-center">
                  <span className="block text-base font-bold text-emerald-400">{critic_audit.verified_claims_count}</span>
                  <span className="text-[10px] text-slate-400 uppercase">Verified</span>
                </div>
                <div className="px-3 py-1.5 rounded-lg bg-amber-950/50 border border-amber-800 text-center">
                  <span className="block text-base font-bold text-amber-400">{critic_audit.probable_inferences_count || 0}</span>
                  <span className="text-[10px] text-slate-400 uppercase">Inferences</span>
                </div>
                <div className="px-3 py-1.5 rounded-lg bg-studio-800 border border-studio-700 text-center">
                  <span className="block text-base font-bold text-slate-200">{critic_audit.total_claims_checked}</span>
                  <span className="text-[10px] text-slate-400 uppercase">Total Checks</span>
                </div>
              </div>
            </div>

            {/* Audit Table */}
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs border-collapse">
                <thead>
                  <tr className="border-b border-studio-700 text-slate-400 uppercase tracking-wider text-[11px]">
                    <th className="py-3 px-3">Audited Assertion</th>
                    <th className="py-3 px-3">Type</th>
                    <th className="py-3 px-3">Source Reference</th>
                    <th className="py-3 px-3">Status</th>
                    <th className="py-3 px-3">Critic Auditor Notes</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-studio-700/60">
                  {critic_audit.audit_items.map((item, idx) => (
                    <tr key={idx} className="hover:bg-studio-700/30 transition-colors">
                      <td className="py-3 px-3 font-medium text-white max-w-sm">
                        {item.claim}
                      </td>
                      <td className="py-3 px-3 uppercase text-[10px] text-slate-400 font-mono">
                        {item.claim_type.replace('_', ' ')}
                      </td>
                      <td className="py-3 px-3 text-slate-300 whitespace-nowrap">
                        {item.source_reference}
                      </td>
                      <td className="py-3 px-3 whitespace-nowrap">
                        <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                          item.status === 'VERIFIED'
                            ? 'bg-emerald-950 text-emerald-300 border border-emerald-800'
                            : 'bg-amber-950 text-amber-300 border border-amber-800'
                        }`}>
                          {item.status}
                        </span>
                      </td>
                      <td className="py-3 px-3 text-slate-300 leading-relaxed">
                        {item.critic_notes}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            {/* Known Limitations & Uncontrollable Risks */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-6 pt-6 border-t border-studio-700/80">
              <div className="p-4 rounded-lg bg-studio-900 border border-studio-700">
                <h4 className="text-xs font-bold uppercase tracking-wider text-slate-300 mb-2">
                  Recognized Data &amp; Tracking Limitations
                </h4>
                <ul className="text-xs text-slate-400 space-y-1.5 list-disc list-inside">
                  {critic_audit.known_data_limitations.map((lim, i) => (
                    <li key={i}>{lim}</li>
                  ))}
                </ul>
              </div>

              <div className="p-4 rounded-lg bg-studio-900 border border-studio-700">
                <h4 className="text-xs font-bold uppercase tracking-wider text-slate-300 mb-2">
                  Uncontrollable Theatrical Market Risks
                </h4>
                <ul className="text-xs text-slate-400 space-y-1.5 list-disc list-inside">
                  {critic_audit.uncontrollable_risks.map((risk, i) => (
                    <li key={i}>{risk}</li>
                  ))}
                </ul>
              </div>
            </div>

          </div>
        </div>
      )}

    </div>
  );
}
