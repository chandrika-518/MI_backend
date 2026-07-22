from __future__ import annotations

import logging
from app.schemas.research import (
    CompetitorActivityOut,
    HallucinationCheckOut,
    ResearchRequest,
    ResearchResponse,
    ThemeOut,
)

logger = logging.getLogger("market_research_api")


class ResearchService:
    """Service containing research workflow business logic."""

    def create_research(self, payload: ResearchRequest) -> ResearchResponse:
        """Create a mock report and log the request for future processing."""
        logger.info(
            "Research request received with competitors=%s topics=%s urls=%s context=%s",
            payload.competitors,
            payload.topics,
            payload.urls,
            payload.context,
        )

        source = payload.urls[0] if payload.urls else "https://example.com"
        themes = [
            ThemeOut(
                title="Enterprise AI",
                summary="Mock summary",
                sources=[source],
            )
        ]
        competitor_activities = [
            CompetitorActivityOut(
                competitor="OpenAI",
                activity="Released new enterprise feature",
                sources=[source],
            )
        ]
        hallucination_check = HallucinationCheckOut(status="Supported", confidence=0.95)

        return ResearchResponse(
            themes=themes,
            competitorActivities=competitor_activities,
            hallucinationCheck=hallucination_check,
        )
