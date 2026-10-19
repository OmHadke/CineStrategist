"""
Agent 4: Release Window & Distribution Strategist.
Ranks release date options with strict consistency enforcement between risk scores and competition labels.
Integrates calendar weekday realities (e.g. Sunday holidays) and genre-specific distribution footprints.
"""

from typing import List
import re
from datetime import date, timedelta
import calendar
from app.models.schemas import FilmInput, CompsAnalysis, CalendarAnalysis, AudienceAnalysis, ReleaseStrategy, ReleaseOption

class StrategyAgent:
    async def run(
        self, 
        film_input: FilmInput, 
        comps: CompsAnalysis, 
        calendar_analysis: CalendarAnalysis, 
        audience: AudienceAnalysis
    ) -> ReleaseStrategy:
        
        # Screen count calculation based on star tier and budget
        if film_input.budget_tier == "mega" and film_input.star_tier in ["tier_1", "mega"]:
            screen_est = "4,500 - 5,200 screens across India + 1,200 overseas"
            opt2_screens = "3,800 - 4,200 screens"
        elif film_input.budget_tier in ["mega", "high"] or film_input.star_tier == "tier_1":
            screen_est = "3,200 - 3,800 screens across India + 600 overseas"
            opt2_screens = "2,600 - 3,000 screens"
        elif film_input.budget_tier == "mid":
            screen_est = "1,800 - 2,400 screens across India + 350 overseas"
            opt2_screens = "1,400 - 1,800 screens"
        else: # Low budget / Indie / Niche
            screen_est = "800 - 1,200 screens across India (Phased Platform Multiplex Rollout)"
            opt2_screens = "600 - 900 screens (Targeted Word-of-Mouth Footprint)"

        # Consistency Rule: Competition Level derived strictly from Calendar Risk Score
        risk_score = calendar_analysis.overall_risk_score
        if risk_score >= 8:
            comp_level = "Direct Tentpole Clash"
            slot_type = "High-Risk Festive Clash"
        elif risk_score >= 6:
            comp_level = "Contested Runway (Unannounced Future Slate)"
            slot_type = "Contested Festive Corridor"
        elif risk_score >= 4:
            comp_level = "Manageable Counter-Release"
            slot_type = "Commercial Corridor"
        else:
            comp_level = "Clear Runway"
            slot_type = "Solo Holiday / Open Window"

        window = film_input.planned_window
        year_match = re.search(r'\b(202[4-9]|203[0-5])\b', window)
        year = int(year_match.group(1)) if year_match else 2026

        # Determine exact dates and weekend structure
        is_independence = "independence" in window.lower() or "aug" in window.lower()
        is_valentine = any(w in window.lower() for w in ["valentine", "feb 14", "14 feb", "february"])

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
        elif is_valentine:
            d_val = date(year, 2, 14)
            day_val_name = calendar.day_name[d_val.weekday()]
            proposed_date_1 = f"Friday, February 12, {year} (Opening into Valentine's Weekend Sunday Feb 14)"
            slot_type_1 = "Commercial Thematic Date-Night Corridor"
            pros_1 = [
                f"High-density commercial date-night footfall surge on {day_val_name}, Feb 14",
                "Maximum youth and couple ticket elasticity across premium urban multiplexes",
                "Ideal promotional window for music-driven marketing momentum"
            ]
            cons_1 = [
                f"Feb 14 falls on a {day_val_name}, offering zero gazetted weekday holiday buffer",
                "National secondary/higher board exam season (CBSE/ICSE) depresses weekday student afternoon footfalls"
            ]
        else:
            proposed_date_1 = f"Primary Corridor ({window})"
            slot_type_1 = slot_type
            pros_1 = [f"Capitalizes on targeted window ({window})", "Early advance sales runway"]
            cons_1 = ["Advertising inventory cost inflation during peak festive corridors"]

        # Option 2 Real Date Calculation: Friday ~3 weeks post-window
        if is_independence:
            d_base = date(year, 8, 15)
            days_ahead = (4 - d_base.weekday()) % 7
            if days_ahead <= 0:
                days_ahead += 7
            opt2_date_obj = d_base + timedelta(days=days_ahead + 14)
            opt2_day_name = calendar.day_name[opt2_date_obj.weekday()]
            opt2_date_str = f"{opt2_day_name}, {opt2_date_obj.strftime('%B')} {opt2_date_obj.day}, {opt2_date_obj.year}"
            opt2_slot_type = "Post-Festive Buffer Corridor"
        elif is_valentine:
            d_base = date(year, 2, 14)
            days_ahead = (4 - d_base.weekday()) % 7
            if days_ahead <= 0:
                days_ahead += 7
            opt2_date_obj = d_base + timedelta(days=days_ahead + 14)
            opt2_day_name = calendar.day_name[opt2_date_obj.weekday()]
            opt2_date_str = f"{opt2_day_name}, {opt2_date_obj.strftime('%B')} {opt2_date_obj.day}, {opt2_date_obj.year}"
            opt2_slot_type = "Post-Valentine Counter-Programming Window"
        else:
            opt2_date_str = f"Post-Window Corridor (+3 Weeks Post-{window})"
            opt2_slot_type = "Counter-Programming Window"

        opt2_comp_level = "Unknown / Unconfirmed Runway (Future Slate Unannounced)" if year >= 2026 else "Historical Counter-Programming Slot"

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
                    f"and vigilance against competitor announcements, the corridor footfall multiplier offers the highest opening velocity."
                )
            ),
            ReleaseOption(
                rank=2,
                proposed_date=opt2_date_str,
                slot_type=opt2_slot_type,
                screen_count_est=opt2_screens,
                competition_level=opt2_comp_level,
                pros=[
                    "Completely avoids initial festive tentpole collision noise and screen-sharing disputes",
                    "Lower exhibitor commission terms and cheaper broadcast marketing rates",
                    "Targeted screen allocation ensures higher seat-occupancy ratios"
                ],
                cons=[
                    "Foregoes the initial holiday/thematic weekend single-day surge",
                    f"Competitor slate for late corridor {year} is unannounced, requiring ongoing exhibitor intelligence"
                ],
                strategic_rationale=(
                    f"Contingency escape window scheduled for {opt2_date_str}. While future competitor slates "
                    f"remain unannounced, historical scheduling patterns indicate lower collision risk following the primary corridor rush."
                )
            )
        ]

        # Check genre themes for distribution strategy
        is_war_spy = any(g.lower() in ["war", "action", "thriller"] for g in film_input.genres)
        is_low_budget = film_input.budget_tier == "low"

        if is_war_spy and not is_low_budget:
            dist_strategy = (
                f"Distribute across {screen_est}. Prioritize 65% single-screen footprint in North & Central heartland circuits "
                f"(Delhi-UP, East Punjab, Rajasthan, CP-CI) where armed forces and patriotic themes command historically higher "
                f"ticket density. Reserve 35% capacity for Tier-1 premium multiplexes (IMAX/4DX) to showcase tactical combat scale."
            )
        elif is_low_budget:
            dist_strategy = (
                f"Deploy a phased platform rollout starting across {screen_est} in metro urban hubs and university clusters. "
                f"Leverage high opening-weekend occupancy (>65%) to compel national multiplex chains (PVR-INOX, Cinepolis) to expand screen allocations into Tier-2 centers in Week 2."
            )
        else:
            dist_strategy = (
                f"Distribute across {screen_est}. Maintain balanced 50/50 multiplex-to-single-screen allocation across all major territories."
            )

        ott_window = {
            "theatrical_holdback_weeks": 8,
            "industry_norm_compliance": "Typical ~8-Week Multiplex Theatrical Window Norm",
            "recommended_ott_partners": ["Netflix India", "Prime Video", "JioCinema"],
            "rationale": (
                "Under prevailing Indian theatrical practice, major national multiplex chains (PVR-INOX, Cinepolis) "
                "observe a typical ~8-week (56-day) theatrical exclusivity window before SVOD premiere. "
                "Studio distributors should confirm specific contractual holdback terms directly with exhibitors during final booking agreements."
            )
        }

        # Dynamic, context-aware Pan-India Plan
        if film_input.language.lower() != "hindi":
            if film_input.pan_india:
                pan_india_plan = (
                    f"Lead with dominant distribution in {film_input.language} home territories, and deploy day-and-date dubbed releases "
                    f"in Hindi (North multiplexes) and other key linguistic circuits, supported by nationwide publicity tours."
                )
            else:
                pan_india_plan = (
                    f"Prioritize maximum screen density across primary {film_input.language} territories. Limit outside-market footprint "
                    f"to original-language subtitled prints in Tier-1 metro multiplexes (Mumbai, Delhi-NCR, Bengaluru) to avoid marketing leakage."
                )
        elif is_war_spy and (film_input.pan_india or film_input.budget_tier == "mega"):
            pan_india_plan = (
                "Deploy multi-lingual day-and-date dubbed releases in Telugu and Tamil. Partner with a prominent South distributor "
                "(e.g. Mythri Movie Makers or Asian Cinemas) for Telugu states (Nizam/Andhra) where high-octane combat action set-pieces resonate strongly."
            )
        elif film_input.pan_india:
            pan_india_plan = (
                "Deploy localized dubbed releases in Telugu and Tamil across South metropolitan circuits, supported by regional celebrity trailer launches and localized marketing assets."
            )
        elif film_input.budget_tier == "low":
            pan_india_plan = (
                "Target Hindi original release with English subtitles in South metro multiplexes (Bengaluru, Hyderabad, Chennai, Kochi). "
                "Avoid dilutive regional dubbing expenses; monetize South regional demand via post-theatrical multi-lingual OTT/satellite streaming agreements."
            )
        else:
            pan_india_plan = (
                "Target Hindi original release with English subtitles across South metros (Bengaluru, Hyderabad, Kochi). Avoid regional dubbed dilutive theatrical costs."
            )

        return ReleaseStrategy(
            ranked_release_options=options,
            screen_distribution_strategy=dist_strategy,
            ott_windowing=ott_window,
            pan_india_distribution_plan=pan_india_plan
        )

strategy_agent = StrategyAgent()
