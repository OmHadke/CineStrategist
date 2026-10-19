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
        is_chawl_redevelopment = any(w in logline_lower for w in ["chawl", "redevelopment", "builder", "protest", "eviction", "tenement", "slum", "colony", "housing", "viral", "movement"])
        is_romance_drama = any(g.lower() in ["romance", "romantic", "love", "musical"] for g in film_input.genres)
        is_comedy_social = any(g.lower() in ["comedy", "social", "satire"] for g in film_input.genres)
        is_comedy_family = any(g.lower() in ["comedy", "family"] for g in film_input.genres)

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

        elif is_romance_drama:
            campaign_slogan = f"Every Heart Has A City To Return To: {title}"
            narrative_hooks = [
                "Intoxicating lead chemistry and soulful, era-defining music soundtrack",
                "Relatable modern romantic conflicts: devotion, ambition, and heartbreak",
                "Grand, picturesque visual storytelling engineered for big-screen romantic escapism"
            ]
            beats: List[MarketingBeat] = [
                MarketingBeat(
                    phase="T-90 to T-60 (Tease)",
                    day_offset="T-75 Days",
                    asset_type="Acoustic First Look Motion Poster",
                    title=f"{title}: Character Teaser & Acoustic Theme Motif",
                    description=(
                        "Release an intimate first-look motion poster showcasing the lead pair in a scenic urban or rustic twilight setting, "
                        "accompanied by a 30-second acoustic melody snippet. No dialogue; ignite musical curiosity."
                    ),
                    target_channels=["YouTube Shorts", "Instagram Reels", "Spotify Artist Page"],
                    kpi_metric="Illustrative Target: ~20-25M organic digital views; strong audio bookmark rate"
                ),
                MarketingBeat(
                    phase="T-60 to T-30 (Hype)",
                    day_offset="T-45 Days",
                    asset_type="Song 1 (Lead Romantic Duet) + Video Launch",
                    title="Lead Love Anthem Drop & Reels Hookstep Trend",
                    description=(
                        "Drop Song 1: the album's crown jewel romantic duet (spearheaded by marquee playback singers e.g. Arijit Singh / Shreya Ghoshal). "
                        "Execute simultaneous campus and radio blitz; partner with top 50 Instagram creators for couple reels."
                    ),
                    target_channels=["Spotify India Top 50", "YouTube Worldwide", "Radio Mirchi / Red FM", "Reels"],
                    kpi_metric="Illustrative Target: ~60M+ cross-platform views; Top 5 Spotify India Viral entry"
                ),
                MarketingBeat(
                    phase="T-30 to T-15 (Peak)",
                    day_offset="T-25 Days",
                    asset_type="Song 2 (Heartbreak / Passion Ballad) & College Campus Tour",
                    title="Soulful Passion Track & Multi-City College Roadshow",
                    description=(
                        "Release the intense heartbreak/conflict track. Cast embarks on high-visibility college festivals and mall appearances "
                        "across Delhi, Mumbai, Pune, Bangalore, and Chandigarh for acoustic sing-alongs."
                    ),
                    target_channels=["University Fests", "Streaming Platforms", "Prime-Time Broadcast Collabs"],
                    kpi_metric="Heuristic Estimate: ~25% projected increase in youth advance booking intention"
                ),
                MarketingBeat(
                    phase="T-14 to T-7 (Trailer & Advance)",
                    day_offset="T-12 Days",
                    asset_type="Official Theatrical Trailer",
                    title="Emotional Theatrical Trailer Launch Event",
                    description=(
                        "Unveil the 3-minute official theatrical cut focusing on the emotional turning point and high-stakes romantic conflict. "
                        "Pair trailer release with the complete album jukebox on digital audio streaming."
                    ),
                    target_channels=["DCP Multiplex Screens", "YouTube Global Live Stream", "Lifestyle & Fashion Digital Outlets"],
                    kpi_metric="Illustrative Target: ~70-80M views in 24h; >90% positive audience sentiment score"
                ),
                MarketingBeat(
                    phase="T-7 to Release (Blitz)",
                    day_offset="T-5 Days",
                    asset_type="Advance Booking Blitz + Date-Night Combos",
                    title="Advance Ticketing Open + Couple & Student Promotional Packages",
                    description=(
                        "Open nationwide advance ticketing on BookMyShow and Paytm Insider with exclusive couple-seat packages "
                        "and collegiate promotional discounts. Host exclusive midnight fan club musical premiere screenings."
                    ),
                    target_channels=["BookMyShow / Paytm", "Lifestyle Apps", "FM Radio Takeover"],
                    kpi_metric="Heuristic Benchmark: ~₹8-12 Cr advance ticketing pre-sales prior to Day-1"
                ),
                MarketingBeat(
                    phase="Post-Release (Sustain)",
                    day_offset="Release + 3 Days",
                    asset_type="Emotional Audience Climax Reaction Cut",
                    title="Audience Tears & Standing Ovation Reaction Promo",
                    description=(
                        "Capture raw emotional audience reactions, tears, and spontaneous applause from packed multiplexes. "
                        "Release the unplugged reprise version of the lead ballad to sustain second-week momentum."
                    ),
                    target_channels=["Instagram Reels", "YouTube Shorts", "Music Streaming Platforms"],
                    kpi_metric="Heuristic Benchmark: Maintain sub-25% Monday drop-off in urban multiplex circuits"
                )
            ]
            music_strategy = (
                "For a modern romantic drama, the music album is the primary commercial driver. The release must follow a strict "
                "3-stage strategy: (1) Intoxicating love anthem at T-45 to capture mainstream radio and reels, (2) Deeply moving heartbreak ballad at T-25, "
                "and (3) Full soundtrack jukebox alongside theatrical trailer at T-12 to maximize streaming royalty saturation before opening day."
            )
            brand_tie_ins = [
                "Coffee Chain & QSR Partner (signature couple drinks and thematic cup sleeves)",
                "Youth Fashion & Apparel Brand (protagonist wardrobe collection)",
                "Audio Streaming Platform Exclusive (immersive artist commentary playlist)",
                "Dating / Social Discovery App (Valentine's or seasonal 'First Date at Movies' ticket bundles)"
            ]
            single_vs_multi = (
                "Urban multiplexes receive aesthetic romantic photo-booths and Dolby Atmos acoustic listening lounges. "
                "Heartland single screens receive massive cutout banners highlighting the film's larger-than-life emotional stakes and musical soul."
            )

        elif is_chawl_redevelopment and is_comedy_social:
            campaign_slogan = f"Our Chawl, Our Voice, Our Rules: {title}"
            narrative_hooks = [
                "David-vs-Goliath street comedy: eccentric chawl residents outsmarting corrupt real-estate tycoons",
                "Viral digital rebellion: weaponizing livestreams, memes, and community unity against corporate eviction",
                "Sharp, relatable situational humor exposing bureaucracy with heart-warming collective triumph"
            ]
            beats = [
                MarketingBeat(
                    phase="T-90 to T-60 (Tease)",
                    day_offset="T-50 Days",
                    asset_type="Mock Eviction Notice & Character Vignettes",
                    title="The Eviction Notice & Chawl Resident Introduction",
                    description=(
                        "Release an in-universe 'Official Notice of Demolition' digital asset that breaks the fourth wall, "
                        "followed by 45-second quirky character reels showcasing each eccentric resident's hilarious reaction. Zero plot spoilers."
                    ),
                    target_channels=["Instagram Reels", "YouTube Shorts", "College Campus Portals"],
                    kpi_metric="Illustrative Target: ~6-8M organic views; viral curiosity on real-estate satire (heuristic estimate)"
                ),
                MarketingBeat(
                    phase="T-60 to T-30 (Hype)",
                    day_offset="T-35 Days",
                    asset_type="Song 1 (Street Rap / Satirical Anthem)",
                    title="Gully Anthem Drop: 'Hum Nahi Hatenge' (We Won't Move)",
                    description=(
                        "Drop Song 1: a high-energy, infectious satirical street anthem blending dholak rhythms with street rap (in the vein of Gully Boy / Bareilly Ki Barfi). "
                        "Avoid conventional glossy party tracks; spotlight grassroots defiance and humor. Launch #SaveOurChawl meme contest."
                    ),
                    target_channels=["Spotify India Indie Top 50", "YouTube Music", "Campus Radio", "Reels Creators"],
                    kpi_metric="Illustrative Target: ~15-20M cross-platform streams; 30k+ creator reels (heuristic estimate)"
                ),
                MarketingBeat(
                    phase="T-30 to T-15 (Peak)",
                    day_offset="T-20 Days",
                    asset_type="Song 2 (Heartwarming Community Melody) + College Townhalls",
                    title="Chawl Solidarity Anthem & University Housing Debates",
                    description=(
                        "Release Song 2: a warm, nostalgic acoustic melody celebrating childhood memories and tenement camaraderie. "
                        "Cast and director host lively interactive college debates in Mumbai, Pune, Delhi, and Bangalore on urban redevelopment."
                    ),
                    target_channels=["Campus Conclaves", "Audio Streaming", "Digital News Satire Portals"],
                    kpi_metric="Heuristic Estimate: ~25% projected bump in collegiate weekend advance ticketing intent"
                ),
                MarketingBeat(
                    phase="T-14 to T-7 (Trailer & Advance)",
                    day_offset="T-10 Days",
                    asset_type="Official Theatrical Trailer",
                    title="Grand Trailer Launch at Historic Mumbai Chawl",
                    description=(
                        "Host a landmark on-ground trailer premiere directly inside an iconic heritage chawl in Central Mumbai. "
                        "Unveil the 2.5-minute official cut maximizing the laugh-a-minute clash between ruthless builders and cunning residents."
                    ),
                    target_channels=["DCP Multiplex Theaters", "YouTube Live Stream", "Print Culture Features"],
                    kpi_metric="Illustrative Target: ~25-30M views in 24h; >90% positive audience reception index (heuristic target)"
                ),
                MarketingBeat(
                    phase="T-7 to Release (Blitz)",
                    day_offset="T-4 Days",
                    asset_type="Targeted Metro Advance Ticketing & Influencer Screenings",
                    title="Advance Ticketing Open + Student Early-Access Previews",
                    description=(
                        "Open advance bookings on BookMyShow and Paytm Insider with targeted student and group discounts. "
                        "Organize paid Thursday evening word-of-mouth previews across 150 top metro multiplexes to ignite opening-weekend talkability."
                    ),
                    target_channels=["BookMyShow / Paytm", "Campus Hubs", "Metro Transit Billboards"],
                    kpi_metric="Heuristic Benchmark: ~₹80 Lakh - ₹1.5 Cr advance ticket pre-sales (realistic sleeper baseline)"
                ),
                MarketingBeat(
                    phase="Post-Release (Sustain)",
                    day_offset="Release + 3 Days",
                    asset_type="Audience Laughs & Climax Reaction Promo",
                    title="Theater Laughter Reels & Grassroots Triumph Reaction",
                    description=(
                        "Capture raw auditorium laughter, clapping, and genuine audience smiles from packed metro multiplexes. "
                        "Deploy digital clips highlighting the film's heartwarming underdog resolution to drive massive Saturday/Sunday multiplier."
                    ),
                    target_channels=["YouTube Shorts", "Instagram", "Broadcast News Satire Segments"],
                    kpi_metric="Heuristic Benchmark: Target 100%+ Saturday and Sunday box-office jump over Friday opening (sleeper trajectory)"
                )
            ]
            music_strategy = (
                "For a grassroots social comedy, glossy generic party tracks destroy authenticity. The soundtrack must be driven by punchy "
                "satirical street hip-hop, energetic dholak anthems, and an inspiring underdog solidarity chorus that fuels campus reels."
            )
            brand_tie_ins = [
                "Urban Streetwear & Sustainable Apparel Partner (chawl pride graphic tees)",
                "Digital Meme & News Satire Media Networks (co-branded viral explainer shorts)",
                "College Transit / Mobility Apps (special student cinema commute credits)"
            ]
            single_vs_multi = (
                "Curated metro multiplexes receive quirky 'Save Our Chawl' interactive digital photo-booths and meme installations. "
                "Heartland single screens receive grassroots street cutouts and autorickshaw speaker broadcasts."
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
                    kpi_metric="Illustrative Target: ~15-20M views; positive sentiment index > 90% (heuristic pacing)"
                ),
                MarketingBeat(
                    phase="T-60 to T-30 (Hype)",
                    day_offset="T-40 Days",
                    asset_type="Song 1 (Festive / Dance Track)",
                    title="Celebration Anthem & Hookstep Challenge",
                    description="Release the album's lead high-energy festive track. Launch Instagram Reels creator dance trend.",
                    target_channels=["Spotify", "YouTube Music", "Radio Mirchi", "Reels Creators"],
                    kpi_metric="Illustrative Target: 300k+ user-generated reels; Top 15 streaming chart entry (heuristic pacing)"
                ),
                MarketingBeat(
                    phase="T-30 to T-15 (Peak)",
                    day_offset="T-22 Days",
                    asset_type="Song 2 (Emotional Heart) & Brand Collabs",
                    title="Melodic Anchor Song + Family FMCG Tie-Ins",
                    description="Release the soulful melodic emotional anchor. Announce quick-commerce and consumer brand bundle contests.",
                    target_channels=["Streaming Channels", "Outdoor Billboards", "Food Delivery App Insets"],
                    kpi_metric="Heuristic Estimate: Deep organic emotional resonance across family demographic"
                ),
                MarketingBeat(
                    phase="T-14 to T-7 (Trailer & Advance)",
                    day_offset="T-10 Days",
                    asset_type="Official Theatrical Trailer",
                    title="Official Theatrical Comedy/Drama Trailer",
                    description="Launch laughter-packed 2-minute 45-second trailer emphasizing both comedic set-pieces and the emotional core.",
                    target_channels=["DCP Theatrical Screens", "YouTube Worldwide", "National Print Ads"],
                    kpi_metric="Illustrative Target: ~35-45M views in 24 hours; trending reception score > 85% (heuristic target)"
                ),
                MarketingBeat(
                    phase="T-7 to Release (Blitz)",
                    day_offset="T-5 Days",
                    asset_type="Advance Booking Open & Multi-City Tour",
                    title="Advance Ticketing Launch + Family Mall Roadshows",
                    description="Open bookings across all chains with early-bird family ticket discounts. Cast visits Ahmedabad, Delhi, Pune, Kolkata.",
                    target_channels=["BookMyShow", "Paytm Insider", "Shopping Mall Atriums"],
                    kpi_metric="Heuristic Benchmark: ~₹3-5 Cr advance ticket pre-sales before Friday opening (heuristic benchmark)"
                ),
                MarketingBeat(
                    phase="Post-Release (Sustain)",
                    day_offset="Release + 3 Days",
                    asset_type="Audience Laughs & Tears Reaction Cut",
                    title="Theater Reaction Cut & Bonus Song Drop",
                    description="Showcase genuine laughing families and emotional reactions outside theaters. Release bonus comedy promotional clip.",
                    target_channels=["Social Platforms", "News Broadcasts"],
                    kpi_metric="Heuristic Benchmark: Sub-30% Monday drop-off across multiplex chains (indicative benchmark)"
                )
            ]
            music_strategy = "Festive celebration dance tracks and hum-worthy melodies."
            brand_tie_ins = ["Family FMCG brands", "Quick-commerce grocery apps", "Lifestyle fashion partners"]
            single_vs_multi = "Broad family reach across all multiplex and single-screen centers."

        else:
            campaign_slogan = f"Experience The Ultimate Big-Screen Event: {title}"
            narrative_hooks = [
                "Unmissable cinematic scale and larger-than-life protagonist elevation",
                "Relentless commercial storytelling engineered for the silver screen"
            ]
            if film_input.budget_tier == "low":
                kpi_teaser = "Illustrative Target: ~5-10M organic impressions across digital hubs (heuristic estimate)"
                kpi_single = "Illustrative Target: ~15-20M views, organic reel adoption (heuristic estimate)"
                kpi_trailer = "Illustrative Target: ~20-30M views across platforms (heuristic estimate)"
                kpi_advance = "Illustrative Target: ~₹50L - ₹1.5 Cr opening weekend pre-sales (WOM dependent)"
            elif film_input.budget_tier == "mid":
                kpi_teaser = "Illustrative Target: ~15-25M organic impressions (heuristic estimate)"
                kpi_single = "Illustrative Target: ~30-45M views, streaming chart entry (heuristic estimate)"
                kpi_trailer = "Illustrative Target: ~40-60M views across platforms (heuristic estimate)"
                kpi_advance = "Illustrative Target: ~₹3-6 Cr opening advance ticketing (heuristic estimate)"
            else:
                kpi_teaser = "Illustrative Target: ~30-50M launch impressions (heuristic estimate)"
                kpi_single = "Illustrative Target: ~60-80M views, Top 5 viral chart entry (heuristic estimate)"
                kpi_trailer = "Illustrative Target: ~80-100M views across platforms (heuristic estimate)"
                kpi_advance = "Illustrative Target: ~₹15-25 Cr opening advance pre-sales (heuristic estimate)"

            beats = [
                MarketingBeat(
                    phase="T-90 to T-60 (Tease)",
                    day_offset="T-75 Days",
                    asset_type="Title Announcement & Motion Poster",
                    title=f"{title}: Character First Look Motion Poster",
                    description="Reveal protagonist silhouette, high-impact theme music motif, and theatrical release date.",
                    target_channels=["YouTube", "Instagram", "X / Twitter"],
                    kpi_metric=kpi_teaser
                ),
                MarketingBeat(
                    phase="T-60 to T-30 (Hype)",
                    day_offset="T-45 Days",
                    asset_type="Teaser & Song 1 (Mass Anthem)",
                    title="Teaser + Anchor Single Launch",
                    description="Drop adrenaline-fueled 90-second teaser followed by signature anchor track.",
                    target_channels=["Spotify India", "YouTube Music", "Instagram Reels"],
                    kpi_metric=kpi_single
                ),
                MarketingBeat(
                    phase="T-30 to T-15 (Peak)",
                    day_offset="T-25 Days",
                    asset_type="Song 2 (Melody / Romance)",
                    title="Melodic / Soulful Audio Single",
                    description="Unveil the secondary melodic track to expand multiplex youth and female audience appeal.",
                    target_channels=["Radio", "Streaming Platforms", "Television Prime Time"],
                    kpi_metric="High streaming retention and radio airplay saturation (indicative benchmark)"
                ),
                MarketingBeat(
                    phase="T-14 to T-7 (Trailer & Advance)",
                    day_offset="T-12 Days",
                    asset_type="Grand Theatrical Trailer Launch",
                    title="Official Theatrical Trailer Event",
                    description="Conduct a multi-city trailer launch with cast in Mumbai and regional centers.",
                    target_channels=["Theatrical DCP", "YouTube Live Stream", "National Newspapers"],
                    kpi_metric=kpi_trailer
                ),
                MarketingBeat(
                    phase="T-7 to Release (Blitz)",
                    day_offset="T-6 Days",
                    asset_type="Advance Booking Blitz & City Tours",
                    title="Advance Ticketing Open + National Promotional Roadshow",
                    description="Open bookings across BookMyShow and national ticketing partners.",
                    target_channels=["BookMyShow", "Paytm", "Mall Atriums", "Reality Shows"],
                    kpi_metric=kpi_advance
                ),
                MarketingBeat(
                    phase="Post-Release (Sustain)",
                    day_offset="Release + 3 Days",
                    asset_type="Audience Theater Reaction Promo",
                    title="Audience Climax Reaction & Celebration Track",
                    description="Capture auditorium cheering to drive repeat viewing and second-weekend surge.",
                    target_channels=["Shorts", "Reels", "Entertainment Channels"],
                    kpi_metric="Illustrative Benchmark: Strong weekday hold with under 35% Monday drop-off"
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
