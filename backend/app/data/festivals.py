"""
Indian Festival & Theatrical Calendar Database.
Provides historical and upcoming holiday dates, expected footfall multipliers,
and calendar hazard periods (IPL, pre-exam lull, pre-Diwali pooja lull).
"""

FESTIVALS_AND_HOLIDAYS = [
    # 2026/2027 Key Theatrical Windows & Milestones
    {
        "date": "2026-01-26",
        "name": "Republic Day Weekend",
        "type": "holiday",
        "footfall_multiplier": 1.45,
        "historical_precedent": "Pathaan, Fighter, Raees opened in this corridor",
        "notes": "Premium national holiday slot for patriotic/action/mega-tentpoles. 4-day extended holiday advantage."
    },
    {
        "date": "2026-03-20",
        "name": "Eid-ul-Fitr Window",
        "type": "festival",
        "footfall_multiplier": 1.50,
        "historical_precedent": "Traditional Salman Khan / Mass holiday weekend",
        "notes": "Mass single-screen footfall surge across North and West India. Post-fasting evening footfall explosion."
    },
    {
        "date": "2026-03-27 to 2026-05-31",
        "name": "IPL Cricket Season",
        "type": "ipl_season",
        "footfall_multiplier": 0.78,
        "historical_precedent": "Studios historically avoid releasing mega male-centric action films on prime match nights",
        "notes": "High competition for youth attention between 7:30 PM - 11:30 PM on weekends. Counter-programming (female-led, niche thrillers) can work."
    },
    {
        "date": "2026-08-15",
        "name": "Independence Day & Raksha Bandhan Synergy",
        "type": "holiday",
        "footfall_multiplier": 1.55,
        "historical_precedent": "Stree 2, Gadar 2, Shershaah period",
        "notes": "Golden theatrical window. If combined with Parsi New Year or Raksha Bandhan, footfalls can sustain ₹50Cr+ daily runs."
    },
    {
        "date": "2026-10-02",
        "name": "Gandhi Jayanti",
        "type": "holiday",
        "footfall_multiplier": 1.30,
        "historical_precedent": "War, Bang Bang",
        "notes": "Mid-week or extended weekend holiday with high urban multiplex turnout."
    },
    {
        "date": "2026-10-20",
        "name": "Dussehra / Navratri Culmination",
        "type": "festival",
        "footfall_multiplier": 1.35,
        "historical_precedent": "High regional festive mood in East (Durga Puja) and North/West",
        "notes": "Good momentum builder prior to pre-Diwali lull."
    },
    {
        "date": "2026-11-01 to 2026-11-06",
        "name": "Pre-Diwali Lull / Laxmi Pujan Days",
        "type": "dry_period",
        "footfall_multiplier": 0.55,
        "historical_precedent": "Pre-Diwali days show lowest footfalls of the year due to shopping and poojas",
        "notes": "Dangerous trap: releases 2-3 days before Diwali suffer empty theaters until Diwali evening."
    },
    {
        "date": "2026-11-08",
        "name": "Diwali Post-Laxmi Pujan & Govardhan Puja",
        "type": "festival",
        "footfall_multiplier": 1.65,
        "historical_precedent": "Singham Again vs Bhool Bhulaiyaa 3, Tiger 3, Housefull 4",
        "notes": "The most lucrative 5-day holiday run for family comedies and mega-spectacles."
    },
    {
        "date": "2026-12-25",
        "name": "Christmas to New Year Holiday Runway",
        "type": "holiday",
        "footfall_multiplier": 1.50,
        "historical_precedent": "Dangal, Dunki, Salaar, PK, 3 Idiots",
        "notes": "Longest holiday legs of the year. Urban multiplexes operate at near-total capacity for 10 straight days."
    }
]

KNOWN_TENTPOLE_CLASHES = [
    {
        "window": "Q4 2026 / Diwali 2026",
        "known_clashes": ["Mega Universe Franchise Part 3", "South Pan-India Action Epic 2"],
        "screen_split_risk": "Severe (50/50 single-screen split risk)",
        "recommendation": "Avoid direct day-and-date release unless budget > ₹250Cr with dominant distributor muscle."
    },
    {
        "window": "Christmas 2026",
        "known_clashes": ["International Hollywood Tentpole (Avatar/Marvel)", "Pan-Indian Spectacle"],
        "screen_split_risk": "IMAX and premium format screens will be 100% locked",
        "recommendation": "Release 1 week ahead (Dec 18) to grab early word-of-mouth before screen compression."
    },
    {
        "window": "Independence Day 2026",
        "known_clashes": ["Patriotic Action Drama", "Comedy Sequel"],
        "screen_split_risk": "Moderate (Market can expand to accommodate two films if genres differ, e.g. Gadar 2 + OMG 2)",
        "recommendation": "Feasible if genres are strictly non-overlapping."
    }
]
