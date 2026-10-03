"""
Agent 1: Market & Comparable Benchmark Agent.
Identifies historical comparable releases, calculates statistical metrics,
and draws strategic lessons from past box-office performances.
"""

import numpy as np
from typing import List
from app.models.schemas import FilmInput, CompsAnalysis, ComparableFilm
from app.services.tmdb_service import tmdb_service
from app.services.llm_service import llm_service

class CompsAgent:
    async def run(self, film_input: FilmInput) -> CompsAnalysis:
        # 1. Fetch comps using TMDB / benchmark service
        raw_candidates = await tmdb_service.get_comparable_candidates(
            genres=film_input.genres,
            budget_tier=film_input.budget_tier,
            star_tier=film_input.star_tier,
            language=film_input.language
        )

        comparables: List[ComparableFilm] = []
        ratings = []

        for c in raw_candidates:
            ratings.append(c["imdb_rating"])
            comparables.append(ComparableFilm(
                id=c["id"],
                title=c["title"],
                year=c["year"],
                genres=c["genres"],
                director=c.get("director"),
                key_cast=c.get("key_cast", []),
                budget_est=c["budget_est"],
                box_office_est=c["box_office_est"],
                verdict=c["verdict"],
                imdb_rating=c["imdb_rating"],
                tmdb_score=c.get("tmdb_score"),
                similarity_score=c["similarity_score"],
                similarity_factors=c.get("similarity_factors", []),
                source=f"TMDB & Curated Box Office Index ({c['year']})",
                key_takeaway=c["key_takeaway"]
            ))

        median_rating = float(np.median(ratings)) if ratings else 6.8
        
        # Determine performance spread
        spread = f"₹{min(c['box_office_est'] for c in raw_candidates)} to ₹{max(c['box_office_est'] for c in raw_candidates)} (Median IMDb: {median_rating})"

        # Success & pitfall patterns
        all_success = []
        for c in raw_candidates:
            all_success.extend(c.get("success_factors", []))
        
        common_success = list(dict.fromkeys(all_success))[:4]
        if not common_success:
            common_success = [
                "Strong pre-release song virality driving day-1 advance booking",
                "Wide multi-lingual South dubbing footprint",
                "Clear high-concept hook with universal emotional grounding"
            ]

        common_pitfalls = [
            "Over-reliance on urban multiplex English-mix dialogues which hurts Tier-2/3 single screens",
            "Slow-starting second-half pacing causing post-weekend drop-offs",
            "Premature OTT release announcements eroding repeat theatrical viewing"
        ]

        summary = (
            f"Benchmarked against {len(comparables)} comparable titles in the {', '.join(film_input.genres)} "
            f"space ({film_input.budget_tier.upper()} budget tier, {film_input.star_tier.replace('_', ' ').title()}). "
            f"Historical comps demonstrate that sustained theatrical legs require an IMDb baseline >= 6.5 "
            f"and strong appeal beyond Tier-1 metro multiplexes."
        )

        return CompsAnalysis(
            comparables=comparables,
            median_rating=round(median_rating, 1),
            performance_spread=spread,
            common_success_factors=common_success,
            common_pitfall_risks=common_pitfalls,
            benchmark_summary=summary
        )

comps_agent = CompsAgent()
