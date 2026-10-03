"""
Historical evaluation presets for instant one-click testing and demonstration.
Pre-populated with pre-release data known before release.
"""

from typing import Dict, Any

PRESET_FILMS: Dict[str, Dict[str, Any]] = {
    "jawan": {
        "id": "jawan",
        "name": "Jawan (Mega Action Pan-India)",
        "year": 2023,
        "input": {
            "title": "Jawan",
            "genres": ["Action", "Thriller", "Drama"],
            "language": "Hindi",
            "budget_tier": "mega",
            "star_tier": "tier_1",
            "director": "Atlee",
            "target_audience": "Mass heartland single-screens + youth urban multiplexes + South regional audiences",
            "planned_window": "Sept 2026 (Janmashtami extended weekend)",
            "logline": "A former commando turned jailer leads a team of six women inmates on audacious socio-political hijackings across India to force government accountability, while confronting a ruthless global arms merchant from his forgotten past.",
            "platforms": "theatrical",
            "pan_india": True
        },
        "historical_context": "Released Sept 7, 2023. Went on to gross ₹1,150 Cr worldwide, becoming an all-time blockbuster by marrying South mass direction with Shah Rukh Khan's pan-Indian appeal."
    },
    "dunki": {
        "id": "dunki",
        "name": "Dunki (Social Dramedy vs Action Clash)",
        "year": 2023,
        "input": {
            "title": "Dunki",
            "genres": ["Comedy", "Drama", "Social"],
            "language": "Hindi",
            "budget_tier": "high",
            "star_tier": "tier_1",
            "director": "Rajkumar Hirani",
            "target_audience": "Universal family audiences + mature diaspora + Tier-1 urban multiplex viewers",
            "planned_window": "Christmas 2026 (Direct clash with mega action tentpole)",
            "logline": "Four friends from a small Punjab village dream of migrating to England for a better life and embark on an arduous illegal backdoor journey known as the 'Donkey Flight', testing their loyalty and love over decades.",
            "platforms": "theatrical",
            "pan_india": False
        },
        "historical_context": "Released Dec 21, 2023 in a high-voltage clash with action giant Salaar. Grossed ₹470 Cr worldwide on a ₹120 Cr budget, proving resilience but illustrating single-screen capacity constraints."
    },
    "stree_2": {
        "id": "stree_2",
        "name": "Stree 2 (Franchise Horror-Comedy)",
        "year": 2024,
        "input": {
            "title": "Stree 2: Sarkate Ka Aatank",
            "genres": ["Comedy", "Horror"],
            "language": "Hindi",
            "budget_tier": "mid",
            "star_tier": "tier_2",
            "director": "Amar Kaushik",
            "target_audience": "Mass youth + family + Tier-2/Tier-3 heartland towns + horror-comedy universe fans",
            "planned_window": "Independence Day 2026 (Extended 5-day holiday)",
            "logline": "The eccentric town of Chanderi faces a terrifying new headless entity that is abducting progressive women, forcing Vicky and his quirky gang to summon the original ghost of Stree to save their town.",
            "platforms": "theatrical",
            "pan_india": False
        },
        "historical_context": "Released Aug 15, 2024. Shocked the industry by grossing ₹860 Cr+ worldwide on a ₹60 Cr budget, becoming the highest-grossing Hindi film domestically."
    },
    "fighter": {
        "id": "fighter",
        "name": "Fighter (High-Concept Aerial Action)",
        "year": 2024,
        "input": {
            "title": "Fighter",
            "genres": ["Action", "Thriller", "War"],
            "language": "Hindi",
            "budget_tier": "mega",
            "star_tier": "tier_1",
            "director": "Siddharth Anand",
            "target_audience": "Urban multiplexes + metro youth + aviation action fans",
            "planned_window": "Republic Day 2026",
            "logline": "Top Indian Air Force fighter pilots from the elite 'Air Dragons' unit navigate high-altitude aerial skirmishes, personal trauma, and cross-border escalation following a terror attack in the valley.",
            "platforms": "theatrical",
            "pan_india": False
        },
        "historical_context": "Released Jan 25, 2024. Earned ₹355 Cr on a ₹250 Cr budget. Excelled in urban IMAX and 3D formats but underperformed in mass single screens due to westernized combat jargon."
    }
}
