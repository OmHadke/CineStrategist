"""
Agent 4: Release Window & Distribution Strategist.
Ranks release date options, calculates screen counts, defines theatrical-to-OTT holdback windows,
and formulates pan-India distribution policies.
"""

from typing import List
from app.models.schemas import FilmInput, CompsAnalysis, CalendarAnalysis, AudienceAnalysis, ReleaseStrategy, ReleaseOption
from app.services.llm_service import llm_service

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
            screen_est = "3,000 - 3,800 screens across India + 600 overseas"
        else:
            screen_est = "1,800 - 2,500 screens across India (targeted multiplex release with targeted single screens)"

        # Formulate Ranked Options
        window = film_input.planned_window
        options: List[ReleaseOption] = [
            ReleaseOption(
                rank=1,
                proposed_date=f"Primary Window ({window})",
                slot_type="Solo National Holiday" if calendar.overall_risk_score <= 4 else "Long Extended Weekend",
                screen_count_est=screen_est,
                competition_level="Direct Tentpole Clash" if calendar.overall_risk_score >= 7 else "Clear Runway",
                pros=[
                    f"Capitalizes on festive or weekend footfall synergies identified in {window}",
                    f"Allows full deployment of {screen_est} before subsequent tentpole arrivals",
                    "Maximizes day-1 and weekend-1 opening capacity"
                ],
                cons=[
                    "High advertising inventory competition during peak windows",
                    "Requires firm adherence to promotional delivery timeline"
                ],
                strategic_rationale=f"Primary recommendation aligned with user timeline. Offers best alignment with {audience.positioning_hook}"
            ),
            ReleaseOption(
                rank=2,
                proposed_date=f"Counter-Corridor (+2 Weeks Post-{window})",
                slot_type="Counter-Programming Window",
                screen_count_est=f"Targeted {screen_est.split()[0]} screens",
                competition_level="Manageable Counter-Release",
                pros=[
                    "Escapes initial week-1 tentpole marketing noise",
                    "Lower distributor revenue share demands and cheaper print/marketing ad rates",
                    "Higher share of premium IMAX/4DX screens as earlier releases taper off"
                ],
                cons=[
                    "Misses initial national holiday footfall multiplier",
                    "Relies heavily on positive word-of-mouth momentum"
                ],
                strategic_rationale="Strategic fallback in case competing studio enforces aggressive day-and-date screen blocking."
            )
        ]

        # OTT Windowing compliance
        ott_window = {
            "theatrical_holdback_weeks": 8,
            "industry_norm_compliance": "Strict PVR-INOX & Multiplex Association of India (MAI) 8-Week Window Accord",
            "recommended_ott_partners": ["Netflix India", "Prime Video", "JioCinema"],
            "rationale": (
                "Under current national multiplex agreements, any Hindi or Pan-Indian theatrical release with less than an "
                "8-week holdback faces total screen boycotts by PVR-INOX and Cinepolis. A disciplined 56-day theatrical run "
                "protects repeat footfalls before monetization on premier SVOD tiers."
            )
        }

        # Pan-India plan
        pan_india_plan = (
            "Multi-language day-and-date release in Hindi, Telugu, and Tamil. Secure prominent South distributor partnerships "
            "(e.g., Mythri Movie Makers, Red Giant, or Sri Venkateswara) for single-screen saturation across Andhra, Telangana, and Tamil Nadu. "
            "Host separate audio/trailer launches in Hyderabad and Chennai to establish regional cultural resonance."
            if film_input.pan_india or film_input.budget_tier == "mega"
            else "Focus 85% distribution footprint on North, Central, and West circuits (Delhi-UP, East Punjab, Mumbai, CP-CI). Deploy subtitled original version in South metros (Bengaluru, Hyderabad, Kochi) without dub dilution."
        )

        return ReleaseStrategy(
            ranked_release_options=options,
            screen_distribution_strategy=(
                f"Distribute {screen_est}. Maintain a 60/40 multiplex-to-single-screen split in Tier-1 metros, "
                f"and pivot to 70% single-screen allocation in Tier-2/3 Mass Heartland circuits."
            ),
            ott_windowing=ott_window,
            pan_india_distribution_plan=pan_india_plan
        )

strategy_agent = StrategyAgent()
