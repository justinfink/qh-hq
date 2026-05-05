"""ClinicalTrials.gov client for pharma + AI signals.

Free, official API v2. Used to spot trials with AI/ML inclusion criteria
or QH-relevant sponsor activity.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import date, timedelta
from typing import Any

import httpx

logger = logging.getLogger(__name__)

API_BASE = "https://clinicaltrials.gov/api/v2"


@dataclass
class TrialRecord:
    nct_id: str
    title: str
    sponsor: str
    sponsor_class: str
    status: str
    posted_date: str
    url: str
    intervention: str
    summary: str


async def search_recent_ai_trials(
    days: int = 30,
    page_size: int = 50,
) -> list[TrialRecord]:
    """Recent trials with AI/ML intervention or related keywords."""
    cutoff = date.today() - timedelta(days=days)
    params = {
        "query.term": '("artificial intelligence" OR "machine learning" OR "large language model" OR "generative AI") AND AREA[FirstPostDate]RANGE[' + cutoff.isoformat() + ',MAX]',
        "pageSize": page_size,
        "format": "json",
    }

    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(f"{API_BASE}/studies", params=params, timeout=30.0)
            resp.raise_for_status()
            data = resp.json()
        except Exception as exc:
            logger.warning("ClinicalTrials search failed: %s", exc)
            return []

    out: list[TrialRecord] = []
    for study in data.get("studies", []):
        proto = study.get("protocolSection", {})
        ident = proto.get("identificationModule", {})
        sponsor_mod = proto.get("sponsorCollaboratorsModule", {})
        status_mod = proto.get("statusModule", {})
        intervention_mod = proto.get("armsInterventionsModule", {})
        desc = proto.get("descriptionModule", {})

        nct_id = ident.get("nctId", "")
        if not nct_id:
            continue

        out.append(TrialRecord(
            nct_id=nct_id,
            title=ident.get("briefTitle", ""),
            sponsor=sponsor_mod.get("leadSponsor", {}).get("name", "Unknown"),
            sponsor_class=sponsor_mod.get("leadSponsor", {}).get("class", "Unknown"),
            status=status_mod.get("overallStatus", "Unknown"),
            posted_date=status_mod.get("studyFirstPostDateStruct", {}).get("date", ""),
            url=f"https://clinicaltrials.gov/study/{nct_id}",
            intervention=", ".join(
                i.get("name", "") for i in intervention_mod.get("interventions", [])[:3]
            ),
            summary=(desc.get("briefSummary") or "")[:500],
        ))
    return out
