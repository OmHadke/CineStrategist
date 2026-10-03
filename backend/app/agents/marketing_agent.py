"""
Agent 5: Tactical 30/60/90 Marketing Playbook Agent.
Designs a granular marketing roadmap matching the asset rollout rhythms of Indian cinema.
"""

from typing import List
from app.models.schemas import FilmInput, AudienceAnalysis, ReleaseStrategy, MarketingPlaybook, MarketingBeat

class MarketingAgent:
    async def run(
        self, 
        film_input: FilmInput, 
        audience: AudienceAnalysis, 
        strategy: ReleaseStrategy
    ) -> MarketingPlaybook:
        
        title = film_input.title
        beats: List[MarketingBeat] = [
            MarketingBeat(
                phase="T-90 to T-60 (Tease)",
                day_offset="T-75 Days",
                asset_type="Title Announcement & Motion Poster",
                title=f"{title}: Concept & Character Reveal",
                description="Drop high-impact motion poster showcasing protagonist look and thematic audio motif.",
                target_channels=["YouTube", "Instagram Reels", "X / Twitter", "National Multiplex Intermissions"],
                kpi_metric="25M+ cross-platform impressions in 24 hours, #1 Trending on X"
            ),
            MarketingBeat(
                phase="T-60 to T-30 (Hype)",
                day_offset="T-45 Days",
                asset_type="Teaser & Song 1 (Mass / Dance Anthem)",
                title="Pre-Trailer Teaser + Track 1 Drop",
                description="Unveil action/mood teaser followed 4 days later by the album's primary energy track. Drive Instagram creator challenge.",
                target_channels=["Spotify India", "YouTube Music", "Instagram Reels / Influencer Collabs", "Radio Mirchi / Red FM"],
                kpi_metric="50M+ views, 500k+ organic Reel creations within 7 days"
            ),
            MarketingBeat(
                phase="T-30 to T-15 (Peak)",
                day_offset="T-25 Days",
                asset_type="Song 2 (Melody / Romance) & Brand Tie-ins",
                title="Emotional Anchor Track + Co-Branded Campaign",
                description="Release the soulful heart of the album. Launch co-branded consumer campaigns (beverage, apparel, or fintech partner).",
                target_channels=["Streaming Platforms", "Television Prime Time", "Metro Billboard Hoardings"],
                kpi_metric="Audio climbs to Spotify India Top 10, 15% surge in brand partner visibility"
            ),
            MarketingBeat(
                phase="T-14 to T-7 (Trailer & Advance)",
                day_offset="T-12 Days",
                asset_type="Grand Theatrical Trailer Launch",
                title="Official Theatrical Trailer + Press Conference",
                description="Hold physical multi-city trailer launch event with lead cast and director in Mumbai and Hyderabad. Distribute DCP trailer to 5,000 screens.",
                target_channels=["DCP Theatrical Screens", "YouTube Worldwide", "National Print Front Pages"],
                kpi_metric="Record 80M+ views in 24 hours, universal positive trailer reception score > 85%"
            ),
            MarketingBeat(
                phase="T-7 to Release (Blitz)",
                day_offset="T-6 Days",
                asset_type="Advance Booking Blitz & City Mall Tours",
                title="Advance Ticketing Open + National College/Mall Roadshow",
                description="Open advance bookings on BookMyShow and Paytm Insider with early-bird merchandise bundles. Lead cast visits Delhi, Ahmedabad, Kolkata, Bengaluru.",
                target_channels=["BookMyShow", "Paytm Insider", "Mall Atriums", "TV Reality Show Guest Spots"],
                kpi_metric="₹15Cr+ pre-sales advance before Thursday night preview shows"
            ),
            MarketingBeat(
                phase="Post-Release (Sustain)",
                day_offset="Release + 3 Days",
                asset_type="Word-of-Mouth Amplification & Celebration Song",
                title="Audience Reaction Cut & Bonus Song Release",
                description="Capture ecstatic live audience theater reactions; drop the unreleased end-credit celebration track to fuel repeat weekend-2 viewings.",
                target_channels=["YouTube Shorts", "Instagram", "News Channels"],
                kpi_metric="Maintain < 35% Monday drop-off in all major national chains"
            )
        ]

        music_strategy = (
            "Music is the emotional locomotive of Indian film marketing. Adopt a 3-track staggered rollout: "
            "(1) High-energy mass anthem at T-45 for dance floor/gym hype, (2) Melodic romantic ballad at T-25 for radio/streaming longevity, "
            "and (3) Full original jukebox drop 48 hours prior to release."
        )

        brand_tie_ins = [
            "National Beverage / Quick-Commerce Delivery Partner (exclusive branded packaging with QR ticket contest)",
            "Automotive / Fashion Lifestyle Tie-in (lead cast wardrobe line or mobility partner)",
            "Fintech / Payment Gateway Co-marketing (discounted BOGO ticket offers to spur day-1 rush)"
        ]

        single_vs_multi = (
            "Deploy dual-pronged marketing collateral: Metro multiplexes receive immersive 3D standees and interactive photo-ops. "
            "Heartland single-screen circuits receive large-format painted hoardings, auto-rickshaw loudspeaker branding, and local radio spot saturation."
        )

        return MarketingPlaybook(
            campaign_slogan_or_theme=f"Experience the Phenomenon: {audience.positioning_hook}",
            key_narrative_hooks=[
                f"High-stakes confrontation tailored for {film_input.target_audience}",
                "Spectacular cinematic scale demanding the largest available silver screen",
                "Unforgettable musical and emotional journey"
            ],
            timeline_beats=beats,
            music_release_cadence=music_strategy,
            brand_tie_ins=brand_tie_ins,
            single_screen_vs_multiplex_activation=single_vs_multi
        )

marketing_agent = MarketingAgent()
