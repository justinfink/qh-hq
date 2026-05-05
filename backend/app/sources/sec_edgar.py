"""SEC EDGAR client for healthcare AI funding/M&A signals.

Free, official API. Documents must be requested with a User-Agent header
identifying who is making the request (SEC requirement).
"""
from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any

import httpx

logger = logging.getLogger(__name__)

USER_AGENT = "QH-HQ-Intel justin@justinryanventures.com"


@dataclass
class EdgarFiling:
    cik: str
    company_name: str
    form_type: str
    filing_date: str
    accession_number: str
    primary_document: str
    url: str

    @property
    def detected_at(self) -> datetime:
        return datetime.fromisoformat(self.filing_date).replace(tzinfo=timezone.utc)


async def search_recent_filings(
    form_types: list[str] | None = None,
    days: int = 7,
) -> list[EdgarFiling]:
    """Pull recent filings of interest. Free EDGAR endpoint.

    Form types of interest:
      D / D/A   — exempt private offering (Regulation D, indicates a funding round)
      8-K       — material events (M&A, leadership changes, partnerships)
      S-1       — IPO registration
    """
    form_types = form_types or ["D", "D/A", "8-K", "S-1"]
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)

    out: list[EdgarFiling] = []
    async with httpx.AsyncClient(headers={"User-Agent": USER_AGENT}) as client:
        for form_type in form_types:
            url = (
                "https://efts.sec.gov/LATEST/search-index?"
                f"forms={form_type}"
                f"&dateRange=custom&startdt={cutoff.strftime('%Y-%m-%d')}"
                f"&enddt={datetime.now(timezone.utc).strftime('%Y-%m-%d')}"
            )
            try:
                resp = await client.get(url, timeout=20.0)
                resp.raise_for_status()
                data = resp.json()
            except Exception as exc:
                logger.warning("EDGAR search failed (%s): %s", form_type, exc)
                continue

            for hit in data.get("hits", {}).get("hits", [])[:50]:
                src = hit.get("_source", {})
                cik = src.get("ciks", [""])[0]
                accession = hit.get("_id", "")
                primary = src.get("display_names", ["unknown"])[0]
                filing_date = src.get("file_date", "")
                doc = src.get("xsl", "") or src.get("file_name", "")
                if not (cik and accession):
                    continue
                acc_no_dashes = accession.replace("-", "")
                doc_url = f"https://www.sec.gov/Archives/edgar/data/{cik}/{acc_no_dashes}/{doc}"
                out.append(EdgarFiling(
                    cik=cik,
                    company_name=primary,
                    form_type=form_type,
                    filing_date=filing_date,
                    accession_number=accession,
                    primary_document=doc,
                    url=doc_url,
                ))
    return out


async def filter_healthcare_ai_filings(
    filings: list[EdgarFiling],
    keyword_bank: list[str] | None = None,
) -> list[EdgarFiling]:
    """Lightweight filter: keep filings whose company name matches our keyword bank.

    For deeper filtering, the news_scout agent uses LLM-based classification.
    """
    keyword_bank = keyword_bank or [
        "health", "medical", "clinical", "hospital", "pharma", "bio",
        "diagnos", "patient", "care", "ai", "artificial intelligence",
        "rx", "therapeut", "med",
    ]
    kb_lower = [k.lower() for k in keyword_bank]
    out: list[EdgarFiling] = []
    for f in filings:
        name_lower = f.company_name.lower()
        if any(kw in name_lower for kw in kb_lower):
            out.append(f)
    return out
