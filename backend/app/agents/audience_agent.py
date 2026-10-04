"""
Agent 3: Audience & Sentiment Archetype Agent.
Performs deep semantic inspection of genres, logline conflict, and comparable reception patterns.
Surfaces critical historical warnings (e.g. the Fighter heartland disconnect hazard).
"""

from app.models.schemas import FilmInput, CompsAnalysis, AudienceAnalysis
from app.services.llm_service import llm_service

class AudienceAgent:
    async def run(self, film_input: FilmInput, comps: CompsAnalysis) -> AudienceAnalysis:
        # Check if LLM is active
        if llm_service.is_available():
            prompt = f"""
            Analyze audience demographics and sentiment for this film:
            Title: {film_input.title}
            Genres: {', '.join(film_input.genres)}
            Budget Tier: {film_input.budget_tier}
            Target Audience: {film_input.target_audience}
            Logline: {film_input.logline}
            Top Comparable Titles: {', '.join(c.title for c in comps.comparables[:3])}

            Return JSON matching this exact structure:
            {{
              "primary_archetypes": ["archetype1", "archetype2", "archetype3"],
              "urban_multiplex_appeal": 40,
              "heartland_single_screen_appeal": 60,
              "sentiment_drivers": ["driver1", "driver2"],
              "fatigue_or_backlash_risks": ["risk1", "risk2"],
              "positioning_hook": "one sentence studio positioning hook",
              "word_of_mouth_dependence": "Low (Star-driven Opening)" | "Moderate to High (Word-of-Mouth Dependent)" | "Extreme (Sleeper/Story-driven)"
            }}
            """
            system_instruction = "You are a senior audience insights analyst at a major film studio. Reflect the exact themes in the logline."
            res = await llm_service.generate_json(prompt, system_instruction)
            if res and "primary_archetypes" in res:
                return AudienceAnalysis(**res)

        # Domain heuristic with deep semantic inspection of logline
        logline_lower = film_input.logline.lower()
        is_war_military = any(g.lower() in ["war", "action", "thriller"] for g in film_input.genres) and any(
            w in logline_lower for w in ["war", "covert", "special forces", "mission", "enemy lines", "officer", "duty", "cross-border"]
        )
        is_romance_drama = any(g.lower() in ["romance", "romantic", "love", "musical"] for g in film_input.genres)
        is_comedy_family = any(g.lower() in ["comedy", "family"] for g in film_input.genres)

        if is_war_military:
            urban_split = 40
            heartland_split = 60
            # Military action with high-concept mission is heavily WOM dependent (like Uri and Fighter)
            wom = "Moderate to High (Word-of-Mouth Dependent)"
            archetypes = [
                "Mass Heartland Single-Screen Moviegoers & Defense/Armed Forces Community",
                "Patriotic Family Theatergoers (seeking emotional national pride during holiday corridors)",
                "Youth Tactical Action & Espionage Thriller Enthusiasts"
            ]
            drivers = [
                "Visceral special forces brotherhood and high-stakes covert tension behind enemy lines",
                "Emotional family dilemma: the tragic friction between military duty and personal sacrifice",
                "Grand, authentic tactical combat choreography without cartoonish physics"
            ]
            risks = [
                "THE FIGHTER HAZARD: Risk of isolating heartland single-screens if combat terminology is too cold, technical, or westernized (the primary factor that held Fighter to an 'Average' verdict). Emotional family stakes must remain front-and-center.",
                "CBFC & DEFENCE PROTOCOL SCRUTINY: Portraying cross-border covert operations requires Ministry of Defence (MoD) NOC and careful handling to prevent regulatory friction or political controversy."
            ]
            hook = f"Position {film_input.title} as an unyielding, high-stakes tactical covert operation that balances relentless behind-enemy-lines combat with an emotionally devastating core of duty versus family."

        elif is_romance_drama:
            urban_split = 55
            heartland_split = 45
            wom = "High (Music & Emotional Word-of-Mouth Dependent)"
            archetypes = [
                "Youth & College Demographic (driving repeat viewings & streaming audio saturation)",
                "Metro & Urban Multiplex Couples & Contemporary Romance Seekers",
                "Female Decision-Makers & Multi-generational Family Audiences"
            ]
            drivers = [
                "Soulful, chart-topping musical album that dominates Spotify India and social reels",
                "Magnetic screen chemistry and emotionally raw confrontation between the leads",
                "Universal romantic stakes: personal sacrifice, modern relationship dilemmas, or heartbreak"
            ]
            risks = [
                "THE MUSIC DEPENDENCY HAZARD: Romantic dramas cannot open on star power alone if the music album fails to achieve viral breakout status (T-30 days prior).",
                "Risk of isolating single screens if dialogues are overly stylized or urban-centric without heartland emotional grounding."
            ]
            hook = f"Position {film_input.title} as the definitive modern love story of the season, propelled by an unforgettable musical soundtrack and poignant emotional stakes."

        elif is_comedy_family:
            urban_split = 55
            heartland_split = 45
            wom = "Extreme (Sleeper/Story-driven)"
            archetypes = [
                "Multi-generational Family Groups",
                "Metro Urban Multiplex Moviegoers",
                "Social Media Comedy & Meme Demographic"
            ]
            drivers = [
                "Relatable social commentary with organic comedic timing",
                "Emotional climax that resonates across age brackets",
                "Hum-worthy festive soundtrack"
            ]
            risks = [
                "Vulnerability to slow opening if trailer fails to deliver clear laughter quotient",
                "Risk of sounding preachy rather than entertaining"
            ]
            hook = f"Frame {film_input.title} as the heartfelt family entertainer of the season that leaves audiences laughing and moved."

        else:
            urban_split = 60
            heartland_split = 40
            wom = "Moderate"
            archetypes = [
                "Discerning Urban Multiplex Audiences",
                "High-Concept Commercial Moviegoers",
                "College & Digital-Savvy Youth"
            ]
            drivers = [
                "Intelligent narrative pacing and charismatic lead protagonist elevation",
                "Polished atmospheric cinematography and sound design"
            ]
            risks = [
                "Risk of alienating rural single screens if dialogues are too dense or pacing is uneven"
            ]
            hook = f"Position {film_input.title} as an edge-of-the-seat theatrical event demanding big-screen viewing."

        return AudienceAnalysis(
            primary_archetypes=archetypes,
            urban_multiplex_appeal=urban_split,
            heartland_single_screen_appeal=heartland_split,
            sentiment_drivers=drivers,
            fatigue_or_backlash_risks=risks,
            positioning_hook=hook,
            word_of_mouth_dependence=wom
        )

audience_agent = AudienceAgent()
