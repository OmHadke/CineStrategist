"""
Agent 5: Tactical 30/60/90 Marketing Playbook Agent.
Builds an authentic, theme-aware campaign cadence strictly derived from the film's genre,
logline conflict (e.g. duty vs family, covert warfare), and target market sensibilities.
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
        logline_lower = film_input.logline.lower()
        is_war_military = any(g.lower() in ["war", "action", "thriller"] for g in film_input.genres) and any(
            w in logline_lower for w in ["war", "covert", "special forces", "mission", "enemy lines", "officer", "duty", "cross-border"]
        )
        is_comedy_family = any(g.lower() in ["comedy", "drama", "family"] for g in film_input.genres)

        if is_war_military:
            # Dedicated campaign slogan tailored to covert warfare and duty vs family
            campaign_slogan = "Behind Enemy Lines, Duty Is The Only Shield"
            narrative_hooks = [
                "Unsanctioned covert warfare: high-stakes survival behind enemy lines with zero room for failure",
                "The heartbreaking emotional friction: choosing between the uniform and the family you left behind",
                "Grand, authentic military tactical set-pieces engineered for IMAX and single-screen auditoriums alike"
            ]

            beats: List[MarketingBeat] = [
                MarketingBeat(
                    phase="T-90 to T-60 (Tease)",
                    day_offset="T-75 Days",
                    asset_type="Classified Mission Brief & First Look",
                    title=f"{title}: Operational File & Tactical Character Reveal",
                    description=(
                        "Release an ominous, classified intelligence dossier motion poster revealing the lead operative in tactical gear, "
                        "accompanied by intercepted radio comms and an intense metallic battle score. No plot spoilers; establish mission urgency."
                    ),
                    target_channels=["YouTube", "Instagram", "X / Twitter", "National Multiplex Pre-Rolls"],
                    kpi_metric="Illustrative Target: ~25-30M organic digital impressions (heuristic pacing benchmark)"
                ),
                MarketingBeat(
                    phase="T-60 to T-30 (Hype)",
                    day_offset="T-45 Days",
                    asset_type="Combat Teaser + Patriotic Anthem",
                    title="Mission Teaser Drop & Song 1 (Battle / Brotherhood Anthem)",
                    description=(
                        "Drop a 75-second high-octane combat teaser showcasing raw tactical firefights, followed 4 days later by Song 1: "
                        "a roaring, goosebump-inducing patriotic battle anthem (in the tradition of 'Teri Mitti' / 'Aarambh Hai Prachand'). "
                        "Avoid forced glamorous party tracks; focus on brotherhood and national duty."
                    ),
                    target_channels=["Spotify India", "YouTube Music", "Radio Mirchi / Red FM", "Reels Tactical Trend Collabs"],
                    kpi_metric="Illustrative Target: ~50-60M cross-platform views; Top 10 Spotify India Viral entry (heuristic pacing)"
                ),
                MarketingBeat(
                    phase="T-30 to T-15 (Peak)",
                    day_offset="T-25 Days",
                    asset_type="Duty vs Family Emotional Featurette & Track 2",
                    title="The Heart of the Mission: Emotional Motif & Co-Branded Launch",
                    description=(
                        "Release Song 2: a soulful, poignant melody spotlighting the family dilemma—letters sent home, promises to return, "
                        "and the personal agony of soldiers. Launch nationwide co-branded initiative with Armed Forces veteran welfare foundations."
                    ),
                    target_channels=["National Television Prime Time", "Outdoor Metro Billboards", "Streaming Platforms"],
                    kpi_metric="Heuristic Estimate: ~15-20% projected lift in female/family ticketing intent (studio heuristic analog)"
                ),
                MarketingBeat(
                    phase="T-14 to T-7 (Trailer & Advance)",
                    day_offset="T-12 Days",
                    asset_type="Theatrical Trailer Launch at Military Landmark",
                    title="Grand Trailer Launch Event (War Memorial / Air Base)",
                    description=(
                        "Host a massive on-ground trailer launch in Delhi/Chandigarh attended by defense veterans, lead cast, and director. "
                        "Unveil the 3-minute theatrical cut balancing tactical gunplay, covert betrayal tension, and national pride."
                    ),
                    target_channels=["5,000+ Theatrical DCP Screens", "YouTube Global Live Stream", "Front Page Print Coverage"],
                    kpi_metric="Illustrative Debut Target: ~80-100M views in 24h; >85% positive reception index (heuristic target)"
                ),
                MarketingBeat(
                    phase="T-7 to Release (Blitz)",
                    day_offset="T-6 Days",
                    asset_type="Advance Booking Blitz & Heartland City Tours",
                    title="Advance Ticketing Open + Punjab/UP/Delhi Armed Forces Roadshow",
                    description=(
                        "Open advance ticketing nationwide on BookMyShow and Paytm Insider. Conduct targeted high-energy city tours across "
                        "major military recruit belts (Chandigarh, Jaipur, Lucknow, Dehradun). Organize early-access tribute screenings for soldiers' families."
                    ),
                    target_channels=["BookMyShow / Paytm", "Mall Atriums", "Armed Forces Cantonment Screenings", "News Conclaves"],
                    kpi_metric="Heuristic Benchmark: ~₹15-20Cr pre-sales target before opening day (indicative pacing benchmark)"
                ),
                MarketingBeat(
                    phase="Post-Release (Sustain)",
                    day_offset="Release + 3 Days",
                    asset_type="Duty & Sacrifice Emotional Reaction Cut",
                    title="Audience Climax Reaction Promo & Final Tribute Cut",
                    description=(
                        "Capture raw emotional audience tears and standing ovations from the duty-vs-family climax. "
                        "Deploy digital clips celebrating real-life martyrs and operatives to turn holiday momentum into sustained 3-week legs."
                    ),
                    target_channels=["YouTube Shorts", "Instagram", "Broadcast News Features"],
                    kpi_metric="Heuristic Benchmark: Maintain sub-35% Monday drop-off across major circuits (indicative benchmark)"
                )
            ]


            music_strategy = (
                "For a serious tactical war thriller, conventional romantic duets or club party songs break narrative tension and alienate audiences. "
                "The album must follow a disciplined 2-pillar architecture: (1) A thumping, adrenalized patriotic/brotherhood anthem at T-45 for pre-workout "
                "and youth motivation, and (2) A deeply emotional family tribute ballad at T-25 that articulates the heartbreaking cost of duty over family."
            )

            brand_tie_ins = [
                "Automotive / Heavy Terrain Mobility Partner (exclusive co-branded spot featuring tactical transport)",
                "Outdoor Tactical & Apparel Brand (official mission utility gear line)",
                "Fintech / Ticket Platform Armed Forces Day Tribute (special discounted access for service families)",
                "Armed Forces Relief & Welfare Fund Charity Collaboration (percentage of day-1 proceeds dedicated to martyr support)"
            ]

            single_vs_multi = (
                "Heartland single-screen circuits (Punjab, Haryana, Rajasthan, UP) receive high-impact painted cutouts, local radio battle cries, "
                "and auto-rickshaw speaker promotions. Metro multiplexes receive immersive 3D tactical command center photo installations and Dolby Atmos sound previews."
            )

        elif is_comedy_family:
            campaign_slogan = f"The Heartfelt Family Entertainer of the Year: {title}"
            narrative_hooks = [
                "Universal multi-generational humor and emotional warmth",
                "Relatable social commentary with unforgettable comedic timing"
            ]
            beats = [
                MarketingBeat(
                    phase="T-90 to T-60 (Tease)",
                    day_offset="T-60 Days",
                    asset_type="Character Teaser & Title Look",
                    title=f"{title}: Quirky Family/World Reveal",
                    description="Drop character introduction vignettes introducing the eccentric cast ensemble and high-concept premise.",
                    target_channels=["YouTube", "Instagram Reels", "Family Television Intermissions"],
                    kpi_metric="20M+ views, positive sentiment index > 90%"
                ),
                MarketingBeat(
                    phase="T-60 to T-30 (Hype)",
                    day_offset="T-40 Days",
                    asset_type="Song 1 (Festive / Dance Track)",
                    title="Celebration Anthem & Hookstep Challenge",
                    description="Release the album's lead high-energy festive track. Launch Instagram Reels creator dance trend.",
                    target_channels=["Spotify", "YouTube Music", "Radio Mirchi", "Reels Creators"],
                    kpi_metric="500k+ user-generated reels, Top 10 streaming chart entry"
                ),
                MarketingBeat(
                    phase="T-30 to T-15 (Peak)",
                    day_offset="T-22 Days",
                    asset_type="Song 2 (Emotional Heart) & Brand Collabs",
                    title="Melodic Anchor Song + Family FMCG Tie-Ins",
                    description="Release the soulful melodic emotional anchor. Announce quick-commerce and consumer brand bundle contests.",
                    target_channels=["Streaming Channels", "Outdoor Billboards", "Food Delivery App Insets"],
                    kpi_metric="Deep organic emotional resonance across family demographic"
                ),
                MarketingBeat(
                    phase="T-14 to T-7 (Trailer & Advance)",
                    day_offset="T-10 Days",
                    asset_type="Official Theatrical Trailer",
                    title="Official Theatrical Comedy/Drama Trailer",
                    description="Launch laughter-packed 2-minute 45-second trailer emphasizing both comedic set-pieces and the emotional core.",
                    target_channels=["DCP Theatrical Screens", "YouTube Worldwide", "National Print Ads"],
                    kpi_metric="75M+ views in 24 hours, #1 Trending on YouTube"
                ),
                MarketingBeat(
                    phase="T-7 to Release (Blitz)",
                    day_offset="T-5 Days",
                    asset_type="Advance Booking Open & Multi-City Tour",
                    title="Advance Ticketing Launch + Family Mall Roadshows",
                    description="Open bookings across all chains with early-bird family ticket discounts. Cast visits Ahmedabad, Delhi, Pune, Kolkata.",
                    target_channels=["BookMyShow", "Paytm Insider", "Shopping Mall Atriums"],
                    kpi_metric="₹10Cr+ advance ticket pre-sales before Thursday evening previews"
                ),
                MarketingBeat(
                    phase="Post-Release (Sustain)",
                    day_offset="Release + 3 Days",
                    asset_type="Audience Laughs & Tears Reaction Cut",
                    title="Theater Reaction Cut & Bonus Song Drop",
                    description="Showcase genuine laughing families and emotional reactions outside theaters. Release bonus comedy promotional clip.",
                    target_channels=["Social Platforms", "News Broadcasts"],
                    kpi_metric="Sub-30% Monday drop-off across all multiplex chains"
                )
            ]
            music_strategy = "Festive celebration dance tracks and hum-worthy romantic melodies."
            brand_tie_ins = ["Family FMCG brands", "Quick-commerce grocery apps", "Lifestyle fashion partners"]
            single_vs_multi = "Broad family reach across all multiplex and single-screen centers."

        else:
            campaign_slogan = f"Experience The Ultimate Big-Screen Event: {title}"
            narrative_hooks = [
                "Unmissable cinematic scale and larger-than-life protagonist elevation",
                "Relentless commercial storytelling engineered for the largest silver screen"
            ]
            beats = [
                MarketingBeat(
                    phase="T-90 to T-60 (Tease)",
                    day_offset="T-75 Days",
                    asset_type="Title Announcement & Motion Poster",
                    title=f"{title}: Character First Look Motion Poster",
                    description="Reveal protagonist silhouette, high-impact theme music motif, and theatrical release date.",
                    target_channels=["YouTube", "Instagram", "X / Twitter"],
                    kpi_metric="25M+ impressions in 24 hours"
                ),
                MarketingBeat(
                    phase="T-60 to T-30 (Hype)",
                    day_offset="T-45 Days",
                    asset_type="Teaser & Song 1 (Mass Anthem)",
                    title="Action Teaser + Mass Single Launch",
                    description="Drop adrenaline-fueled 90-second teaser followed by the signature mass hero intro track.",
                    target_channels=["Spotify India", "YouTube Music", "Instagram Reels"],
                    kpi_metric="50M+ views, Top 5 viral music chart entry"
                ),
                MarketingBeat(
                    phase="T-30 to T-15 (Peak)",
                    day_offset="T-25 Days",
                    asset_type="Song 2 (Melody / Romance)",
                    title="Romantic / Soulful Audio Single",
                    description="Unveil the lead romantic duet to expand multiplex youth and female audience appeal.",
                    target_channels=["Radio", "Streaming Platforms", "Television Prime Time"],
                    kpi_metric="High streaming retention and radio airplay saturation"
                ),
                MarketingBeat(
                    phase="T-14 to T-7 (Trailer & Advance)",
                    day_offset="T-12 Days",
                    asset_type="Grand Theatrical Trailer Launch",
                    title="Official Theatrical Trailer Event",
                    description="Conduct a grand multi-city trailer launch with cast in Mumbai and regional centers. Distribute trailer to 5,000 screens.",
                    target_channels=["Theatrical DCP", "YouTube Live Stream", "National Newspapers"],
                    kpi_metric="85M+ views in 24 hours, universal positive trailer reception score > 85%"
                ),
                MarketingBeat(
                    phase="T-7 to Release (Blitz)",
                    day_offset="T-6 Days",
                    asset_type="Advance Booking Blitz & City Tours",
                    title="Advance Ticketing Open + National Promotional Roadshow",
                    description="Open bookings across BookMyShow and Paytm with nationwide college and mall blitzes.",
                    target_channels=["BookMyShow", "Paytm", "Mall Atriums", "Reality Shows"],
                    kpi_metric="₹15Cr+ pre-sales advance before opening day"
                ),
                MarketingBeat(
                    phase="Post-Release (Sustain)",
                    day_offset="Release + 3 Days",
                    asset_type="Audience Theater Reaction Promo",
                    title="Audience Climax Reaction & Celebration Track",
                    description="Capture auditorium whistling and cheering to drive repeat viewing and second-weekend surge.",
                    target_channels=["Shorts", "Reels", "Entertainment Channels"],
                    kpi_metric="Strong weekday hold with under 35% Monday drop-off"
                )
            ]
            music_strategy = "Staggered commercial audio rollout: Mass hero intro anthem at T-45, romantic duet at T-25, jukebox at T-10."
            brand_tie_ins = ["Beverage & food delivery partner", "Fintech ticketing partner", "Automotive partner"]
            single_vs_multi = "High-impact single-screen cutouts in heartland centers; interactive standees in metro multiplexes."

        return MarketingPlaybook(
            campaign_slogan_or_theme=campaign_slogan,
            key_narrative_hooks=narrative_hooks,
            timeline_beats=beats,
            music_release_cadence=music_strategy,
            brand_tie_ins=brand_tie_ins,
            single_screen_vs_multiplex_activation=single_vs_multi
        )


marketing_agent = MarketingAgent()
