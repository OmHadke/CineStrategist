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

if __name__ == "__main__":
    asyncio.run(test_jawan_pipeline_execution())
