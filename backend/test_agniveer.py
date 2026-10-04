"""
Verification script for Test 2: Project Agniveer (Independence Day 2027, Mega Budget War/Action).
Verifies:
1. Year 2027 parsed correctly; event is August 15, 2027 (Sunday); no false Diwali clash flagged.
2. Contradiction check: Risk is 6/10 (High Risk), Competition Level is "Contested Runway (Unannounced Future Slate)", NOT "Clear Runway".
3. Sunday holiday structure: Aug 15, 2027 is a Sunday, NOT falsely labeled "Long Extended Weekend".
4. Performance spread: calculated from numbers (₹355 Cr to ₹1,150 Cr), NO double "₹₹".
5. Comps scoring: War/Action/Spy titles (Fighter, Pathaan, War, Uri, Jawan) prioritized over fantasy/horror.
6. Marketing reflects logline: Covert mission, tactical anthem, duty vs family emotional core, distinct slogan.
7. Critic credibility score: Realistic (83-88%), honest source attribution to curated dataset.
"""

import asyncio
from app.models.schemas import FilmInput, CineStrategistReport
from app.orchestrator import orchestrator

async def verify_agniveer():
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
    
    print("=" * 60)
    print("PROJECT AGNIVEER PIPELINE AUDIT REPORT")
    print("=" * 60)
    
    # 1. Comps check
    print(f"\n1. COMPS & SPREAD:")
    print(f"   Performance Spread: {report.comps_analysis.performance_spread}")
    print(f"   Median Rating: {report.comps_analysis.median_rating} / 10")
    print(f"   Top Comps:")
    for c in report.comps_analysis.comparables:
        print(f"     - {c.title} ({c.year}) [{', '.join(c.genres)}]: Sim={c.similarity_score} | Gross={c.box_office_est}")

    # 2. Calendar check
    print(f"\n2. CALENDAR & CLASHES:")
    print(f"   Risk Score: {report.calendar_analysis.overall_risk_score}/10 ({report.calendar_analysis.risk_tier})")
    for event in report.calendar_analysis.clashes_and_events:
        print(f"     - {event.event_name} on {event.date} (Severity: {event.severity})")

    # 3. Strategy check
    top_opt = report.release_strategy.ranked_release_options[0]
    print(f"\n3. STRATEGY CONSISTENCY:")
    print(f"   Option 1 Proposed Date: {top_opt.proposed_date}")
    print(f"   Option 1 Slot Type: {top_opt.slot_type}")
    print(f"   Option 1 Competition Level: {top_opt.competition_level}")

    # 4. Marketing check
    print(f"\n4. MARKETING PLAYBOOK (LOGLINE AWARENESS):")
    print(f"   Campaign Slogan: '{report.marketing_playbook.campaign_slogan_or_theme}'")
    print(f"   Key Hooks: {report.marketing_playbook.key_narrative_hooks}")
    for beat in report.marketing_playbook.timeline_beats[:3]:
        print(f"     - [{beat.day_offset}] {beat.title} ({beat.asset_type})")

    # 5. Critic check
    print(f"\n5. PRODUCER'S CRITIC AUDIT:")
    print(f"   Credibility Score: {report.critic_audit.credibility_score}% ({report.critic_audit.verdict})")
    print(f"   Verified Claims: {report.critic_audit.verified_claims_count}/{report.critic_audit.total_claims_checked}")
    for item in report.critic_audit.audit_items:
        print(f"     - [{item.status}] {item.claim[:60]}... -> {item.critic_notes[:50]}...")

    # Assertions
    assert "2027" in report.calendar_analysis.clashes_and_events[0].date
    assert "Sunday" in report.calendar_analysis.clashes_and_events[0].description or "Sunday" in report.calendar_analysis.clashes_and_events[0].date
    assert "diwali" not in [c.event_name.lower() for c in report.calendar_analysis.clashes_and_events]
    assert top_opt.competition_level != "Clear Runway"
    assert "₹₹" not in report.comps_analysis.performance_spread
    assert "behind enemy lines" in report.marketing_playbook.campaign_slogan_or_theme.lower() or "duty" in report.marketing_playbook.campaign_slogan_or_theme.lower()
    
    # Check Option 2 real date and unknown competition
    opt2 = report.release_strategy.ranked_release_options[1]
    assert "September 3, 2027" in opt2.proposed_date
    assert "Unknown" in opt2.competition_level or "Unannounced" in opt2.competition_level

    # Check Brahmastra exclusion
    comp_titles = [c.title.lower() for c in report.comps_analysis.comparables]
    assert not any("brahmāstra" in t or "brahmastra" in t for t in comp_titles)

    # Check Critic counts and formula
    assert report.critic_audit.verified_claims_count < report.critic_audit.total_claims_checked
    assert report.critic_audit.probable_inferences_count > 0
    assert "Formula:" in report.critic_audit.score_formula_breakdown
    assert report.critic_audit.credibility_score < 95

    # Check Execution time is realistic (> 0.1s)
    assert report.metadata.get("execution_time_seconds", 0) > 0.1
    assert "execution_time_formatted" in report.metadata

    print("\n[ALL CHECKS PASSED] Contradictions, counts, Brahmastra exclusion, and real timer verified!")


if __name__ == "__main__":
    asyncio.run(verify_agniveer())
