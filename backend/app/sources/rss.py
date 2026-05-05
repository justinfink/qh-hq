"""RSS-based source for healthcare AI news.

All feeds below are free and publicly accessible. Each entry is normalized
into a candidate signal that the news_scout agent can decide to ingest.
"""
from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any
from urllib.parse import urlparse

import feedparser
import httpx

logger = logging.getLogger(__name__)


@dataclass
class FeedSource:
    name: str
    url: str
    weight: float = 1.0  # Used by ranker to bias toward higher-quality sources
    category: str = "news"


# Curated list. Bias toward feeds that are consistently rich in healthcare AI signal.
HEALTHCARE_FEEDS: list[FeedSource] = [
    FeedSource("Fierce Healthcare", "https://www.fiercehealthcare.com/rss.xml", 1.0),
    FeedSource("Fierce Biotech", "https://www.fiercebiotech.com/rss.xml", 0.8),
    FeedSource("Fierce Pharma", "https://www.fiercepharma.com/rss.xml", 0.8),
    FeedSource("HealthcareITNews", "https://www.healthcareitnews.com/home/feed", 1.0),
    FeedSource("HealthcareITNews AI", "https://www.healthcareitnews.com/topic/artificial-intelligence/feed", 1.2),
    FeedSource("STAT News", "https://www.statnews.com/feed/", 1.1),
    FeedSource("Modern Healthcare", "https://www.modernhealthcare.com/section/rss?path=/", 0.9),
    FeedSource("Healthcare Innovation", "https://www.hcinnovationgroup.com/rss.xml", 0.9),
    FeedSource("Becker's Hospital Review", "https://www.beckershospitalreview.com/feed", 0.9),
    FeedSource("MedCity News", "https://medcitynews.com/feed/", 1.0),
    FeedSource("Endpoints News", "https://endpts.com/feed/", 0.9),
    FeedSource("Politico Pulse", "https://rss.politico.com/healthcare.xml", 0.9),
    FeedSource("Health Affairs Blog", "https://www.healthaffairs.org/do/rss/site/healthaffairs/?type=blog", 0.8),
    FeedSource("CMS Newsroom", "https://www.cms.gov/about-cms/contact/newsroom/feed", 1.3, category="regulatory"),
    FeedSource("FDA News", "https://www.fda.gov/about-fda/contact-fda/stay-informed/rss-feeds/medical-devices/rss.xml", 1.2, category="regulatory"),
    FeedSource("ONC News", "https://www.healthit.gov/buzz-blog/feed", 1.2, category="regulatory"),
    FeedSource("KFF Health News", "https://kffhealthnews.org/feed/", 0.9),
]


@dataclass
class RawSignal:
    title: str
    summary: str
    url: str
    source_name: str
    published_at: datetime | None
    category: str = "news"

    @property
    def stable_id(self) -> str:
        return self.url


async def fetch_feed(client: httpx.AsyncClient, source: FeedSource) -> list[RawSignal]:
    try:
        resp = await client.get(source.url, follow_redirects=True, timeout=20.0)
        resp.raise_for_status()
    except Exception as exc:
        logger.warning("Feed fetch failed: %s (%s)", source.name, exc)
        return []

    parsed = feedparser.parse(resp.content)
    out: list[RawSignal] = []
    for entry in parsed.entries:
        title = (entry.get("title") or "").strip()
        if not title:
            continue
        summary = (entry.get("summary") or entry.get("description") or "").strip()
        # Strip HTML tags from summary
        if "<" in summary:
            from bs4 import BeautifulSoup
            summary = BeautifulSoup(summary, "html.parser").get_text(" ", strip=True)
        url = entry.get("link") or entry.get("id") or ""
        if not url:
            continue
        published_at = _parse_date(entry)
        out.append(RawSignal(
            title=title,
            summary=summary[:1500],
            url=url,
            source_name=source.name,
            published_at=published_at,
            category=source.category,
        ))
    return out


def _parse_date(entry: Any) -> datetime | None:
    for key in ("published_parsed", "updated_parsed"):
        struct = entry.get(key)
        if struct:
            try:
                return datetime(*struct[:6], tzinfo=timezone.utc)
            except (TypeError, ValueError):
                continue
    return None


async def fetch_all_feeds(
    sources: list[FeedSource] | None = None,
    concurrency: int = 6,
) -> list[RawSignal]:
    sources = sources or HEALTHCARE_FEEDS
    sem = asyncio.Semaphore(concurrency)

    async with httpx.AsyncClient(headers={
        "User-Agent": "QH-HQ-Intel/0.1 (justin@justinryanventures.com)",
    }) as client:
        async def bound_fetch(s: FeedSource) -> list[RawSignal]:
            async with sem:
                return await fetch_feed(client, s)
        results = await asyncio.gather(*(bound_fetch(s) for s in sources))

    out: list[RawSignal] = []
    for batch in results:
        out.extend(batch)
    return out
