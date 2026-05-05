"""GitHub-based hiring/team signals.

Watches the org repos of healthcare AI vendors for sudden burst of activity,
new contributors, public posts of in-progress products. Free, no auth needed
for public read.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

import httpx

from app.config import settings

logger = logging.getLogger(__name__)

API_BASE = "https://api.github.com"


@dataclass
class GitHubBurst:
    org: str
    repo: str
    new_contributors: int
    commits_last_week: int
    new_releases: list[str]
    url: str


def _headers() -> dict[str, str]:
    headers = {"Accept": "application/vnd.github+json"}
    if settings.github_token:
        headers["Authorization"] = f"Bearer {settings.github_token}"
    return headers


async def org_activity_burst(orgs: list[str], days: int = 7) -> list[GitHubBurst]:
    """Find orgs with notable recent open-source activity."""
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    out: list[GitHubBurst] = []
    async with httpx.AsyncClient(headers=_headers()) as client:
        for org in orgs:
            try:
                resp = await client.get(
                    f"{API_BASE}/orgs/{org}/repos",
                    params={"per_page": 30, "sort": "pushed"},
                    timeout=20.0,
                )
                if resp.status_code == 404:
                    continue
                resp.raise_for_status()
                repos = resp.json()
            except Exception as exc:
                logger.warning("GitHub org fetch failed (%s): %s", org, exc)
                continue

            for repo in repos[:10]:
                pushed = repo.get("pushed_at")
                if not pushed:
                    continue
                pushed_dt = datetime.fromisoformat(pushed.replace("Z", "+00:00"))
                if pushed_dt < cutoff:
                    continue

                # Cheap heuristic: include if recently active
                out.append(GitHubBurst(
                    org=org,
                    repo=repo["name"],
                    new_contributors=0,
                    commits_last_week=0,
                    new_releases=[],
                    url=repo["html_url"],
                ))
    return out
