"""
Agent 4: Release Window & Distribution Strategist.
Ranks release date options with strict consistency enforcement between risk scores and competition labels.
Integrates calendar weekday realities (e.g. Sunday holidays) and genre-specific distribution footprints.
"""

from typing import List
import re
from app.models.schemas import FilmInput, CompsAnalysis, CalendarAnalysis, AudienceAnalysis, ReleaseStrategy, ReleaseOption

class StrategyAgent:
    async def run(
        self, 
        film_input: FilmInput, 
        comps: CompsAnalysis, 
        calendar: CalendarAnalysis, 
        audience: AudienceAnalysis
    ) -> ReleaseStrategy:
        
        # Screen count calculation based on star tier and budget
        if film_input.budget_tier in ["mega", "high"] and film_input.star_tier in ["tier_1", "mega"]:
            screen_est = "4,500 - 5,200 screens across India + 1,200 overseas"
        elif film_input.budget_tier == "high" or film_input.star_tier == "tier_2":
            screen_est = "3,200 - 3,800 screens across India + 600 overseas"
        else:
            screen_est = "2,000 - 2,500 screens across India (targeted multiplex release with targeted single screens)"

        # Consistency Rule: Competition Level derived strictly from Calendar Risk Score
        risk_score = calendar.overall_risk_score
        if risk_score >= 8:
            comp_level = "Direct Tentpole Clash"
            slot_type = "High-Risk Festive Clash"
        elif risk_score >= 6:
            comp_level = "Contested Runway (Unannounced Future Slate)"
            slot_type = "Contested Festive Corridor"
        elif risk_score >= 4:
            comp_level = "Manageable Counter-Release"
            slot_type = "Long Extended Weekend"
        else:
            comp_level = "Clear Runway"
            slot_type = "Solo National Holiday"

        window = film_input.planned_window
        year_match = re.search(r'\b(202[4-9]|203[0-5])\b', window)
        year = int(year_match.group(1)) if year_match else 2026

        # Determine exact dates and weekend structure
        is_independence = "independence" in window.lower() or "aug" in window.lower()
        if is_independence and year == 2027:
            # 2027-08-15 is Sunday!
            proposed_date_1 = f"Friday, August 13, {year} (Opening into Sunday Aug 15 National Holiday)"
            slot_type_1 = "Standard 3-Day Weekend (Sunday Peak Holiday Climax)"
            pros_1 = [
                f"Capitalizes on Independence Day national patriotism peak on Sunday, August 15, {year}",
                "Leverages maximum armed forces and family theatrical affinity in North and Central India",
                f"Allows deployment of full {screen_est.split()[0]} screen footprint before late-August entries"
            ]
            cons_1 = [
                f"Aug 15 falls on Sunday, so there is NO extra Monday/Friday gazetted holiday cushion — standard 3-day window",
                f"Historically high competition corridor: unannounced {year} competitor tentpoles are likely to announce for this date",
                "High risk of single-screen capacity splitting if a second commercial tentpole enters the frame"
            ]
        elif is_independence:
            proposed_date_1 = f"August 14, {year} (Independence Day Corridor)"
            slot_type_1 = "National Holiday Corridor"
            pros_1 = [f"Direct holiday footfall multiplier ({year})", "Patriotic sentiment surge"]
            cons_1 = ["Competitor collision risk in prime release window"]
        else:
            proposed_date_1 = f"Primary Corridor ({window})"
            slot_type_1 = slot_type
            pros_1 = [f"Capitalizes on proposed window ({window})", "Early advance sales runway"]
            cons_1 = ["Advertising inventory cost inflation during peak festive windows"]

        options: List[ReleaseOption] = [
            ReleaseOption(
                rank=1,
                proposed_date=proposed_date_1,
                slot_type=slot_type_1,
                screen_count_est=screen_est,
                competition_level=comp_level,
                pros=pros_1,
                cons=cons_1,
                strategic_rationale=(
                    f"Primary corridor targeted by studio. While {comp_level.lower()} requires proactive marketing "
                    f"and vigilance against competitor announcements, the national holiday footfall multiplier offers the highest opening velocity."
                )
            ),
            ReleaseOption(
                rank=2,
                proposed_date=f"Buffer Corridor (+3 Weeks Post-{window})",
                slot_type="Counter-Programming Window",
                screen_count_est=f"3,800 - 4,200 screens",
                competition_level="Clear Runway",
                pros=[
                    "Completely avoids initial holiday tentpole collision noise and screen-sharing disputes",
                    "Lower exhibitor commission terms and cheaper broadcast marketing rates",
                    "Allows full 100% control of premium IMAX, 4DX, and ICE screens across metro circuits"
                ],
                cons=[
                    "Foregoes the initial Independence Day national holiday single-day surge",
                    "Requires reliance on trailer-driven organic curiosity rather than festive holiday footfalls"
                ],
                strategic_rationale="Contingency escape window in the event that a competing studio locks in an aggressive day-and-date release."
            )
        ]

        # Check genre themes for distribution strategy
        is_war_spy = any(g.lower() in ["war", "action", "thriller"] for g in film_input.genres)
        if is_war_spy:
            dist_strategy = (
                f"Distribute across {screen_est}. Prioritize 65% single-screen footprint in North & Central heartland circuits "
                f"(Delhi-UP, East Punjab, Rajasthan, CP-CI) where armed forces and patriotic themes command historically higher "
                f"ticket density. Reserve 35% capacity for Tier-1 premium multiplexes (IMAX/4DX) to showcase tactical combat scale."
            )
        else:
            dist_strategy = (
                f"Distribute across {screen_est}. Maintain balanced 50/50 multiplex-to-single-screen allocation across all major territories."
            )

        ott_window = {
            "theatrical_holdback_weeks": 8,
            "industry_norm_compliance": "Strict PVR-INOX & Multiplex Association of India (MAI) 8-Week Window Accord",
            "recommended_ott_partners": ["Netflix India", "Prime Video", "JioCinema"],
            "rationale": (
                "National cinema chains strictly enforce an 8-week (56-day) holdback. Any theatrical release violating this norm "
                "is barred from multiplex distribution. A disciplined holdback maximizes repeat visits and strengthens digital streaming valuation."
            )
        }

        pan_india_plan = (
            "Deploy multi-lingual day-and-date dubbed releases in Telugu and Tamil. For a military action thriller, "
            "partner with a prominent South distributor (e.g. Mythri Movie Makers or Asian Cinemas) for Telugu states (Nizam/Andhra) "
            "where mass combat set-pieces resonate strongly."
            if film_input.pan_india or film_input.budget_tier == "mega"
            else "Target Hindi original release with English subtitles in South metros (Bengaluru, Hyderabad, Kochi). Avoid regional dubbed dilutive costs."
        )

        return ReleaseStrategy(
            ranked_release_options=options,
            screen_distribution_strategy=dist_strategy,
            ott_windowing=ott_window,
            pan_india_distribution_plan=pan_india_plan
        )

strategy_agent = StrategyAgent()
