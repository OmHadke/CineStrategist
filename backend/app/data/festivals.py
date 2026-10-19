"""
Multi-Year Indian Festival, Holiday, and Theatrical Calendar Database (2025-2028).
Provides accurate gazetted holiday dates, calculated days of the week,
and historical theatrical clash patterns.
"""

from datetime import date
from typing import Dict, Any, List, Optional
import calendar

# Moveable festivals by year
MOVEABLE_FESTIVALS: Dict[int, Dict[str, str]] = {
    2024: {
        "eid_ul_fitr": "2024-04-11",
        "holi": "2024-03-25",
        "dussehra": "2024-10-12",
        "diwali": "2024-11-01",
        "ipl_start": "2024-03-22",
        "ipl_end": "2024-05-26"
    },
    2025: {
        "eid_ul_fitr": "2025-03-31",
        "holi": "2025-03-14",
        "dussehra": "2025-10-02",
        "diwali": "2025-10-20",
        "ipl_start": "2025-03-22",
        "ipl_end": "2025-05-25"
    },
    2026: {
        "eid_ul_fitr": "2026-03-20",
        "holi": "2026-03-04",
        "dussehra": "2026-10-20",
        "diwali": "2026-11-08",
        "ipl_start": "2026-03-27",
        "ipl_end": "2026-05-31"
    },
    2027: {
        "eid_ul_fitr": "2027-03-10",
        "holi": "2027-03-23",
        "dussehra": "2027-10-10",
        "diwali": "2027-10-29",
        "ipl_start": "2027-03-26",
        "ipl_end": "2027-05-30"
    },
    2028: {
        "eid_ul_fitr": "2028-02-28",
        "holi": "2028-03-11",
        "dussehra": "2028-09-29",
        "diwali": "2028-10-17",
        "ipl_start": "2028-03-24",
        "ipl_end": "2028-05-28"
    }
}

# Fixed gazetted holidays (Month, Day)
FIXED_HOLIDAYS = {
    "republic_day": {"month": 1, "day": 26, "name": "Republic Day"},
    "independence_day": {"month": 8, "day": 15, "name": "Independence Day"},
    "gandhi_jayanti": {"month": 10, "day": 2, "name": "Gandhi Jayanti"},
    "christmas": {"month": 12, "day": 25, "name": "Christmas"}
}

FESTIVALS_AND_HOLIDAYS = [
    {"name": "Republic Day", "date": "January 26", "multiplier": 1.45, "type": "National Gazetted Holiday"},
    {"name": "Eid-ul-Fitr", "date": "March / April (Lunisolar)", "multiplier": 1.50, "type": "Religious Festival"},
    {"name": "IPL Cricket Season", "date": "Late March - Late May", "multiplier": 0.78, "type": "Prime-Time Competition"},
    {"name": "Independence Day", "date": "August 15", "multiplier": 1.55, "type": "National Gazetted Holiday"},
    {"name": "Gandhi Jayanti", "date": "October 2", "multiplier": 1.30, "type": "National Gazetted Holiday"},
    {"name": "Dussehra", "date": "October (Lunisolar)", "multiplier": 1.35, "type": "Religious Festival"},
    {"name": "Pre-Diwali Lull", "date": "T-3 Days to Diwali", "multiplier": 0.55, "type": "Pre-Festive Shopping Lull"},
    {"name": "Diwali Weekend", "date": "October / November (Lunisolar)", "multiplier": 1.65, "type": "Peak Box Office Corridor"},
    {"name": "Christmas Runway", "date": "December 25 - January 1", "multiplier": 1.50, "type": "10-Day Holiday Corridor"}
]

def get_holiday_details(holiday_key: str, year: int) -> Optional[Dict[str, Any]]:
    """Returns exact date, day of week, and holiday structural impact."""
    if holiday_key in FIXED_HOLIDAYS:
        info = FIXED_HOLIDAYS[holiday_key]
        d = date(year, info["month"], info["day"])
        day_name = calendar.day_name[d.weekday()]
        
        # Calculate weekend structure
        is_weekend = d.weekday() in [4, 5, 6] # Fri, Sat, Sun
        if d.weekday() == 6: # Sunday
            weekend_type = "Sunday Holiday (No extra weekday buffer; standard 3-day weekend climax)"
            extended_cushion = False
        elif d.weekday() == 4: # Friday
            weekend_type = "Natural 3-Day Long Weekend (Fri-Sun)"
            extended_cushion = True
        elif d.weekday() == 0: # Monday
            weekend_type = "Natural 3-Day Long Weekend (Sat-Mon)"
            extended_cushion = True
        elif d.weekday() == 3: # Thursday
            weekend_type = "4-Day Extended Weekend Potential (Thu holiday with Friday bridge)"
            extended_cushion = True
        else: # Tue, Wed
            weekend_type = f"Mid-Week Holiday ({day_name})"
            extended_cushion = False

        return {
            "date": d.isoformat(),
            "year": year,
            "day_name": day_name,
            "name": f"{info['name']} {year}",
            "weekend_type": weekend_type,
            "extended_cushion": extended_cushion
        }
    return None
