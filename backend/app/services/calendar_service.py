"""
Enhanced Calendar and Release Clash Evaluation Service.
Dynamically extracts target year, calculates exact calendar days (e.g. Sunday Aug 15, 2027),
filters strictly to the requested theatrical window, and models unannounced future slates.
"""

import re
from datetime import date
import calendar
from typing import Dict, Any, List, Tuple
from app.data.festivals import MOVEABLE_FESTIVALS, FIXED_HOLIDAYS, get_holiday_details
from app.models.schemas import CalendarClash, CalendarAnalysis

class CalendarService:
    def _extract_year_and_window(self, planned_window: str) -> Tuple[int, str]:
        # Extract 4-digit year (e.g. 2020 to 2039)
        year_match = re.search(r'\b(20[1-3][0-9])\b', planned_window)
        current_year = date.today().year
        if year_match:
            year = int(year_match.group(1))
        elif "next year" in planned_window.lower():
            year = current_year + 1
        elif "this year" in planned_window.lower():
            year = current_year
        else:
            year = 2026

        window_lower = planned_window.lower()
        if any(w in window_lower for w in ["valentine", "feb 14", "14 feb", "february"]):
            target_window = "valentine"
        elif any(w in window_lower for w in ["independence", "aug", "15 aug"]):
            target_window = "independence_day"
        elif any(w in window_lower for w in ["republic", "jan", "26 jan"]):
            target_window = "republic_day"
        elif any(w in window_lower for w in ["diwali", "deepavali"]):
            target_window = "diwali"
        elif any(w in window_lower for w in ["christmas", "xmas", "dec", "new year"]):
            target_window = "christmas"
        elif any(w in window_lower for w in ["eid", "ramadan"]):
            target_window = "eid"
        elif any(w in window_lower for w in ["ipl", "cricket"]):
            target_window = "ipl"
        elif any(w in window_lower for w in ["gandhi", "2 oct", "october"]):
            target_window = "gandhi_jayanti"
        elif "q3" in window_lower:
            target_window = "q3"
        elif "q1" in window_lower:
            target_window = "q1"
        elif "q2" in window_lower:
            target_window = "q2"
        elif "q4" in window_lower:
            target_window = "q4"
        else:
            target_window = "custom"

        return year, target_window

    def evaluate_window(self, planned_window: str, genres: List[str]) -> CalendarAnalysis:
        year, target_window = self._extract_year_and_window(planned_window)
        current_year = date.today().year
        clashes: List[CalendarClash] = []
        synergies: List[str] = []
        warnings: List[str] = []

        if year < current_year:
            warnings.append(
                f"Historical Retrospective Window: '{planned_window}' is a past release window ({year} < {current_year}). "
                f"Analysis is operating in retrospective backtest mode."
            )

        is_future_unannounced = year >= 2026

        if target_window == "valentine":
            d = date(year, 2, 14)
            day_name = calendar.day_name[d.weekday()]
            
            if d.weekday() == 6: # Sunday
                weekend_structure = (
                    f"Valentine's Day ({day_name}, Feb 14, {year}). High-density commercial date-night demand concentrated "
                    f"on Sunday evening. Standard 3-day opening weekend (Fri Feb 12 - Sun Feb 14) with standard Monday drop-off (NOT a gazetted holiday)."
                )
            else:
                weekend_structure = (
                    f"Valentine's Day ({day_name}, Feb 14, {year}). Mid-week commercial date-night bump; theatrical footfalls peak after 6 PM."
                )

            synergies.append(f"Valentine's Window ({day_name}, Feb 14, {year}): Date-night footfall multiplier (1.25x) for romance and youth demographics.")
            
            clashes.append(CalendarClash(
                date=f"{year}-02-14 ({day_name})",
                event_name=f"Valentine's Day {year}",
                event_type="holiday",
                severity="low",
                impact_multiplier=1.25,
                description=weekend_structure
            ))

            # Realistic Timing Clash: National Board Exam Season (Feb-March)
            clashes.append(CalendarClash(
                date=f"Mid-February to March {year}",
                event_name=f"National Board Examination Season ({year})",
                event_type="exam_season",
                severity="medium",
                impact_multiplier=0.80,
                description=(
                    "CBSE, ICSE, and State Board secondary/higher examinations commence mid-February and run through March. "
                    "Significantly depresses weekday afternoon and youth/student theatrical attendance across all major circuits."
                )
            ))
            warnings.append(
                f"Board Exam Headwind: Feb-March academic exam period reduces teenage and collegiate weekday footfalls. Focus on prime evening weekend shows."
            )
            risk_score = 5 # Moderate Risk due to exam season headwind
            recommended_range = f"Friday, February 12, {year} to Sunday, February 14, {year}" if d.weekday() == 6 else f"February 12-15, {year}"

        elif target_window == "independence_day":
            d = date(year, 8, 15)
            day_name = calendar.day_name[d.weekday()]
            
            if d.weekday() == 6: # Sunday
                weekend_structure = f"Sunday Holiday ({day_name}, Aug 15, {year}). Standard 3-day weekend (Fri Aug 13 - Sun Aug 15) with NO extra weekday holiday buffer. Peak footfalls concentrated on Sunday."
                impact_mult = 1.35
            elif d.weekday() == 4: # Friday
                weekend_structure = f"Natural 3-Day Long Weekend (Friday Aug 15, {year} through Sunday Aug 17)."
                impact_mult = 1.55
            elif d.weekday() == 3: # Thursday
                weekend_structure = f"4-Day Extended Weekend Potential (Thursday Aug 15, {year} with Friday bridge day)."
                impact_mult = 1.50
            else:
                weekend_structure = f"Mid-Week National Holiday ({day_name}, Aug 15, {year})."
                impact_mult = 1.40

            synergies.append(f"Independence Day ({day_name}, Aug 15, {year}): {weekend_structure} (Multiplier: {impact_mult}x)")
            
            clashes.append(CalendarClash(
                date=f"{year}-08-15 ({day_name})",
                event_name=f"Independence Day {year}",
                event_type="holiday",
                severity="low",
                impact_multiplier=impact_mult,
                description=weekend_structure
            ))

            if is_future_unannounced:
                clashes.append(CalendarClash(
                    date=f"Mid-August {year}",
                    event_name=f"Contested Independence Day Corridor ({year})",
                    event_type="tentpole_clash",
                    severity="high",
                    impact_multiplier=0.75,
                    description=(
                        f"Future {year} slate is unannounced. However, Independence Day is historically one of the most crowded Hindi release corridors "
                        f"(e.g., 2023: Gadar 2 vs OMG 2; 2024: Stree 2 vs Khel Khel Mein / Vedaa). Expect at least 1-2 major competing tentpoles to target this date."
                    )
                ))
                warnings.append(
                    f"Corridor Congestion: While {year} competitor slates remain unannounced, historical data confirms Independence Day is rarely solo. Budget for screen capacity competition."
                )

            risk_score = 6 # High competition corridor
            recommended_range = f"Friday, August 13, {year} to Sunday, August 15, {year}" if d.weekday() == 6 else f"August 14-17, {year}"

        elif target_window == "q3":
            # Q3 = July to September
            synergies.append(f"Q3 {year}: Encompasses prime Independence Day (Aug 15) and Janmashtami festive corridors.")
            clashes.append(CalendarClash(
                date=f"Mid-August {year}",
                event_name=f"Independence Day Corridor Clustering ({year})",
                event_type="tentpole_clash",
                severity="high",
                impact_multiplier=0.75,
                description=f"Q3 contains Independence Day (Aug 15), the highest-density competitive tentpole corridor in Q3. Unannounced A-list tentpoles will crowd mid-August."
            ))
            clashes.append(CalendarClash(
                date=f"July - August {year}",
                event_name=f"Monsoon Weather Footfall Disruptions ({year})",
                event_type="dry_period",
                severity="medium",
                impact_multiplier=0.85,
                description="Heavy seasonal monsoon rainfall frequently causes transit and box office disruptions across Mumbai, Gujarat, and coastal territories."
            ))
            warnings.append(f"Q3 Corridor Caution: Mid-August is highly congested and July-August carries regional monsoon transit risks. September offers cleaner runway.")
            risk_score = 6 # High Risk due to Independence Day and monsoon
            recommended_range = f"September {year} (Post-Monsoon & Post-Independence Day Buffer)"

        elif target_window == "republic_day":
            d = date(year, 1, 26)
            day_name = calendar.day_name[d.weekday()]
            weekend_structure = f"Republic Day ({day_name}, Jan 26, {year})"
            impact_mult = 1.45
            synergies.append(f"Republic Day ({day_name}, Jan 26, {year}): Patriotic and action multiplier (Multiplier: {impact_mult}x)")
            clashes.append(CalendarClash(
                date=f"{year}-01-26 ({day_name})",
                event_name=f"Republic Day {year}",
                event_type="holiday",
                severity="low",
                impact_multiplier=impact_mult,
                description=f"Gazetted National Holiday on {day_name}."
            ))
            risk_score = 4
            recommended_range = f"Late January {year} Corridor"

        elif target_window == "diwali":
            diwali_date = MOVEABLE_FESTIVALS.get(year, {}).get("diwali", f"{year}-11-01")
            synergies.append(f"Diwali Festive Surge ({diwali_date}): Highest family footfall expansion period of the year (1.60x).")
            clashes.append(CalendarClash(
                date=f"T-3 Days before {diwali_date}",
                event_name=f"Pre-Diwali Laxmi Pujan Lull ({year})",
                event_type="dry_period",
                severity="high",
                impact_multiplier=0.55,
                description="Pre-Diwali shopping and puja days historically experience empty theaters until Diwali night."
            ))
            clashes.append(CalendarClash(
                date=diwali_date,
                event_name=f"Diwali Weekend {year}",
                event_type="festival",
                severity="low",
                impact_multiplier=1.60,
                description="Post-puja theatrical explosion for broad mass and family entertainers."
            ))
            risk_score = 7
            recommended_range = f"Diwali Day ({diwali_date}) or Post-Diwali Monday"

        elif target_window == "christmas":
            d = date(year, 12, 25)
            day_name = calendar.day_name[d.weekday()]
            synergies.append(f"Christmas Holiday Runway ({day_name}, Dec 25, {year}): Extended 10-day vacation corridor through New Year (1.50x).")
            clashes.append(CalendarClash(
                date=f"{year}-12-25 ({day_name})",
                event_name=f"Christmas Holiday {year}",
                event_type="holiday",
                severity="low",
                impact_multiplier=1.50,
                description="Metro multiplex operating capacity peaks during this 10-day vacation runway."
            ))
            risk_score = 6
            recommended_range = f"Dec 21 - Dec 25, {year}"

        else: # Custom or unrecognised window
            clashes.append(CalendarClash(
                date=f"Unannounced Corridor {year}",
                event_name=f"Open Release Window ({planned_window})",
                event_type="tentpole_clash",
                severity="medium",
                impact_multiplier=1.0,
                description=f"Standard commercial theatrical corridor for '{planned_window}' in {year}. Unannounced future slate carries standard corridor uncertainty."
            ))
            synergies.append("Flexible release runway without direct mandatory holiday date-locking.")
            risk_score = 5 # Moderate uncertainty for unannounced slate
            recommended_range = f"{planned_window} (Friday Release Recommended)"

        if risk_score >= 8:
            risk_tier = "Severe Clash Hazard"
        elif risk_score >= 6:
            risk_tier = "High Risk"
        elif risk_score >= 4:
            risk_tier = "Moderate Risk"
        else:
            risk_tier = "Low Risk"

        return CalendarAnalysis(
            planned_window=planned_window,
            overall_risk_score=risk_score,
            risk_tier=risk_tier,
            clashes_and_events=clashes,
            festival_synergies=synergies,
            hazard_warnings=warnings if warnings else ["Maintain standard 2-week clearance from unannounced pan-India releases"],
            recommended_date_range=recommended_range
        )

calendar_service = CalendarService()
