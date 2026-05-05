"""Implication Mapper: turns each new signal into QH-specific reasoning.

For each signal, the agent:
  1. Retrieves the most semantically relevant initiatives (via pgvector)
  2. Retrieves the most semantically relevant customers (via pgvector)
  3. Asks Opus to reason about implication for QH
  4. Persists structured implications with severity + recommended action
"""
from __future__ import annotations

import json
import logging
from typing import Any
from uuid import uuid4

from app.agents.base import Agent, RunContext
from app.db.client import get_supabase
from app.services.embeddings import embed_text

logger = logging.getLogger(__name__)


SYSTEM_PROMPT = """You are a senior strategic analyst inside Qualified Health's Office of the CEO.

QH context:
- Series B healthcare AI governance platform ($125M raise, NEA-led, March 2026)
- Core: clinical AI governance, healthcare-specific agent creation, real-time algorithm \
monitoring + audit logging
- Already in health systems representing ~7% of US hospital revenue (500K+ providers)
- Most defensible asset: HTI-1 Decision Support Intervention source attributes + cross-walks to \
NAIC, Colorado AI Act, Joint Commission RUHD, EU AI Act
- Strategic positioning: the "governed operating layer" / runtime layer for clinical AI
- Top existential threats: Epic Factory (native EHR governance), foundation-model vendors going \
direct (OpenAI Healthcare, Anthropic Claude for Healthcare)
- New business lines being explored: ASC vertical, Pharma/Life-Sciences governance, Payer-side AI \
audit (CMMI WISeR-anchored), Governed Model Marketplace for 3rd-party vendors, Specialty practice MSOs

Given a fresh external signal and the most relevant QH initiatives + customer accounts (provided), \
write the implication for QH. Be specific. Name people and dollars when present. Avoid generic \
hedging. If the signal has no real implication, say so explicitly with severity=fyi.

Output a JSON object only:
{
  "headline": "<one sentence, ≤120 chars>",
  "reasoning": "<2-4 sentences. Why this matters for QH specifically. Cite the relevant initiative \
or customer if applicable.>",
  "severity": "critical|high|medium|low|fyi",
  "confidence_score": <0.0-1.0>,
  "best_initiative_id": "<uuid or null>",
  "best_customer_org_id": "<uuid or null>",
  "recommended_action": "<one concrete next step. Include owner role + timing.>",
  "recommended_owner": "<role e.g. 'Head of Office of CEO' or null>",
  "recommended_by_date": "<YYYY-MM-DD or null>"
}

Severity guide:
- critical: existential or near-term competitive threat; needs CEO attention
- high: material to a current initiative; needs Head of OoC attention this week
- medium: moves a workstream; needs initiative owner attention this week
- low: useful context, file for next strategic review
- fyi: tangentially relevant; logged but no action

Never invent facts. Only reason from what's in the signal.
"""


class ImplicationMapper(Agent):
    slug = "implication_mapper"
    name = "Implication Mapper"
    role = "Reasons signals into QH-specific implications"
    description = "For each new signal, retrieves relevant initiatives + customers, drafts an exec implication."
    model = "claude-opus-4-7"

    K_INITIATIVES = 3
    K_CUSTOMERS = 4
    MAX_SIGNALS_PER_RUN = 3  # serverless 30s budget; ~7s per Opus call

    async def run(self, ctx: RunContext, signal_id: str | None = None, **kwargs: Any) -> dict[str, Any]:
        sb = get_supabase()
        if signal_id:
            signals = sb.table("signals").select("*").eq("id", signal_id).execute().data
        else:
            ctx.emit("thought", "Finding recent signals without implications")
            recent = sb.table("signals").select("id,title,summary,source_name,source_url,signal_kind,embedding,primary_organization_id") \
                .order("detected_at", desc=True).limit(50).execute().data
            existing_implication_signal_ids = {
                row["signal_id"]
                for row in sb.table("implications").select("signal_id").execute().data
            }
            signals = [s for s in recent if s["id"] not in existing_implication_signal_ids]
            ctx.emit("decision", f"{len(signals)} signals without implications", new_signals=len(signals))

        if not signals:
            return {"implications_generated": 0}

        signals = signals[: self.MAX_SIGNALS_PER_RUN]
        ctx.emit("thought", f"Processing {len(signals)} (capped per serverless time budget)")

        generated = 0
        for sig in signals:
            try:
                imp = await self._map_one(ctx, sig)
                if imp:
                    generated += 1
            except Exception as exc:
                ctx.emit("error", f"Failed to map signal {sig['id']}: {exc}")
                continue

        ctx.implications_generated = generated
        return {"implications_generated": generated}

    async def _map_one(self, ctx: RunContext, sig: dict) -> dict | None:
        sb = get_supabase()
        ctx.emit("thought", f"Reasoning: {sig['title'][:80]}", signal_id=sig["id"])

        # Get embedding (compute if missing)
        emb = sig.get("embedding")
        if not emb:
            emb = await embed_text(f"{sig['title']}\n\n{sig.get('summary') or ''}")

        # Retrieve top-k initiatives + customers via pgvector
        initiatives = await self._knn_initiatives(emb, self.K_INITIATIVES)
        customers = await self._knn_customers(emb, self.K_CUSTOMERS)
        ctx.emit("tool_result", f"Retrieved {len(initiatives)} initiatives, {len(customers)} customers",
                 initiative_ids=[i["id"] for i in initiatives],
                 customer_ids=[c["id"] for c in customers])

        # Compose user message
        user_msg = json.dumps({
            "signal": {
                "title": sig["title"],
                "summary": sig.get("summary"),
                "source_name": sig.get("source_name"),
                "source_url": sig.get("source_url"),
                "signal_kind": sig["signal_kind"],
            },
            "candidate_initiatives": [
                {"id": i["id"], "name": i["name"], "thesis": i.get("thesis"), "stage": i.get("stage")}
                for i in initiatives
            ],
            "candidate_customers": [
                {"id": c["id"], "name": c["name"], "org_type": c.get("org_type"), "relationship": c.get("relationship")}
                for c in customers
            ],
        }, default=str)

        ctx.emit("tool_call", "Opus reasoning about implication", model=self.model)
        resp = await self.anthropic.messages.create(
            model=self.model,
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_msg}],
        )
        ctx.tokens_input += resp.usage.input_tokens
        ctx.tokens_output += resp.usage.output_tokens

        text = resp.content[0].text  # type: ignore[union-attr]
        try:
            j = self._parse_json(text)
        except Exception as exc:
            ctx.emit("error", f"Could not parse implication JSON: {exc}")
            return None

        sb.table("implications").insert({
            "id": str(uuid4()),
            "signal_id": sig["id"],
            "initiative_id": j.get("best_initiative_id"),
            "customer_org_id": j.get("best_customer_org_id"),
            "severity": j.get("severity", "medium"),
            "confidence_score": float(j.get("confidence_score", 0.6)),
            "headline": j["headline"],
            "reasoning": j["reasoning"],
            "recommended_action": j.get("recommended_action"),
            "recommended_owner": j.get("recommended_owner"),
            "recommended_by_date": j.get("recommended_by_date"),
            "agent_run_id": ctx.run_id,
        }).execute()
        ctx.emit("decision", f"{j.get('severity', 'medium').upper()}: {j['headline'][:100]}",
                 severity=j.get("severity"))
        return j

    async def _knn_initiatives(self, embedding: list[float], k: int) -> list[dict]:
        sb = get_supabase()
        rpc = sb.rpc("match_initiatives", {"query_embedding": embedding, "match_count": k}).execute()
        return rpc.data or []

    async def _knn_customers(self, embedding: list[float], k: int) -> list[dict]:
        sb = get_supabase()
        rpc = sb.rpc("match_organizations", {"query_embedding": embedding, "match_count": k}).execute()
        return rpc.data or []

    def _parse_json(self, text: str) -> dict:
        text = text.strip()
        if text.startswith("```"):
            text = text.split("```", 2)[1]
            if text.startswith("json"):
                text = text[4:]
            text = text.strip("` \n")
        return json.loads(text)
