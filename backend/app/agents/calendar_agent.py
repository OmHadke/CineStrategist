"""
Agent 2: Release Calendar & Clash Risk Evaluator.
Scans Indian festival dates, long weekends, IPL competition, and competing tentpoles.
"""

from app.models.schemas import FilmInput, CalendarAnalysis
from app.services.calendar_service import calendar_service

class CalendarAgent:
    async def run(self, film_input: FilmInput) -> CalendarAnalysis:
        analysis = calendar_service.evaluate_window(
            planned_window=film_input.planned_window,
            genres=film_input.genres
        )
        return analysis

calendar_agent = CalendarAgent()
