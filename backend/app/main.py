"""
FastAPI Server for CineStrategist.
Provides REST API endpoints for film analysis, historical presets,
benchmark retrieval, and system health.
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any, List

from app.config import settings
from app.models.schemas import FilmInput, CineStrategistReport
from app.orchestrator import orchestrator
from app.data.presets import PRESET_FILMS
from app.data.benchmarks import BENCHMARK_FILMS
from app.data.festivals import FESTIVALS_AND_HOLIDAYS
from app.services.llm_service import llm_service
from app.services.tmdb_service import tmdb_service

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Multi-Agent Film Release and Marketing Analyst API"
)

# CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/v1/health")
async def health_check():
    return {
        "status": "online",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "llm_provider": "Gemini API (Active)" if llm_service.is_available() else "Deterministic Multi-Agent Engine (Offline/Hybrid)",
        "tmdb_configured": tmdb_service.is_configured(),
        "total_curated_benchmarks": len(BENCHMARK_FILMS),
        "total_festivals_tracked": len(FESTIVALS_AND_HOLIDAYS)
    }

@app.get("/api/v1/presets")
async def get_presets():
    """Returns historical backtest presets for instant 1-click evaluation."""
    return [
        {
            "id": k,
            "name": v["name"],
            "year": v["year"],
            "historical_context": v["historical_context"],
            "preview_data": v["input"]
        }
        for k, v in PRESET_FILMS.items()
    ]

@app.get("/api/v1/presets/{preset_id}")
async def get_preset_detail(preset_id: str):
    if preset_id not in PRESET_FILMS:
        raise HTTPException(status_code=404, detail=f"Preset '{preset_id}' not found.")
    return PRESET_FILMS[preset_id]

@app.post("/api/v1/analyze", response_model=CineStrategistReport)
async def analyze_film(film_input: FilmInput, bypass_cache: bool = False):
    """
    Triggers the 6-agent CineStrategist pipeline to produce a data-backed release and marketing report.
    """
    try:
        report = await orchestrator.run_pipeline(film_input, bypass_cache=bypass_cache)
        return report
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Analysis pipeline failed: {str(e)}")

@app.get("/api/v1/benchmarks")
async def get_benchmarks():
    """Returns curated Indian and international box office benchmarks."""
    return BENCHMARK_FILMS

@app.get("/api/v1/festivals")
async def get_festivals():
    """Returns the Indian theatrical festival calendar and footfall multipliers."""
    return FESTIVALS_AND_HOLIDAYS

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=True)
