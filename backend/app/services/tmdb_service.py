"""
TMDB & Curated Benchmark Integration Service with Multi-Factor Similarity Scoring.
Computes true Jaccard genre similarity, budget tier distance, star power matching,
and logline thematic keyword resonance.
"""

import httpx
import re
from typing import List, Dict, Any, Optional
from app.config import settings
from app.data.benchmarks import BENCHMARK_FILMS

_CACHE: Dict[str, Any] = {}

class TMDBService:
    BASE_URL = "https://api.themoviedb.org/3"

    def __init__(self):
        self.api_key = settings.TMDB_API_KEY

    def is_configured(self) -> bool:
        return bool(self.api_key and len(self.api_key.strip()) > 5)

    async def get_comparable_candidates(
        self, 
        genres: List[str], 
        budget_tier: str, 
        star_tier: str, 
        language: str = "Hindi",
        logline: str = ""
    ) -> List[Dict[str, Any]]:
        """
        Retrieves comparable films with rigorous multi-factor scoring:
        - Genre Jaccard Index (0.0 to 1.0)
        - Budget tier compatibility (mega vs high vs mid)
        - Star power pull alignment
        - Thematic keyword resonance from logline
        Employs progressive fallback (strict 2+ genre match -> 1-genre match -> scale fallback)
        to ensure robust decision support without 0-comp crashes.
        """
        user_genres_set = set(g.strip().lower() for g in genres)
        logline_tokens = set(re.findall(r'\b[a-zA-Z]{3,}\b', logline.lower())) if logline else set()

        def score_film(film: Dict[str, Any], min_genre_match: int) -> Optional[Dict[str, Any]]:
            film_genres_set = set(g.strip().lower() for g in film["genres"])
            intersection = user_genres_set.intersection(film_genres_set)
            union = user_genres_set.union(film_genres_set)

            if len(intersection) < min_genre_match:
                return None

            # 1. Jaccard Genre Similarity (Weight: 0.35)
            jaccard_genre = len(intersection) / len(union) if union else 0.0
            genre_score = jaccard_genre * 0.35

            f_budget = film.get("budget_tier", "mid")
            
            # STRICT BUDGET SCALE ENFORCEMENT:
            # - For "low" budget films (<= ₹35 Cr): REJECT mega and high budget films (completely different economics).
            # - For "mid" budget films (₹35-90 Cr): REJECT mega budget films (> ₹200 Cr).
            # - For "mega" budget films (> ₹200 Cr): REJECT low budget films (< ₹35 Cr).
            if budget_tier == "low" and f_budget in ["mega", "high"]:
                return None
            if budget_tier == "mid" and f_budget == "mega":
                return None
            if budget_tier == "mega" and f_budget == "low":
                return None

            # 2. Budget Tier Compatibility (Weight: 0.25)
            if f_budget == budget_tier:
                budget_score = 0.25
            elif (budget_tier == "mega" and f_budget == "high") or (budget_tier == "high" and f_budget == "mega"):
                budget_score = 0.15
            elif (budget_tier == "high" and f_budget == "mid") or (budget_tier == "mid" and f_budget == "high"):
                budget_score = 0.10
            elif (budget_tier == "mid" and f_budget == "low") or (budget_tier == "low" and f_budget == "mid"):
                budget_score = 0.15
            else:
                budget_score = 0.0

            # 3. Star Power Compatibility (Weight: 0.20)
            f_star = film.get("star_tier", "tier_2")
            if f_star == star_tier:
                star_score = 0.20
            elif (star_tier == "tier_1" and f_star == "tier_2") or (star_tier == "tier_2" and f_star == "tier_1"):
                star_score = 0.10
            elif (star_tier == "tier_2" and f_star == "tier_3") or (star_tier == "tier_3" and f_star == "tier_2"):
                star_score = 0.10
            else:
                star_score = 0.05

            # 4. Thematic Keyword Resonance (Weight: 0.20)
            f_themes = set(t.lower() for t in film.get("themes", []))
            theme_matches = logline_tokens.intersection(f_themes)
            theme_score = min(0.20, len(theme_matches) * 0.06)

            total_similarity = genre_score + budget_score + star_score + theme_score
            normalized_score = round(min(0.98, max(0.25, total_similarity)), 2)

            reasons = []
            if intersection:
                reasons.append(f"Matching genres: {', '.join(g.capitalize() for g in intersection)}")
            elif min_genre_match == 0:
                reasons.append("Scale-based benchmark fallback (No direct genre match)")
            if f_budget == budget_tier:
                reasons.append(f"Matching budget scale ({budget_tier.capitalize()})")
            if theme_matches:
                reasons.append(f"Shared themes: {', '.join(t.capitalize() for t in theme_matches)}")
            if film.get("language", "").lower() == language.lower():
                reasons.append(f"Same primary market ({language})")

            return {
                **film,
                "original_language": film.get("original_language", film.get("language", "Hindi")),
                "similarity_score": normalized_score,
                "similarity_factors": reasons
            }

        # Pass 1: Strict Match (>= 2 genres if user selected >= 2 genres, 1 if 1 genre, 0 if 0 genres provided)
        required_matches = 2 if len(user_genres_set) >= 2 else (1 if len(user_genres_set) == 1 else 0)
        candidates = []
        seen_ids = set()

        for film in BENCHMARK_FILMS:
            res = score_film(film, min_genre_match=required_matches)
            if res:
                candidates.append(res)
                seen_ids.add(film["id"])

        # Pass 2: Relaxed Match (>= 1 genre match) if fewer than 3 candidates
        if len(candidates) < 3 and required_matches > 1:
            for film in BENCHMARK_FILMS:
                if film["id"] in seen_ids:
                    continue
                res = score_film(film, min_genre_match=1)
                if res:
                    res["similarity_score"] = round(res["similarity_score"] * 0.85, 2)
                    candidates.append(res)
                    seen_ids.add(film["id"])

        # Pass 3: Scale Fallback if still fewer than 2 candidates
        if len(candidates) < 2:
            for film in BENCHMARK_FILMS:
                if film["id"] in seen_ids:
                    continue
                res = score_film(film, min_genre_match=0)
                if res:
                    res["similarity_score"] = min(0.40, round(res["similarity_score"] * 0.60, 2))
                    candidates.append(res)
                    seen_ids.add(film["id"])
                    if len(candidates) >= 4:
                        break

        # Sort by similarity score descending
        candidates.sort(key=lambda x: x["similarity_score"], reverse=True)
        return candidates[:6]

tmdb_service = TMDBService()
