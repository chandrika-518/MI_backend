from __future__ import annotations

from typing import List
from pydantic import BaseModel, Field


class ResearchRequest(BaseModel):
    """Incoming research request payload."""

    competitors: List[str] = Field(default_factory=list)
    topics: List[str] = Field(default_factory=list)
    urls: List[str] = Field(default_factory=list)
    context: str = ""


class ThemeOut(BaseModel):
    """A research theme included in the mock report."""

    title: str
    summary: str
    sources: List[str] = Field(default_factory=list)


class CompetitorActivityOut(BaseModel):
    """Competitor activity summary."""

    competitor: str
    activity: str
    sources: List[str] = Field(default_factory=list)


class HallucinationCheckOut(BaseModel):
    """Hallucination check section of the mock report."""

    status: str
    confidence: float


class ResearchResponse(BaseModel):
    """Mock research report response."""

    themes: List[ThemeOut] = Field(default_factory=list)
    competitorActivities: List[CompetitorActivityOut] = Field(default_factory=list)
    hallucinationCheck: HallucinationCheckOut
