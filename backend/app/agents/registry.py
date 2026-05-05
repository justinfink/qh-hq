"""Agent registry. Maps slug -> agent instance for dispatch from API/cron."""
from __future__ import annotations

from app.agents.base import Agent
from app.agents.news_scout import NewsScout
from app.agents.implication_mapper import ImplicationMapper

_AGENTS: dict[str, Agent] = {}


def register_all() -> None:
    for cls in (NewsScout, ImplicationMapper):
        agent = cls()
        _AGENTS[agent.slug] = agent


def get_agent(slug: str) -> Agent:
    if not _AGENTS:
        register_all()
    if slug not in _AGENTS:
        raise KeyError(f"Unknown agent: {slug}")
    return _AGENTS[slug]


def all_agents() -> list[Agent]:
    if not _AGENTS:
        register_all()
    return list(_AGENTS.values())
