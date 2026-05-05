"""Seed runner. Loads research-grounded data into Supabase with embeddings.

Idempotent: each entity is upserted by name (orgs, contacts) or code (initiatives).
Re-running is safe — it updates rather than duplicates.

Usage:
    python -m app.data.seed_runner
"""
from __future__ import annotations

import asyncio
import json
import logging
from datetime import datetime, timezone
from uuid import uuid4

from app.data.seed_organizations import (
    QH_FOCAL, CUSTOMERS, PROSPECTS, COMPETITORS, PARTNERS, REGULATORS,
)
from app.data.seed_contacts import CONTACTS
from app.data.seed_initiatives import INITIATIVES, WORKSTREAMS
from app.data.seed_signals import SEED_SIGNALS
from app.data.seed_implications import SEED_IMPLICATIONS
from app.data.seed_dynamics import merge_dynamics_into_orgs
from app.db.client import get_supabase
from app.services.embeddings import embed_batch

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def _embed_text_for_org(org: dict) -> str:
    parts = [
        org["name"],
        org.get("short_name", "") or "",
        org.get("description", "") or "",
        " ".join(f"{k}: {v}" for k, v in (org.get("metadata") or {}).items() if isinstance(v, (str, int, float))),
    ]
    return "\n".join(p for p in parts if p)


def _embed_text_for_initiative(init: dict) -> str:
    parts = [
        init["name"],
        init.get("thesis", "") or "",
        f"Stage: {init['stage']}, Confidence: {init.get('confidence')}, Velocity: {init.get('velocity')}",
        f"Top blocker: {init.get('top_blocker', '')}",
        f"Next milestone: {init.get('next_milestone', '')}",
    ]
    return "\n".join(p for p in parts if p)


def _embed_text_for_signal(sig: dict) -> str:
    return f"{sig['title']}\n\n{sig.get('summary', '') or ''}"


async def seed_organizations() -> dict[str, str]:
    """Upsert all orgs (focal + customers + prospects + competitors + partners + regulators).
    Returns name->id map.
    """
    sb = get_supabase()
    all_orgs = [QH_FOCAL] + CUSTOMERS + PROSPECTS + COMPETITORS + PARTNERS + REGULATORS
    all_orgs = merge_dynamics_into_orgs(all_orgs)
    logger.info("Embedding %d organizations", len(all_orgs))
    embeddings = await embed_batch([_embed_text_for_org(o) for o in all_orgs])

    name_to_id: dict[str, str] = {}
    for org, emb in zip(all_orgs, embeddings):
        existing = sb.table("organizations").select("id").eq("name", org["name"]).execute()
        if existing.data:
            org_id = existing.data[0]["id"]
            sb.table("organizations").update({
                "short_name": org.get("short_name"),
                "org_type": org["org_type"],
                "relationship": org["relationship"],
                "hq_city": org.get("hq_city"),
                "hq_state": org.get("hq_state"),
                "region": org.get("region"),
                "size_label": org.get("size_label"),
                "size_metric": org.get("size_metric"),
                "size_value": org.get("size_value"),
                "description": org.get("description"),
                "homepage_url": org.get("homepage_url"),
                "metadata": org.get("metadata") or {},
                "embedding": emb,
            }).eq("id", org_id).execute()
        else:
            org_id = str(uuid4())
            sb.table("organizations").insert({
                "id": org_id,
                "name": org["name"],
                "short_name": org.get("short_name"),
                "org_type": org["org_type"],
                "relationship": org["relationship"],
                "hq_city": org.get("hq_city"),
                "hq_state": org.get("hq_state"),
                "region": org.get("region"),
                "size_label": org.get("size_label"),
                "size_metric": org.get("size_metric"),
                "size_value": org.get("size_value"),
                "description": org.get("description"),
                "homepage_url": org.get("homepage_url"),
                "metadata": org.get("metadata") or {},
                "embedding": emb,
            }).execute()
        name_to_id[org["name"]] = org_id
    logger.info("Seeded %d organizations", len(all_orgs))
    return name_to_id


async def seed_contacts(org_map: dict[str, str]) -> None:
    sb = get_supabase()
    for c in CONTACTS:
        org_id = org_map.get(c["org"])
        if not org_id:
            logger.warning("Skipping contact %s — unknown org %s", c["name"], c["org"])
            continue
        existing = sb.table("contacts").select("id").eq("organization_id", org_id).eq("name", c["name"]).execute()
        payload = {
            "organization_id": org_id,
            "name": c["name"],
            "title": c.get("title"),
            "role_category": c.get("role_category"),
            "linkedin_url": c.get("linkedin"),
            "notes": c.get("notes"),
        }
        if existing.data:
            sb.table("contacts").update(payload).eq("id", existing.data[0]["id"]).execute()
        else:
            sb.table("contacts").insert(payload).execute()
    logger.info("Seeded %d contacts", len(CONTACTS))


async def seed_initiatives() -> dict[str, str]:
    sb = get_supabase()
    logger.info("Embedding %d initiatives", len(INITIATIVES))
    embeddings = await embed_batch([_embed_text_for_initiative(i) for i in INITIATIVES])

    code_to_id: dict[str, str] = {}
    for init, emb in zip(INITIATIVES, embeddings):
        existing = sb.table("initiatives").select("id").eq("code", init["code"]).execute()
        payload = {
            "code": init["code"],
            "name": init["name"],
            "kind": init["kind"],
            "thesis": init.get("thesis"),
            "stage": init["stage"],
            "confidence": init.get("confidence"),
            "velocity": init.get("velocity"),
            "primary_owner": init.get("primary_owner"),
            "exec_sponsor": init.get("exec_sponsor"),
            "fte_allocated": init.get("fte_allocated"),
            "spend_quarterly_usd": init.get("spend_quarterly_usd"),
            "target_revenue_year_one_usd": init.get("target_revenue_year_one_usd"),
            "target_design_partners": init.get("target_design_partners"),
            "current_design_partners": init.get("current_design_partners", 0),
            "top_blocker": init.get("top_blocker"),
            "next_milestone": init.get("next_milestone"),
            "next_milestone_date": init.get("next_milestone_date").isoformat() if init.get("next_milestone_date") else None,
            "metadata": init.get("metadata") or {},
            "embedding": emb,
        }
        if existing.data:
            init_id = existing.data[0]["id"]
            sb.table("initiatives").update(payload).eq("id", init_id).execute()
        else:
            init_id = str(uuid4())
            sb.table("initiatives").insert({**payload, "id": init_id}).execute()
        code_to_id[init["code"]] = init_id
    logger.info("Seeded %d initiatives", len(INITIATIVES))
    return code_to_id


async def seed_workstreams(init_map: dict[str, str]) -> None:
    sb = get_supabase()
    for ws in WORKSTREAMS:
        init_id = init_map.get(ws["initiative_code"])
        if not init_id:
            continue
        existing = sb.table("workstreams").select("id").eq("initiative_id", init_id).eq("kind", ws["kind"]).execute()
        payload = {
            "initiative_id": init_id,
            "kind": ws["kind"],
            "status": ws.get("status"),
            "owner": ws.get("owner"),
            "summary": ws.get("summary"),
            "next_action": ws.get("next_action"),
            "next_action_due": ws.get("next_action_due").isoformat() if ws.get("next_action_due") else None,
            "last_movement_at": ws.get("last_movement_at"),
        }
        if existing.data:
            sb.table("workstreams").update(payload).eq("id", existing.data[0]["id"]).execute()
        else:
            sb.table("workstreams").insert(payload).execute()
    logger.info("Seeded %d workstreams", len(WORKSTREAMS))


async def seed_signals(org_map: dict[str, str]) -> None:
    sb = get_supabase()
    logger.info("Embedding %d seed signals", len(SEED_SIGNALS))
    embeddings = await embed_batch([_embed_text_for_signal(s) for s in SEED_SIGNALS])

    for sig, emb in zip(SEED_SIGNALS, embeddings):
        existing = sb.table("signals").select("id").eq("source_url", sig["source_url"]).execute()
        primary_org_id = org_map.get(sig.get("primary_org_name")) if sig.get("primary_org_name") else None
        payload = {
            "signal_kind": sig["signal_kind"],
            "title": sig["title"],
            "summary": sig.get("summary"),
            "source_name": sig.get("source_name"),
            "source_url": sig.get("source_url"),
            "source_type": sig.get("source_type"),
            "primary_organization_id": primary_org_id,
            "occurred_at": sig.get("occurred_at"),
            "raw_payload": {"is_research_seed": True},
            "embedding": emb,
            "is_seed": True,
        }
        if existing.data:
            sb.table("signals").update(payload).eq("id", existing.data[0]["id"]).execute()
        else:
            sb.table("signals").insert({**payload, "id": str(uuid4())}).execute()
    logger.info("Seeded %d signals", len(SEED_SIGNALS))


async def seed_implications(org_map: dict[str, str], init_map: dict[str, str]) -> int:
    sb = get_supabase()
    # Build a signal-url -> id map
    sigs_rows = sb.table("signals").select("id,source_url").execute().data
    sig_map = {r["source_url"]: r["id"] for r in sigs_rows if r.get("source_url")}

    inserted = 0
    for imp in SEED_IMPLICATIONS:
        sig_id = sig_map.get(imp["signal_source_url"])
        if not sig_id:
            logger.warning("Skipping implication — signal not found: %s", imp["signal_source_url"][:60])
            continue
        existing = sb.table("implications").select("id").eq("signal_id", sig_id).eq("headline", imp["headline"]).execute()
        payload = {
            "signal_id": sig_id,
            "initiative_id": init_map.get(imp.get("initiative_code")) if imp.get("initiative_code") else None,
            "customer_org_id": org_map.get(imp.get("customer_org_name")) if imp.get("customer_org_name") else None,
            "severity": imp["severity"],
            "confidence_score": imp.get("confidence_score"),
            "headline": imp["headline"],
            "reasoning": imp["reasoning"],
            "recommended_action": imp.get("recommended_action"),
            "recommended_owner": imp.get("recommended_owner"),
            "recommended_by_date": imp.get("recommended_by_date"),
            "status": "open",
        }
        if existing.data:
            sb.table("implications").update(payload).eq("id", existing.data[0]["id"]).execute()
        else:
            sb.table("implications").insert({**payload, "id": str(__import__('uuid').uuid4())}).execute()
            inserted += 1
    logger.info("Seeded %d implications (total %d)", inserted, len(SEED_IMPLICATIONS))
    return inserted


async def main():
    logger.info("=" * 60)
    logger.info("QH HQ seed runner starting")
    logger.info("=" * 60)
    org_map = await seed_organizations()
    await seed_contacts(org_map)
    init_map = await seed_initiatives()
    await seed_workstreams(init_map)
    await seed_signals(org_map)
    await seed_implications(org_map, init_map)
    logger.info("=" * 60)
    logger.info("Seed complete: %d orgs, %d contacts, %d initiatives, %d workstreams, %d signals, %d implications",
                len(org_map), len(CONTACTS), len(init_map), len(WORKSTREAMS), len(SEED_SIGNALS), len(SEED_IMPLICATIONS))
    logger.info("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
