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

import time
from collections import defaultdict
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from fastapi import Request

class RateLimitMiddleware(BaseHTTPMiddleware):
    """In-memory rate limiter protecting AI pipeline endpoints against abuse."""
    def __init__(self, app, requests_per_minute: int = 30):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.request_records = defaultdict(list)

    async def dispatch(self, request: Request, call_next):
        if request.url.path.startswith("/api/v1/analyze"):
            client_ip = request.client.host if request.client else "127.0.0.1"
            forwarded = request.headers.get("x-forwarded-for")
            if forwarded:
                client_ip = forwarded.split(",")[0].strip()

            now = time.time()
            window_start = now - 60.0
            timestamps = [ts for ts in self.request_records[client_ip] if ts > window_start]

            if len(timestamps) >= self.requests_per_minute:
                return JSONResponse(
                    status_code=429,
                    content={
                        "detail": f"Rate limit exceeded: maximum {self.requests_per_minute} analyses per minute per IP. Please retry shortly.",
                        "retry_after_seconds": int(60 - (now - timestamps[0]))
                    },
                    headers={"Retry-After": "60"}
                )

            timestamps.append(now)
            self.request_records[client_ip] = timestamps

        return await call_next(request)

app.add_middleware(RateLimitMiddleware, requests_per_minute=30)

@app.get("/api/v1/health")
async def health_check():
    return {
        "status": "online",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "llm_provider": "Gemini API (Active)" if llm_service.is_available() else "Deterministic Multi-Agent Engine (Offline/Hybrid)",
        "tmdb_configured": tmdb_service.is_configured(),
        "total_curated_benchmarks": len(BENCHMARK_FILMS),
        "total_festivals_tracked": len(FESTIVALS_AND_HOLIDAYS),
        "disclaimer": "CineStrategist is an autonomous strategic decision-support engine, not a deterministic box-office predictor. Projections represent trade heuristic modeling based on historical theatrical metrics.",
        "attribution": "This product uses the TMDB API but is not endorsed or certified by TMDB. Theatrical box office metrics curated from industry trade archives.",
        "data_last_checked": "October 2026"
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

# Serve static frontend build if it exists (for unified single-port hosting)
import os
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

frontend_dist = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../frontend/dist"))
if os.path.exists(frontend_dist):
    assets_dir = os.path.join(frontend_dist, "assets")
    if os.path.exists(assets_dir):
        app.mount("/assets", StaticFiles(directory=assets_dir), name="static-assets")

    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        if full_path.startswith("api/"):
            raise HTTPException(status_code=404, detail="API endpoint not found")
        file_path = os.path.join(frontend_dist, full_path)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse(os.path.join(frontend_dist, "index.html"))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=True)

