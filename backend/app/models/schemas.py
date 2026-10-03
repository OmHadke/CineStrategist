from typing import List, Optional, Dict, Any, Literal
from pydantic import BaseModel, Field

# User Form Input Schema
class FilmInput(BaseModel):
    title: str = Field(..., description="Working title of the film", examples=["Project Thunder"])
    genres: List[str] = Field(..., description="List of primary and secondary genres", examples=[["Action", "Thriller"]])
    language: str = Field(default="Hindi", description="Primary original language", examples=["Hindi", "Telugu", "Tamil", "English"])
    budget_tier: Literal["low", "mid", "high", "mega"] = Field(
        ..., 
        description="Budget scale: low (<₹25Cr / <$5M), mid (₹25-75Cr / $5-20M), high (₹75-200Cr / $20-60M), mega (>₹200Cr / >$60M)"
    )
    star_tier: Literal["tier_1", "tier_2", "tier_3", "ensemble", "fresh_faces"] = Field(
        ...,
        description="Star power tier / box office pull"
    )
    director: Optional[str] = Field(default=None, description="Director name if known")
    target_audience: str = Field(
        ..., 
        description="Target audience demographics and psychographics (e.g., 'Mass heartland single-screens + youth urban multiplexes')"
    )
    planned_window: str = Field(
        ..., 
        description="Target release quarter or date range (e.g., 'Q4 2026' or 'Diwali 2026' or 'Dec 2026')"
    )
    logline: str = Field(
        ..., 
        description="1-2 paragraph plot synopsis or high-concept logline"
    )
    platforms: Literal["theatrical", "ott_only", "hybrid"] = Field(
        default="theatrical",
        description="Primary platform release strategy"
    )
    pan_india: bool = Field(
        default=False, 
        description="Whether a multi-lingual dub release (Tamil, Telugu, etc.) is planned"
    )

# Comparable Film Schema
class ComparableFilm(BaseModel):
    id: str
    title: str
    year: int
    genres: List[str]
    director: Optional[str] = None
    key_cast: List[str] = Field(default_factory=list)
    budget_est: str
    box_office_est: str
    verdict: str = Field(description="Box office verdict (All-Time Blockbuster, Hit, Average, Flop)")
    imdb_rating: float
    tmdb_score: Optional[float] = None
    similarity_score: float = Field(description="Score between 0.0 and 1.0 indicating comp fit")
    similarity_factors: List[str] = Field(default_factory=list)
    source: str = Field(default="Historical Curated DB & TMDB")
    key_takeaway: str = Field(description="Strategic learning from this comp's release")

class CompsAnalysis(BaseModel):
    comparables: List[ComparableFilm]
    median_rating: float
    performance_spread: str
    common_success_factors: List[str]
    common_pitfall_risks: List[str]
    benchmark_summary: str

# Release Calendar & Clash Risk Schema
class CalendarClash(BaseModel):
    date: str
    event_name: str
    event_type: Literal["holiday", "festival", "tentpole_clash", "ipl_season", "exam_season", "dry_period"]
    severity: Literal["low", "medium", "high", "critical"]
    impact_multiplier: float = Field(description="Expected footfall multiplier: e.g. 1.4 for Diwali, 0.7 for direct clash")
    description: str

class CalendarAnalysis(BaseModel):
    planned_window: str
    overall_risk_score: int = Field(ge=1, le=10, description="Risk score from 1 (optimal) to 10 (hazardous)")
    risk_tier: Literal["Low Risk", "Moderate Risk", "High Risk", "Severe Clash Hazard"]
    clashes_and_events: List[CalendarClash]
    festival_synergies: List[str]
    hazard_warnings: List[str]
    recommended_date_range: str

# Audience Archetype Schema
class AudienceAnalysis(BaseModel):
    primary_archetypes: List[str]
    urban_multiplex_appeal: int = Field(ge=0, le=100, description="Percentage appeal in Tier-1 multiplexes")
    heartland_single_screen_appeal: int = Field(ge=0, le=100, description="Percentage appeal in Mass single screens")
    sentiment_drivers: List[str]
    fatigue_or_backlash_risks: List[str]
    positioning_hook: str
    word_of_mouth_dependence: str = Field(description="e.g. 'Low (Star-driven Opening)', 'Moderate to High (Word-of-Mouth Dependent)', 'Extreme'")

# Strategy & Distribution Schema
class ReleaseOption(BaseModel):
    rank: int
    proposed_date: str
    slot_type: str = Field(description="e.g. 'Standard 3-Day Weekend (Sunday Peak Holiday Climax)', 'Contested Festive Corridor'")
    screen_count_est: str
    competition_level: str = Field(description="e.g. 'Contested Runway (Unannounced Future Slate)', 'Clear Runway', 'Direct Tentpole Clash'")
    pros: List[str]
    cons: List[str]
    strategic_rationale: str

class ReleaseStrategy(BaseModel):
    ranked_release_options: List[ReleaseOption]
    screen_distribution_strategy: str
    ott_windowing: Dict[str, Any] = Field(
        description="e.g. {'theatrical_holdback_weeks': 8, 'norm_compliance': 'PVR-INOX Multiplex Pact', 'target_ott_platforms': ['Netflix', 'Amazon Prime'], 'rationale': '...'}"
    )
    pan_india_distribution_plan: Optional[str] = None

# Tactical 30/60/90 Marketing Playbook Schema
class MarketingBeat(BaseModel):
    phase: Literal["T-90 to T-60 (Tease)", "T-60 to T-30 (Hype)", "T-30 to T-15 (Peak)", "T-14 to T-7 (Trailer & Advance)", "T-7 to Release (Blitz)", "Post-Release (Sustain)"]
    day_offset: str = Field(description="e.g. 'T-45 Days', 'T-10 Days'")
    asset_type: str = Field(description="e.g. 'Title Teaser', 'Song 1 (Mass Anthem)', 'Official Trailer', 'City Tour', 'Advance Booking Launch'")
    title: str
    description: str
    target_channels: List[str]
    kpi_metric: str

class MarketingPlaybook(BaseModel):
    campaign_slogan_or_theme: str
    key_narrative_hooks: List[str]
    timeline_beats: List[MarketingBeat]
    music_release_cadence: str
    brand_tie_ins: List[str]
    single_screen_vs_multiplex_activation: str

# Anti-Hallucination Critic Audit Schema
class AuditItem(BaseModel):
    claim: str
    claim_type: Literal["data_fact", "historical_comp", "calendar_date", "strategic_inference"]
    source_reference: str
    status: Literal["VERIFIED", "PROBABLE_INFERENCE", "CAUTION_UNVERIFIED"]
    critic_notes: str

class CriticAudit(BaseModel):
    credibility_score: int = Field(ge=0, le=100, description="Overall verification score")
    verdict: Literal["Approved - Studio Grade", "Approved with Inferences", "Needs Evidence Review"]
    total_claims_checked: int
    verified_claims_count: int
    audit_items: List[AuditItem]
    known_data_limitations: List[str]
    uncontrollable_risks: List[str]

# Full Unified Report Schema
class CineStrategistReport(BaseModel):
    report_id: str
    film_input: FilmInput
    comps_analysis: CompsAnalysis
    calendar_analysis: CalendarAnalysis
    audience_analysis: AudienceAnalysis
    release_strategy: ReleaseStrategy
    marketing_playbook: MarketingPlaybook
    critic_audit: CriticAudit
    metadata: Dict[str, Any] = Field(default_factory=dict)
