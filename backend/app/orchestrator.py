"""
CineStrategist Master Multi-Agent Orchestrator.
Sequences the 6 agents, captures timing metrics, logs intermediate states,
and compiles the unified studio intelligence report.
"""

import time
import uuid
import hashlib
from typing import Dict, Any, List
from datetime import datetime

from app.models.schemas import FilmInput, CineStrategistReport
from app.agents.comps_agent import comps_agent
from app.agents.calendar_agent import calendar_agent
from app.agents.audience_agent import audience_agent
from app.agents.strategy_agent import strategy_agent
from app.agents.marketing_agent import marketing_agent
from app.agents.critic_agent import critic_agent
from app.services.llm_service import llm_service

# In-memory report cache
_REPORT_CACHE: Dict[str, CineStrategistReport] = {}

class Orchestrator:
    def _compute_cache_key(self, film_input: FilmInput) -> str:
        raw_key = f"{film_input.title}_{film_input.planned_window}_{film_input.budget_tier}_{film_input.star_tier}_{film_input.language}"
        return hashlib.md5(raw_key.lower().encode("utf-8")).hexdigest()

    async def run_pipeline(self, film_input: FilmInput, bypass_cache: bool = False) -> CineStrategistReport:
        cache_key = self._compute_cache_key(film_input)
        if not bypass_cache and cache_key in _REPORT_CACHE:
            print(f"[Orchestrator] Returning cached report for '{film_input.title}'")
            return _REPORT_CACHE[cache_key]

        start_time = time.time()
        logs: List[Dict[str, Any]] = []

        def log_step(agent_name: str, message: str, status: str = "completed"):
            logs.append({
                "timestamp": datetime.now().isoformat(),
                "agent": agent_name,
                "message": message,
                "status": status,
                "elapsed_seconds": round(time.time() - start_time, 2)
            })

        print(f"[Orchestrator] Starting CineStrategist Pipeline for '{film_input.title}'...")

        # Step 1: Comps Agent
        t0 = time.time()
        comps_result = await comps_agent.run(film_input)
        log_step("Market & Comps Agent", f"Identified {len(comps_result.comparables)} historical comparables. Median IMDb: {comps_result.median_rating}")
        
        # Step 2: Calendar & Clash Agent
        calendar_result = await calendar_agent.run(film_input)
        log_step("Calendar & Clash Agent", f"Evaluated window '{film_input.planned_window}'. Overall risk score: {calendar_result.overall_risk_score}/10 ({calendar_result.risk_tier})")

        # Step 3: Audience & Sentiment Agent
        audience_result = await audience_agent.run(film_input, comps_result)
        log_step("Audience & Sentiment Agent", f"Analyzed demographics: {audience_result.urban_multiplex_appeal}% Urban Multiplex vs {audience_result.heartland_single_screen_appeal}% Heartland Single Screen")

        # Step 4: Strategy & Distribution Agent
        strategy_result = await strategy_agent.run(film_input, comps_result, calendar_result, audience_result)
        log_step("Strategy & Distribution Agent", f"Generated {len(strategy_result.ranked_release_options)} ranked release corridors with 8-week MAI OTT holdback compliance")

        # Step 5: Tactical Marketing Agent
        marketing_result = await marketing_agent.run(film_input, audience_result, strategy_result)
        log_step("Marketing Playbook Agent", f"Crafted 30/60/90-day campaign playbook with {len(marketing_result.timeline_beats)} synchronized asset beats")

        # Step 6: The Critic & Verifier Agent
        critic_result = await critic_agent.run(
            film_input=film_input,
            comps=comps_result,
            calendar=calendar_result,
            audience=audience_result,
            strategy=strategy_result,
            marketing=marketing_result
        )
        log_step("Executive Critic & Verifier", f"Audited {critic_result.total_claims_checked} claims with {critic_result.credibility_score}% data verification score. Verdict: {critic_result.verdict}")

        total_elapsed = round(time.time() - start_time, 2)
        report_id = f"cine-{uuid.uuid4().hex[:8]}"

        report = CineStrategistReport(
            report_id=report_id,
            film_input=film_input,
            comps_analysis=comps_result,
            calendar_analysis=calendar_result,
            audience_analysis=audience_result,
            release_strategy=strategy_result,
            marketing_playbook=marketing_result,
            critic_audit=critic_result,
            metadata={
                "generated_at": datetime.now().strftime("%B %d, %Y - %H:%M:%S IST"),
                "execution_time_seconds": total_elapsed,
                "agent_execution_logs": logs,
                "llm_engine": "Gemini 2.5 Flash / Enhanced Multi-Agent Engine" if llm_service.is_available() else "CineStrategist Deterministic Heuristic Engine",
                "studio_grade": True
            }
        )

        _REPORT_CACHE[cache_key] = report
        print(f"[Orchestrator] Completed report {report_id} in {total_elapsed}s.")
        return report

orchestrator = Orchestrator()
