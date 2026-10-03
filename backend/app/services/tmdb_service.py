"""
TMDB API Integration Service with Graceful Fallback and In-Memory Caching.
Fetches real movie metadata, genres, ratings, and similar titles.
Falls back seamlessly to local Indian & global curated benchmarks if TMDB API is offline or unconfigured.
"""

import httpx
from typing import List, Dict, Any, Optional
from app.config import settings
from app.data.benchmarks import BENCHMARK_FILMS

# In-memory LRU-like cache
_CACHE: Dict[str, Any] = {}

class TMDBService:
    BASE_URL = "https://api.themoviedb.org/3"

    def __init__(self):
        self.api_key = settings.TMDB_API_KEY

    def is_configured(self) -> bool:
        return bool(self.api_key and len(self.api_key.strip()) > 5)

    async def search_movies(self, query: str) -> List[Dict[str, Any]]:
        cache_key = f"search_{query.lower()}"
        if cache_key in _CACHE:
            return _CACHE[cache_key]

        if not self.is_configured():
            # Filter from curated benchmark database
            results = [
                f for f in BENCHMARK_FILMS 
                if query.lower() in f["title"].lower() or any(query.lower() in g.lower() for g in f["genres"])
            ]
            _CACHE[cache_key] = results
            return results

        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                res = await client.get(
                    f"{self.BASE_URL}/search/movie",
                    params={"api_key": self.api_key, "query": query, "include_adult": False}
                )
                if res.status_code == 200:
                    data = res.json()
                    results = data.get("results", [])
                    _CACHE[cache_key] = results
                    return results
        except Exception as e:
            print(f"[TMDB] Live search failed: {e}. Falling back to curated data.")

        # Fallback
        results = [f for f in BENCHMARK_FILMS if query.lower() in f["title"].lower()]
        _CACHE[cache_key] = results
        return results

    async def get_comparable_candidates(
        self, 
        genres: List[str], 
        budget_tier: str, 
        star_tier: str, 
        language: str = "Hindi"
    ) -> List[Dict[str, Any]]:
        """
        Retrieves comparable films based on genre overlap, budget tier, and scale.
        Calculates similarity scoring.
        """
        candidates = []
        for film in BENCHMARK_FILMS:
            genre_overlap = set(g.lower() for g in genres).intersection(set(g.lower() for g in film["genres"]))
            similarity_points = len(genre_overlap) * 0.35
            
            # Budget tier matching
            if film.get("budget_tier") == budget_tier:
                similarity_points += 0.25
            
            # Star tier matching
            if film.get("star_tier") == star_tier:
                similarity_points += 0.20
                
            # Language matching
            if film.get("language", "").lower() == language.lower():
                similarity_points += 0.20

            # Normalize to max 0.98
            score = min(0.98, max(0.40, similarity_points))
            
            reasons = []
            if genre_overlap:
                reasons.append(f"Shared genres: {', '.join(g.capitalize() for g in genre_overlap)}")
            if film.get("budget_tier") == budget_tier:
                reasons.append(f"Matching budget scale ({budget_tier.capitalize()})")
            if film.get("star_tier") == star_tier:
                reasons.append(f"Comparable star power pull ({star_tier})")
            if film.get("language", "").lower() == language.lower():
                reasons.append(f"Same primary market ({language})")

            candidates.append({
                **film,
                "similarity_score": round(score, 2),
                "similarity_factors": reasons
            })

        # Sort by similarity score descending
        candidates.sort(key=lambda x: x["similarity_score"], reverse=True)
        return candidates[:6]

tmdb_service = TMDBService()
