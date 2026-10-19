import asyncio
import pytest
from app.models.schemas import FilmInput
from app.orchestrator import orchestrator

def run(**kw):
    return asyncio.run(orchestrator.run_pipeline(FilmInput(**kw), bypass_cache=True))

def test_romance_has_no_military_text():
    r = run(
        title="T1",
        genres=["Romance", "Drama"],
        language="Hindi",
        budget_tier="mid",
        star_tier="tier_1",
        director="",
        target_audience="Urban youth",
        planned_window="Valentine's Week 2027",
        logline="An architect returns home and falls for a conservator.",
        platforms="theatrical",
        pan_india=True
    )
    # Strategy checks
    assert "military" not in r.release_strategy.pan_india_distribution_plan.lower()
    assert "combat" not in r.release_strategy.pan_india_distribution_plan.lower()
    
    # Calendar checks: 2027 date, Feb 14 = Sunday, board-exam note
    first_event = r.calendar_analysis.clashes_and_events[0]
    assert "2027" in first_event.date
    assert "sunday" in first_event.date.lower() or "sunday" in first_event.description.lower()
    
    exam_clash = any("exam" in c.event_type.lower() or "exam" in c.event_name.lower() for c in r.calendar_analysis.clashes_and_events)
    assert exam_clash, "Board exam season must be flagged for Valentine's Week"
    
    # Comps check: at least one underperformer / downside case
    verdicts = [c.verdict.lower() for c in r.comps_analysis.comparables]
    assert any(v in ["average", "flop", "below average"] for v in verdicts), "Must include at least one underperforming romance comp"

def test_star_budget_mismatch_warns():
    r = run(
        title="T3b",
        genres=["Comedy", "Social"],
        language="Hindi",
        budget_tier="low",
        star_tier="tier_1",
        director="",
        target_audience="Urban",
        planned_window="Q3 2027",
        logline="Chawl eviction goes viral.",
        platforms="theatrical",
        pan_india=False
    )
    assert r.comps_analysis.configuration_warnings
    assert any("star" in w.lower() and "budget" in w.lower() for w in r.comps_analysis.configuration_warnings)

def test_war_action_test2_agniveer():
    r = run(
        title="Project Agniveer",
        genres=["Action", "Thriller", "War"],
        language="Hindi",
        budget_tier="mega",
        star_tier="tier_1",
        director="Test Director A",
        target_audience="Mass heartland single-screens, patriotic family audiences, urban multiplexes",
        planned_window="Independence Day 2027",
        logline="During a cross-border crisis, a special forces officer must lead a covert mission behind enemy lines with a team he doesn't trust. Part war film, part spy thriller, with large-scale action set pieces and an emotional core about duty versus family.",
        platforms="theatrical",
        pan_india=True
    )
    # Aug 15 = Sunday
    first_clash = r.calendar_analysis.clashes_and_events[0]
    assert "2027-08-15" in first_clash.date
    assert "sunday" in first_clash.date.lower() or "sunday" in first_clash.description.lower()
    
    # Runway must NOT say 'Clear Runway'
    top_option = r.release_strategy.ranked_release_options[0]
    assert "clear runway" not in top_option.competition_level.lower()
    assert "contested" in top_option.competition_level.lower() or "unknown" in top_option.competition_level.lower()
    
    # No romance beats in marketing
    for beat in r.marketing_playbook.timeline_beats:
        assert "romantic ballad" not in beat.title.lower()
        assert "romantic duet" not in beat.title.lower()
        
    # Comps within mega/high budget tier (no Brahmāstra, no ₹65 Cr / ₹100 Cr low budget comps)
    for comp in r.comps_analysis.comparables:
        assert comp.title != "Brahmāstra: Part One – Shiva"
        assert comp.title != "Shaitaan"
        assert comp.title != "Animal"
    assert len(r.comps_analysis.comparables) >= 4

def test_low_budget_no_flat_kpis_test3():
    r = run(
        title="Test 3 Low Budget Comedy",
        genres=["Comedy", "Social"],
        language="Hindi",
        budget_tier="low",
        star_tier="fresh_faces",
        director="",
        target_audience="Urban, college and OTT-first",
        planned_window="Q3 2027",
        logline="A chawl redevelopment project sparks a viral grassroots community movement.",
        platforms="theatrical",
        pan_india=False
    )
    # Independence Day inside the Q3 window
    events = [c.event_name.lower() for c in r.calendar_analysis.clashes_and_events]
    assert any("independence" in e for e in events)
    
    # Phased screen distribution for low budget
    assert "600 - 900" in r.release_strategy.ranked_release_options[1].screen_count_est or "800 - 1,200" in r.release_strategy.screen_distribution_strategy
    
    # No 75M+ views or ₹10 Cr+ pre-sales in marketing KPIs
    for beat in r.marketing_playbook.timeline_beats:
        assert "75m+" not in beat.kpi_metric.lower()
        assert "₹10 cr+" not in beat.kpi_metric.lower()
        assert "₹15cr+" not in beat.kpi_metric.lower()
        assert "illustrative" in beat.kpi_metric.lower() or "heuristic" in beat.kpi_metric.lower() or "benchmark" in beat.kpi_metric.lower()

def test_edge_cases_handling():
    # Edge case 1: 4 genres
    r_4g = run(
        title="Multi-Genre Edge",
        genres=["Action", "Thriller", "Sci-Fi", "Drama"],
        language="Hindi",
        budget_tier="high",
        star_tier="tier_2",
        director="",
        target_audience="Multiplex youth",
        planned_window="Q4 2026",
        logline="A scientist discovers an anomaly in space that threatens earth.",
        platforms="theatrical",
        pan_india=False
    )
    assert len(r_4g.comps_analysis.comparables) > 0

    # Edge case 2: 0 genres
    r_0g = run(
        title="Zero-Genre Edge",
        genres=[],
        language="Hindi",
        budget_tier="mid",
        star_tier="tier_2",
        director="",
        target_audience="General audience",
        planned_window="Q1 2027",
        logline="A small town teacher uncovers a financial conspiracy.",
        platforms="theatrical",
        pan_india=False
    )
    assert len(r_0g.comps_analysis.comparables) > 0

    # Edge case 3: Blank director handled cleanly
    assert r_0g.film_input.director == ""

    # Edge case 4: Vague window ("sometime next year")
    r_vague = run(
        title="Vague Window Film",
        genres=["Drama"],
        language="Hindi",
        budget_tier="mid",
        star_tier="tier_2",
        director="A. Director",
        target_audience="General",
        planned_window="sometime next year",
        logline="An emotional homecoming story.",
        platforms="theatrical",
        pan_india=False
    )
    assert len(r_vague.calendar_analysis.clashes_and_events) > 0

    # Edge case 5: Past window ("Diwali 2024")
    r_past = run(
        title="Past Window Film",
        genres=["Action"],
        language="Hindi",
        budget_tier="mega",
        star_tier="tier_1",
        director="Director X",
        target_audience="Mass",
        planned_window="Diwali 2024",
        logline="Undercover cop takes on an international syndicate.",
        platforms="theatrical",
        pan_india=True
    )
    assert any("retrospective" in w.lower() or "historical" in w.lower() for w in r_past.calendar_analysis.hazard_warnings)

    # Edge case 6: Language other than Hindi
    r_tamil = run(
        title="Tamil Feature",
        genres=["Action", "Drama"],
        language="Tamil",
        budget_tier="mid",
        star_tier="tier_2",
        director="Mani R.",
        target_audience="Tamil Nadu + diaspora",
        planned_window="Pongal 2027",
        logline="A rural leader protects agricultural land from an industrial conglomerate.",
        platforms="theatrical",
        pan_india=False
    )
    assert "tamil" in r_tamil.release_strategy.pan_india_distribution_plan.lower()
    assert "target hindi original release" not in r_tamil.release_strategy.pan_india_distribution_plan.lower()

@pytest.mark.asyncio
async def test_concurrency_two_simultaneous_reports():
    input1 = FilmInput(
        title="Concurrent Film A",
        genres=["Action"],
        language="Hindi",
        budget_tier="high",
        star_tier="tier_1",
        target_audience="Mass",
        planned_window="Diwali 2026",
        logline="Action thriller A."
    )
    input2 = FilmInput(
        title="Concurrent Film B",
        genres=["Romance"],
        language="Hindi",
        budget_tier="mid",
        star_tier="tier_2",
        target_audience="Youth",
        planned_window="Valentine's Week 2027",
        logline="Romantic drama B."
    )
    r1, r2 = await asyncio.gather(
        orchestrator.run_pipeline(input1, bypass_cache=True),
        orchestrator.run_pipeline(input2, bypass_cache=True)
    )
    assert r1.film_input.title == "Concurrent Film A"
    assert r2.film_input.title == "Concurrent Film B"
    assert r1.report_id != r2.report_id
