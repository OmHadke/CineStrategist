"""
Calendar and Release Clash Evaluation Service.
Assesses window hazards (IPL, pre-Diwali lull, exams) and festival synergies.
"""

from typing import Dict, Any, List
from app.data.festivals import FESTIVALS_AND_HOLIDAYS, KNOWN_TENTPOLE_CLASHES
from app.models.schemas import CalendarClash, CalendarAnalysis

class CalendarService:
    def evaluate_window(self, planned_window: str, genres: List[str]) -> CalendarAnalysis:
        window_lower = planned_window.lower()
        clashes: List[CalendarClash] = []
        synergies: List[str] = []
        warnings: List[str] = []
        
        base_risk = 3 # Base normal risk
        
        # Check for festival or holiday overlaps
        for fest in FESTIVALS_AND_HOLIDAYS:
            fest_name = fest["name"].lower()
            fest_date = fest["date"].lower()
            fest_type = fest["type"]
            
            # Simple keyword matching for planned window
            matches = False
            if "diwali" in window_lower and "diwali" in fest_name:
                matches = True
            elif "christmas" in window_lower and "christmas" in fest_name:
                matches = True
            elif ("republic" in window_lower or "jan" in window_lower) and "republic" in fest_name:
                matches = True
            elif ("independence" in window_lower or "aug" in window_lower) and "independence" in fest_name:
                matches = True
            elif ("eid" in window_lower or "mar" in window_lower or "apr" in window_lower) and "eid" in fest_name:
                matches = True
            elif ("ipl" in window_lower or "may" in window_lower or "april" in window_lower) and "ipl" in fest_name:
                matches = True
            elif ("sept" in window_lower or "oct" in window_lower) and ("dussehra" in fest_name or "gandhi" in fest_name):
                matches = True

            if matches:
                severity = "low"
                if fest_type == "dry_period":
                    severity = "high"
                    base_risk += 3
                    warnings.append(f"Pre-holiday lull trap detected: {fest['name']} ({fest['notes']})")
                elif fest_type == "ipl_season":
                    severity = "medium"
                    base_risk += 2
                    warnings.append(f"IPL prime-time competition reduces evening weekend occupancy by ~20-25%")
                elif fest_type in ["holiday", "festival"]:
                    severity = "low"
                    synergies.append(f"{fest['name']}: {fest['notes']} (Multiplier: {fest['footfall_multiplier']}x)")
                
                clashes.append(CalendarClash(
                    date=fest["date"],
                    event_name=fest["name"],
                    event_type=fest_type,
                    severity=severity,
                    impact_multiplier=fest["footfall_multiplier"],
                    description=fest["notes"]
                ))

        # Check for known clashes in that window
        for clash_entry in KNOWN_TENTPOLE_CLASHES:
            if any(term in window_lower for term in ["diwali", "christmas", "independence", "q4"]):
                base_risk += 3
                warnings.append(f"Tentpole screen split: {clash_entry['screen_split_risk']}. {clash_entry['recommendation']}")
                clashes.append(CalendarClash(
                    date="Target Weekend",
                    event_name=f"Tentpole Collision ({clash_entry['window']})",
                    event_type="tentpole_clash",
                    severity="high",
                    impact_multiplier=0.75,
                    description=clash_entry["recommendation"]
                ))
                break

        # Fallback if no specific matches found
        if not clashes:
            clashes.append(CalendarClash(
                date="Target Quarter",
                event_name="Open Theatrical Corridor",
                event_type="holiday",
                severity="low",
                impact_multiplier=1.0,
                description="No catastrophic tentpole collisions recorded; standard weekend trajectory."
            ))
            synergies.append("Clean 2-week runway with minimal premium IMAX screen compression.")

        risk_score = min(10, max(1, base_risk))
        
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
            festival_synergies=synergies if synergies else ["Solo runway advantage for word-of-mouth growth"],
            hazard_warnings=warnings if warnings else ["Maintain standard 2-week clearance from unannounced pan-India releases"],
            recommended_date_range=f"Targeting optimal Thursday/Friday launch in {planned_window} corridor"
        )

calendar_service = CalendarService()
