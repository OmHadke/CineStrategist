import React, { useState } from 'react';
import { Play, Sparkles, History, ChevronRight, Info, CheckCircle2 } from 'lucide-react';

const GENRE_OPTIONS = [
  "Action", "Thriller", "Drama", "Comedy", "Horror", 
  "Romance", "Crime", "Mystery", "War", "Fantasy", "Social"
];

export default function FilmInputForm({ 
  formData, 
  setFormData, 
  presets, 
  onLoadPreset, 
  activePresetId,
  onSubmit, 
  isLoading 
}) {
  const [selectedGenre, setSelectedGenre] = useState('');

  const handleGenreToggle = (genre) => {
    if (formData.genres.includes(genre)) {
      if (formData.genres.length > 1) {
        setFormData({ ...formData, genres: formData.genres.filter(g => g !== genre) });
      }
    } else {
      setFormData({ ...formData, genres: [...formData.genres, genre] });
    }
  };

  return (
    <div className="bg-studio-800 border border-studio-700/80 rounded-2xl p-6 sm:p-8 shadow-xl">
      
      {/* Historical Presets Quick-Bar */}
      <div className="mb-8 p-4 rounded-xl bg-studio-900/60 border border-studio-700/60">
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center space-x-2">
            <History className="w-4 h-4 text-studio-gold" />
            <span className="text-xs font-bold uppercase tracking-wider text-slate-300">
              One-Click Historical Case Studies (Evaluation Suite)
            </span>
          </div>
          <span className="text-[11px] text-slate-400">Pre-release inputs tested against real outcomes</span>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-2.5">
          {presets.map((preset) => {
            const isSelected = activePresetId === preset.id;
            return (
              <button
                key={preset.id}
                type="button"
                onClick={() => onLoadPreset(preset.id)}
                className={`text-left p-3 rounded-lg border transition-all ${
                  isSelected 
                    ? 'bg-studio-accent/15 border-studio-accent text-white shadow-sm'
                    : 'bg-studio-800/80 border-studio-700/70 text-slate-300 hover:border-slate-500 hover:bg-studio-700/50'
                }`}
              >
                <div className="flex items-center justify-between mb-1">
                  <span className="font-semibold text-xs text-white truncate">{preset.name}</span>
                  {isSelected && <CheckCircle2 className="w-3.5 h-3.5 text-studio-accent shrink-0 ml-1" />}
                </div>
                <p className="text-[11px] text-slate-400 line-clamp-1">{preset.historical_context}</p>
              </button>
            );
          })}
        </div>
      </div>

      {/* Main Input Form */}
      <form onSubmit={onSubmit} className="space-y-6">
        
        {/* Title & Language */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="md:col-span-2">
            <label className="block text-xs font-bold uppercase tracking-wider text-slate-300 mb-2">
              Film Working Title <span className="text-studio-accent">*</span>
            </label>
            <input
              type="text"
              required
              value={formData.title}
              onChange={(e) => setFormData({ ...formData, title: e.target.value })}
              placeholder="e.g. Jawan, Dhurandhar, Project Thunder"
              className="w-full bg-studio-900 border border-studio-600 rounded-xl px-4 py-3 text-white placeholder-slate-500 focus:outline-none focus:border-studio-accent focus:ring-1 focus:ring-studio-accent text-sm"
            />
          </div>

          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-slate-300 mb-2">
              Primary Language
            </label>
            <select
              value={formData.language}
              onChange={(e) => setFormData({ ...formData, language: e.target.value })}
              className="w-full bg-studio-900 border border-studio-600 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-studio-accent text-sm"
            >
              <option value="Hindi">Hindi (Bollywood)</option>
              <option value="Telugu">Telugu (Tollywood)</option>
              <option value="Tamil">Tamil (Kollywood)</option>
              <option value="Malayalam">Malayalam (Mollywood)</option>
              <option value="Kannada">Kannada (Sandalwood)</option>
              <option value="English">English / Global</option>
            </select>
          </div>
        </div>

        {/* Genres Selection */}
        <div>
          <label className="block text-xs font-bold uppercase tracking-wider text-slate-300 mb-2">
            Genres (Select 1 to 3) <span className="text-studio-accent">*</span>
          </label>
          <div className="flex flex-wrap gap-2">
            {GENRE_OPTIONS.map((genre) => {
              const isSelected = formData.genres.includes(genre);
              return (
                <button
                  key={genre}
                  type="button"
                  onClick={() => handleGenreToggle(genre)}
                  className={`px-3 py-1.5 rounded-lg text-xs font-medium border transition-colors ${
                    isSelected 
                      ? 'bg-studio-accent text-white border-studio-accent' 
                      : 'bg-studio-900/80 text-slate-400 border-studio-700 hover:border-slate-500 hover:text-slate-200'
                  }`}
                >
                  {genre}
                </button>
              );
            })}
          </div>
        </div>

        {/* Budget Tier & Star Power Tier */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-slate-300 mb-2">
              Budget Scale Tier <span className="text-studio-accent">*</span>
            </label>
            <select
              value={formData.budget_tier}
              onChange={(e) => setFormData({ ...formData, budget_tier: e.target.value })}
              className="w-full bg-studio-900 border border-studio-600 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-studio-accent text-sm"
            >
              <option value="mega">Mega Spectacle (&gt;₹200 Cr / &gt;$25M)</option>
              <option value="high">High Budget (₹75 - ₹200 Cr)</option>
              <option value="mid">Mid Budget (₹25 - ₹75 Cr)</option>
              <option value="low">Controlled / Low Budget (&lt;₹25 Cr)</option>
            </select>
          </div>

          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-slate-300 mb-2">
              Star Power &amp; Opening Pull <span className="text-studio-accent">*</span>
            </label>
            <select
              value={formData.star_tier}
              onChange={(e) => setFormData({ ...formData, star_tier: e.target.value })}
              className="w-full bg-studio-900 border border-studio-600 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-studio-accent text-sm"
            >
              <option value="tier_1">Tier-1 Megastar (Guaranteed Day-1 Opening Rush)</option>
              <option value="tier_2">Tier-2 Established Star (Strong Multiplex / Regional Pull)</option>
              <option value="tier_3">Tier-3 Emerging / Character Lead (Content Dependent)</option>
              <option value="ensemble">High-Profile Ensemble Cast</option>
              <option value="fresh_faces">Fresh Faces / Debutants</option>
            </select>
          </div>
        </div>

        {/* Planned Window & Director */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-slate-300 mb-2">
              Planned Theatrical Window <span className="text-studio-accent">*</span>
            </label>
            <input
              type="text"
              required
              value={formData.planned_window}
              onChange={(e) => setFormData({ ...formData, planned_window: e.target.value })}
              placeholder="e.g. Diwali 2026, Christmas 2026, Independence Day 2026, Q3 2026"
              className="w-full bg-studio-900 border border-studio-600 rounded-xl px-4 py-3 text-white placeholder-slate-500 focus:outline-none focus:border-studio-accent text-sm"
            />
          </div>

          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-slate-300 mb-2">
              Director (Optional)
            </label>
            <input
              type="text"
              value={formData.director || ''}
              onChange={(e) => setFormData({ ...formData, director: e.target.value })}
              placeholder="e.g. Atlee, Siddharth Anand, Rajkumar Hirani"
              className="w-full bg-studio-900 border border-studio-600 rounded-xl px-4 py-3 text-white placeholder-slate-500 focus:outline-none focus:border-studio-accent text-sm"
            />
          </div>
        </div>

        {/* Target Audience */}
        <div>
          <label className="block text-xs font-bold uppercase tracking-wider text-slate-300 mb-2">
            Target Audience &amp; Demographics <span className="text-studio-accent">*</span>
          </label>
          <input
            type="text"
            required
            value={formData.target_audience}
            onChange={(e) => setFormData({ ...formData, target_audience: e.target.value })}
            placeholder="e.g. Mass heartland single-screens + youth urban multiplexes + South regional audiences"
            className="w-full bg-studio-900 border border-studio-600 rounded-xl px-4 py-3 text-white placeholder-slate-500 focus:outline-none focus:border-studio-accent text-sm"
          />
        </div>

        {/* Logline / Plot Synopsis */}
        <div>
          <label className="block text-xs font-bold uppercase tracking-wider text-slate-300 mb-2">
            Logline &amp; Narrative Hook (1-2 Paragraphs) <span className="text-studio-accent">*</span>
          </label>
          <textarea
            required
            rows={3}
            value={formData.logline}
            onChange={(e) => setFormData({ ...formData, logline: e.target.value })}
            placeholder="Describe the central conflict, protagonist motivation, emotional core, and scale of the film..."
            className="w-full bg-studio-900 border border-studio-600 rounded-xl px-4 py-3 text-white placeholder-slate-500 focus:outline-none focus:border-studio-accent text-sm"
          />
        </div>

        {/* Toggles: Pan-India Dubbing & Release Platform */}
        <div className="flex flex-wrap items-center justify-between gap-4 pt-2 border-t border-studio-700/60">
          <div className="flex items-center space-x-3">
            <label className="relative inline-flex items-center cursor-pointer">
              <input 
                type="checkbox" 
                checked={formData.pan_india} 
                onChange={(e) => setFormData({ ...formData, pan_india: e.target.checked })} 
                className="sr-only peer" 
              />
              <div className="w-11 h-6 bg-studio-900 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-slate-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-studio-accent"></div>
            </label>
            <span className="text-xs text-slate-300 font-medium">
              Pan-India Dubbed Release (Tamil, Telugu, Malayalam, Kannada)
            </span>
          </div>

          <div className="flex items-center space-x-2">
            <span className="text-xs text-slate-400">Release Format:</span>
            <span className="text-xs font-semibold px-2.5 py-1 rounded bg-studio-900 border border-studio-700 text-white">
              Theatrical First (8-Week OTT Holdback)
            </span>
          </div>
        </div>

        {/* CTA Submit Button */}
        <div className="pt-4">
          <button
            type="submit"
            disabled={isLoading}
            className={`w-full py-4 px-6 rounded-xl font-display font-bold text-base flex items-center justify-center space-x-3 transition-all shadow-xl shadow-red-950/40 ${
              isLoading
                ? 'bg-studio-700 text-slate-400 cursor-not-allowed'
                : 'bg-gradient-to-r from-studio-accent via-red-600 to-red-700 hover:from-red-600 hover:to-red-800 text-white active:scale-[0.99]'
            }`}
          >
            {isLoading ? (
              <>
                <div className="w-5 h-5 border-2 border-white/20 border-t-white rounded-full animate-spin" />
                <span>Orchestrating 6 Intelligence Agents...</span>
              </>
            ) : (
              <>
                <Sparkles className="w-5 h-5" />
                <span>Generate Studio Release &amp; Marketing Intelligence</span>
                <ChevronRight className="w-5 h-5" />
              </>
            )}
          </button>
        </div>

      </form>
    </div>
  );
}
