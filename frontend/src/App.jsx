import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import FilmInputForm from './components/FilmInputForm';
import AgentProgressTracker from './components/AgentProgressTracker';
import ReportDashboard from './components/ReportDashboard';

const DEFAULT_FILM_INPUT = {
  title: "Jawan",
  genres: ["Action", "Thriller", "Drama"],
  language: "Hindi",
  budget_tier: "mega",
  star_tier: "tier_1",
  director: "Atlee",
  target_audience: "Mass heartland single-screens + youth urban multiplexes + South regional audiences",
  planned_window: "Sept 2026 (Janmashtami extended weekend)",
  logline: "A former commando turned jailer leads a team of six women inmates on audacious socio-political hijackings across India to force government accountability, while confronting a ruthless global arms merchant from his forgotten past.",
  platforms: "theatrical",
  pan_india: true
};

export default function App() {
  const [formData, setFormData] = useState(DEFAULT_FILM_INPUT);
  const [presets, setPresets] = useState([]);
  const [activePresetId, setActivePresetId] = useState('jawan');
  const [systemHealth, setSystemHealth] = useState(null);
  
  const [isLoading, setIsLoading] = useState(false);
  const [currentLogs, setCurrentLogs] = useState([]);
  const [report, setReport] = useState(null);
  const [error, setError] = useState(null);

  // Initial data loading
  useEffect(() => {
    async function init() {
      try {
        const [healthRes, presetsRes] = await Promise.all([
          fetch('/api/v1/health').catch(() => null),
          fetch('/api/v1/presets').catch(() => null)
        ]);

        if (healthRes && healthRes.ok) {
          const hData = await healthRes.json();
          setSystemHealth(hData);
        }
        if (presetsRes && presetsRes.ok) {
          const pData = await presetsRes.json();
          setPresets(pData);
        }
      } catch (err) {
        console.warn("Failed to load initial metadata:", err);
      }
    }
    init();
  }, []);

  const handleLoadPreset = async (presetId) => {
    setActivePresetId(presetId);
    setError(null);
    try {
      const res = await fetch(`/api/v1/presets/${presetId}`);
      if (res.ok) {
        const data = await res.json();
        setFormData(data.input);
      }
    } catch (err) {
      console.error("Error loading preset:", err);
    }
  };

  const handleSubmit = async (e) => {
    e?.preventDefault();
    setIsLoading(true);
    setError(null);
    setCurrentLogs([]);

    // Simulated progress indicators while waiting for pipeline
    const timer1 = setTimeout(() => {
      setCurrentLogs(prev => [...prev, {
        agent: "Market & Comps Agent",
        message: "Benchmarking 10+ historical titles against budget & star scale",
        status: "completed",
        elapsed_seconds: 0.12
      }]);
    }, 200);

    const timer2 = setTimeout(() => {
      setCurrentLogs(prev => [...prev, {
        agent: "Calendar & Clash Agent",
        message: `Cross-referencing release window '${formData.planned_window}' against Indian festivals`,
        status: "completed",
        elapsed_seconds: 0.28
      }]);
    }, 450);

    const timer3 = setTimeout(() => {
      setCurrentLogs(prev => [...prev, {
        agent: "Audience & Sentiment Agent",
        message: "Calculating urban multiplex vs heartland single-screen resonance",
        status: "completed",
        elapsed_seconds: 0.45
      }]);
    }, 700);

    try {
      const res = await fetch('/api/v1/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });

      if (!res.ok) {
        throw new Error(`Analysis failed with status code ${res.status}`);
      }

      const reportData = await res.json();
      
      // Update with final logs from server
      if (reportData.metadata?.agent_execution_logs) {
        setCurrentLogs(reportData.metadata.agent_execution_logs);
      }
      setReport(reportData);
    } catch (err) {
      setError(err.message || "Failed to generate report. Please verify backend is running.");
    } finally {
      clearTimeout(timer1);
      clearTimeout(timer2);
      clearTimeout(timer3);
      setIsLoading(false);
    }
  };

  const handleReset = () => {
    setReport(null);
    setError(null);
  };

  return (
    <div className="min-h-screen bg-studio-900 text-slate-100 flex flex-col font-sans">
      
      {/* Top Studio Bar */}
      <Header systemHealth={systemHealth} onSelectPreset={handleLoadPreset} />

      {/* Main Content Area */}
      <main className="flex-1 max-w-7xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-8 sm:py-10">
        
        {error && (
          <div className="mb-6 p-4 rounded-xl bg-red-950/60 border border-red-800 text-red-200 text-xs flex items-center justify-between">
            <span>{error}</span>
            <button onClick={() => setError(null)} className="font-bold underline ml-4">Dismiss</button>
          </div>
        )}

        {/* If no report is active, show the input form */}
        {!report ? (
          <div>
            <div className="max-w-3xl mb-8">
              <span className="text-xs uppercase tracking-widest font-bold text-studio-accent">
                Autonomous Studio Intelligence Platform
              </span>
              <h2 className="font-display font-extrabold text-3xl sm:text-4xl text-white tracking-tight mt-1 mb-3">
                Data-Backed Film Release &amp; Campaign Analyst
              </h2>
              <p className="text-sm text-slate-400 leading-relaxed">
                Zero false-precision box office guessing. Ingests your film parameters and runs 6 specialized agents 
                to evaluate comparable benchmarks, release clash risks, demographic positioning, and a 30/60/90-day marketing playbook.
              </p>
            </div>

            {isLoading && (
              <AgentProgressTracker logs={currentLogs} isRunning={true} />
            )}

            <FilmInputForm
              formData={formData}
              setFormData={setFormData}
              presets={presets}
              onLoadPreset={handleLoadPreset}
              activePresetId={activePresetId}
              onSubmit={handleSubmit}
              isLoading={isLoading}
            />
          </div>
        ) : (
          <div>
            {/* Show Agent Waterfall Logs for transparency */}
            <AgentProgressTracker 
              logs={report.metadata?.agent_execution_logs || currentLogs} 
              isRunning={false} 
            />

            {/* Comprehensive Executive Report */}
            <ReportDashboard report={report} onReset={handleReset} />
          </div>
        )}

      </main>

      {/* Studio Footer */}
      <footer className="border-t border-studio-800 bg-studio-950 py-6 text-center text-xs text-slate-500 no-print">
        <div className="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-3">
          <p>© 2026 CineStrategist. Designed for premier studio distribution &amp; marketing intelligence.</p>
          <div className="flex items-center space-x-4">
            <span className="text-slate-400">Strict PVR-INOX 8-Week OTT Compliance</span>
            <span className="text-slate-400">•</span>
            <span className="text-slate-400">Indian Theatrical Calendar Sync</span>
          </div>
        </div>
      </footer>

    </div>
  );
}
