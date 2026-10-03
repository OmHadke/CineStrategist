"""
Agent 3: Audience & Sentiment Archetype Agent.
Profiles target demographics, computes multiplex vs single-screen resonance,
and articulates core sentiment drivers.
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
              "urban_multiplex_appeal": 60,
              "heartland_single_screen_appeal": 40,
              "sentiment_drivers": ["driver1", "driver2"],
              "fatigue_or_backlash_risks": ["risk1", "risk2"],
              "positioning_hook": "one sentence studio positioning hook",
              "word_of_mouth_dependence": "Low (Star-driven Opening)" | "Moderate" | "Extreme (Sleeper/Story-driven)"
            }}
            """
            system_instruction = "You are a senior audience insights analyst at a major film studio (e.g. Red Chillies, YRF)."
            res = await llm_service.generate_json(prompt, system_instruction)
            if res and "primary_archetypes" in res:
                return AudienceAnalysis(**res)

        # High-calibre domain heuristic
        is_action_mass = any(g in ["Action", "Thriller", "Horror"] for g in film_input.genres)
        is_family_comedy = any(g in ["Comedy", "Drama", "Family"] for g in film_input.genres)
        is_mega_star = film_input.star_tier in ["tier_1", "mega"]

        if is_action_mass and is_mega_star:
            urban_split = 45
            heartland_split = 55
            wom = "Low (Star-driven Opening)"
            archetypes = [
                "Mass Tier-2/Tier-3 Single Screen Front-Benchers",
                "Youth Action & Pop-Culture Community",
                "Weekend Family Spectacle Seekers"
            ]
            drivers = [
                "Heroic elevation moments and whistle-worthy dialogue",
                "High-adrenaline musical score and dance anthem",
                "Grand physical action choreography"
            ]
            risks = [
                "Critical pushback if emotional stakes feel formulaic or thin",
                "Pacing drag during romantic subplots"
            ]
            hook = "Position as an unmissable big-screen high-octane theatrical event engineered for collective auditorium euphoria."
        elif is_family_comedy:
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
                "Hum-worthy melodic or festive soundtrack"
            ]
            risks = [
                "Vulnerability to slow opening if trailer fails to deliver clear laughter quotient",
                "Risk of sounding preachier than entertaining"
            ]
            hook = "Frame as the heartfelt family entertainer of the season that leaves audiences laughing and moved."
        else:
            urban_split = 65
            heartland_split = 35
            wom = "Moderate"
            archetypes = [
                "Discerning Urban Multiplex Audiences",
                "High-Concept Thriller Enthusiasts",
                "College & Digital-Savvy Youth"
            ]
            drivers = [
                "Intelligent non-linear narrative and twist reveal",
                "Polished atmospheric cinematography and sound design"
            ]
            risks = [
                "Risk of alienating rural single screens if English dialogues or pacing are too dense"
            ]
            hook = "Market as an edge-of-the-seat psychological ride that demands post-screening debate and discovery."

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
