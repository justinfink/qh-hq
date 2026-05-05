"""News Scout: pulls RSS + ClinicalTrials.gov + EDGAR, dedupes, embeds, persists.

Fast triage agent. Uses Haiku for the relevance pass to keep cost low.
Real signals get embedded and written to `signals` for downstream agents
(implication_mapper, ranker) to operate on.
"""
from __future__ import annotations

import asyncio
import json
import logging
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from app.agents.base import Agent, RunContext
from app.config import settings
from app.db.client import get_supabase
from app.services.embeddings import embed_batch
from app.sources.rss import RawSignal, fetch_all_feeds

logger = logging.getLogger(__name__)


RELEVANCE_PROMPT = """You triage news for Qualified Health's Office of CEO. QH is a Series B healthcare AI \
governance platform. They sell to IDNs, run clinical AI runtime + audit/monitoring, and are exploring \
new business lines: ASC vertical, Pharma/Life-Sciences governance, Payer-side AI audit, a governed \
model marketplace for third-party clinical AI vendors, and Specialty practice networks.

For each candidate news item, decide if it is RELEVANT to QH's strategic decision-making. Relevance \
means: tells QH something material about (a) a competitor or potentially-competing vendor, (b) a \
customer or prospect IDN/health system AI deployment, (c) a partner candidate, (d) a regulatory \
shift affecting clinical AI governance, (e) a funding or M&A event in healthcare AI.

Return a JSON array. For each input item, output:
{"id": "<input id>", "relevant": true|false, "kind": "<signal_kind>", \
"primary_org": "<canonical org name or null>", "rationale": "<one short sentence>"}

signal_kind enum: funding | product_launch | partnership | customer_win | leadership_change | \
regulatory | m_and_a | public_failure | conference_talk | hiring_signal | patent | thought_leadership | other

Be strict about relevance. If it's generic healthcare news with no AI angle, mark relevant=false. \
If it's pure consumer health news, mark relevant=false. Be precise in primary_org canonicalization \
(use the canonical company name, not slug variants).

Output JSON only, no surrounding prose.
"""


class NewsScout(Agent):
    slug = "news_scout"
    name = "News Scout"
    role = "Source ingestion + first-pass relevance triage"
    description = "Polls RSS, EDGAR, ClinicalTrials.gov; dedupes; classifies; persists signals."
    model = "claude-haiku-4-5-20251001"

    BATCH_SIZE = 25  # number of items per Haiku triage call

    async def run(self, ctx: RunContext, **kwargs: Any) -> dict[str, Any]:
        ctx.emit("thought", "Polling 17 RSS feeds for healthcare + regulatory signal")
        raws = await fetch_all_feeds()
        ctx.emit("tool_result", f"Pulled {len(raws)} candidates", source_count=17, candidate_count=len(raws))

        # Dedupe against existing signals by source_url
        ctx.emit("thought", "Deduplicating against existing signals in DB")
        sb = get_supabase()
        existing_urls = {
            row["source_url"]
            for row in sb.table("signals").select("source_url").not_.is_("source_url", None).execute().data
        }
        novel = [r for r in raws if r.url not in existing_urls]
        ctx.emit("decision", f"{len(novel)} novel candidates after dedupe", duplicates=len(raws) - len(novel))

        if not novel:
            return {"signals_ingested": 0, "novel_candidates": 0}

        # Triage in batches with Haiku
        accepted: list[tuple[RawSignal, dict]] = []
        for batch_start in range(0, len(novel), self.BATCH_SIZE):
            batch = novel[batch_start : batch_start + self.BATCH_SIZE]
            triaged = await self._triage_batch(ctx, batch)
            accepted.extend(triaged)

        ctx.emit("decision", f"{len(accepted)} candidates passed relevance filter", accepted_count=len(accepted))

        if not accepted:
            return {"signals_ingested": 0, "novel_candidates": len(novel)}

        # Embed accepted candidates
        ctx.emit("tool_call", "Embedding accepted candidates", embedding_model="voyage-3-large")
        texts = [f"{r.title}\n\n{r.summary}" for r, _ in accepted]
        vectors = await embed_batch(texts, input_type="document")
        ctx.emit("tool_result", f"Embedded {len(vectors)} candidates")

        # Persist
        rows = []
        for (raw, judgment), vec in zip(accepted, vectors):
            primary_org_id = await self._find_or_create_org(judgment.get("primary_org"))
            rows.append({
                "id": str(uuid4()),
                "signal_kind": judgment.get("kind", "other"),
                "title": raw.title,
                "summary": raw.summary,
                "source_name": raw.source_name,
                "source_url": raw.url,
                "source_type": "rss",
                "primary_organization_id": primary_org_id,
                "detected_at": datetime.now(timezone.utc).isoformat(),
                "occurred_at": raw.published_at.isoformat() if raw.published_at else None,
                "raw_payload": {"triage_rationale": judgment.get("rationale", "")},
                "embedding": vec,
                "is_seed": False,
            })

        sb.table("signals").insert(rows).execute()
        ctx.signals_ingested = len(rows)
        ctx.emit("complete", f"Persisted {len(rows)} new signals")
        return {
            "signals_ingested": len(rows),
            "novel_candidates": len(novel),
            "duplicates_skipped": len(raws) - len(novel),
        }

    async def _triage_batch(
        self, ctx: RunContext, batch: list[RawSignal]
    ) -> list[tuple[RawSignal, dict]]:
        items = [
            {
                "id": i,
                "title": r.title,
                "source": r.source_name,
                "summary": r.summary[:600],
            }
            for i, r in enumerate(batch)
        ]
        ctx.emit("tool_call", f"Haiku triaging batch of {len(batch)}", batch_size=len(batch))
        try:
            resp = await self.anthropic.messages.create(
                model=self.model,
                max_tokens=2048,
                system=RELEVANCE_PROMPT,
                messages=[{
                    "role": "user",
                    "content": json.dumps(items),
                }],
            )
            ctx.tokens_input += resp.usage.input_tokens
            ctx.tokens_output += resp.usage.output_tokens
            text = resp.content[0].text  # type: ignore[union-attr]
            judgments = self._parse_judgments(text)
        except Exception as exc:
            ctx.emit("error", f"Triage batch failed: {exc}")
            return []

        out: list[tuple[RawSignal, dict]] = []
        judgment_by_id = {j.get("id"): j for j in judgments}
        for i, raw in enumerate(batch):
            j = judgment_by_id.get(i) or {}
            if j.get("relevant"):
                out.append((raw, j))
        return out

    def _parse_judgments(self, text: str) -> list[dict]:
        text = text.strip()
        # Strip code fences if present
        if text.startswith("```"):
            text = text.split("```", 2)[1]
            if text.startswith("json"):
                text = text[4:]
            text = text.strip("` \n")
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            # Try to extract array
            start = text.find("[")
            end = text.rfind("]")
            if start >= 0 and end > start:
                try:
                    return json.loads(text[start : end + 1])
                except json.JSONDecodeError:
                    pass
        return []

    async def _find_or_create_org(self, name: str | None) -> str | None:
        if not name or not name.strip():
            return None
        sb = get_supabase()
        # Exact match first
        existing = sb.table("organizations").select("id").ilike("name", name).limit(1).execute()
        if existing.data:
            return existing.data[0]["id"]
        # Trigram fuzzy match (handled by trgm index)
        return None  # New orgs only get created with org_classifier agent (out of MVP scope)
