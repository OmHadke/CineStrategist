"""
End-to-End Test for CineStrategist Multi-Agent Pipeline.
Verifies that all 6 agents execute in sequence and output conforms to Pydantic schemas.
"""

import pytest
import asyncio
from app.models.schemas import FilmInput, CineStrategistReport
from app.orchestrator import orchestrator
from app.data.presets import PRESET_FILMS

@pytest.mark.asyncio
async def test_jawan_pipeline_execution():
    preset = PRESET_FILMS["jawan"]
    film_input = FilmInput(**preset["input"])
    
    report: CineStrategistReport = await orchestrator.run_pipeline(film_input, bypass_cache=True)
    
    # Assertions
    assert report.report_id.startswith("cine-")
    assert report.film_input.title == "Jawan"
    
    # 1. Comps Agent Check
    assert len(report.comps_analysis.comparables) >= 3
    assert report.comps_analysis.median_rating > 5.0
    
    # 2. Calendar Agent Check
    assert 1 <= report.calendar_analysis.overall_risk_score <= 10
    assert len(report.calendar_analysis.clashes_and_events) > 0
    
    # 3. Audience Agent Check
    assert report.audience_analysis.urban_multiplex_appeal + report.audience_analysis.heartland_single_screen_appeal == 100
    assert len(report.audience_analysis.sentiment_drivers) > 0
    
    # 4. Strategy Agent Check
    assert len(report.release_strategy.ranked_release_options) >= 2
    assert report.release_strategy.ott_windowing["theatrical_holdback_weeks"] == 8
    
    # 5. Marketing Agent Check
    assert len(report.marketing_playbook.timeline_beats) >= 4
    
    # 6. Critic Agent Check
    assert 0 <= report.critic_audit.credibility_score <= 100
    assert report.critic_audit.total_claims_checked > 0
    assert len(report.critic_audit.audit_items) > 0

    print("\n[TEST PASSED] Jawan pipeline executed successfully end-to-end!")
    print(f"Report ID: {report.report_id}")
    print(f"Credibility Score: {report.critic_audit.credibility_score}%")
    print(f"Execution Time: {report.metadata.get('execution_time_seconds')}s")

@pytest.mark.asyncio
async def test_project_agniveer_consistency_and_credibility():
    agniveer_input = FilmInput(
        title="Project Agniveer",
        language="Hindi",
        genres=["Action", "Thriller", "War"],
        budget_tier="mega",
        star_tier="tier_1",
        director="Test Director A",
        target_audience="Mass heartland single-screens, patriotic family audiences, urban multiplexes",
        planned_window="Independence Day 2027",
        logline="During a cross-border crisis, a special forces officer must lead a covert mission behind enemy lines with a team he doesn't trust. Part war film, part spy thriller, with large-scale action set pieces and an emotional core about duty versus family.",
        platforms="theatrical",
        pan_india=True
    )

    report: CineStrategistReport = await orchestrator.run_pipeline(agniveer_input, bypass_cache=True)

    # 1. Year and Window checks
    assert "2027" in report.calendar_analysis.clashes_and_events[0].date
    assert "diwali" not in [c.event_name.lower() for c in report.calendar_analysis.clashes_and_events]
    assert report.calendar_analysis.overall_risk_score >= 6

    # 2. No contradiction between risk and competition
    top_opt = report.release_strategy.ranked_release_options[0]
    assert top_opt.competition_level != "Clear Runway"
    assert "Sunday" in top_opt.slot_type or "Sunday" in report.calendar_analysis.clashes_and_events[0].description
    assert "Long Extended Weekend" not in top_opt.slot_type

    # 3. Numeric spread without doubled symbols
    assert "₹₹" not in report.comps_analysis.performance_spread
    assert "Cr to" in report.comps_analysis.performance_spread

    # 4. Marketing reflects logline
    slogan = report.marketing_playbook.campaign_slogan_or_theme.lower()
    assert "enemy lines" in slogan or "duty" in slogan or "agniveer" in slogan

    # 5. Critic credibility score is realistic and counts match
    assert report.critic_audit.credibility_score < 95
    assert report.critic_audit.verdict == "Approved with Inferences"
    assert report.critic_audit.verified_claims_count < report.critic_audit.total_claims_checked
    assert "Formula:" in report.critic_audit.score_formula_breakdown

    # 6. Option 2 check
    opt2 = report.release_strategy.ranked_release_options[1]
    assert "September 3, 2027" in opt2.proposed_date
    assert "Unknown" in opt2.competition_level or "Unannounced" in opt2.competition_level

    # 7. Brahmastra check
    comp_titles = [c.title.lower() for c in report.comps_analysis.comparables]
    assert not any("brahmāstra" in t or "brahmastra" in t for t in comp_titles)

    # 8. Real timer check
    assert report.metadata.get("execution_time_seconds", 0) > 0.1
    assert "execution_time_formatted" in report.metadata

    print("\n[TEST PASSED] Project Agniveer regression test passed with 0 contradictions!")

if __name__ == "__main__":
    asyncio.run(test_jawan_pipeline_execution())
    asyncio.run(test_project_agniveer_consistency_and_credibility())
