from datetime import datetime, timedelta, timezone
from typing import Literal

from fastapi import APIRouter, Query

from app.db.client import get_supabase

router = APIRouter()


@router.get("")
async def list_signals(
    severity: Literal["critical", "high", "medium", "low", "fyi"] | None = None,
    days: int = Query(default=30, ge=1, le=365),
    limit: int = Query(default=50, ge=1, le=200),
    initiative_id: str | None = None,
):
    sb = get_supabase()
    cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()

    # Pull signals with joined implications + org
    query = sb.table("signals").select(
        "id,signal_kind,title,summary,source_name,source_url,source_type,detected_at,occurred_at,is_seed,"
        "primary_organization_id,"
        "implications(id,severity,confidence_score,headline,reasoning,recommended_action,recommended_owner,recommended_by_date,rank_score,initiative_id,customer_org_id,status)"
    ).gte("detected_at", cutoff).order("detected_at", desc=True).limit(limit)

    rows = query.execute().data

    # Enrich with org names
    org_ids = {r["primary_organization_id"] for r in rows if r.get("primary_organization_id")}
    org_map: dict[str, dict] = {}
    if org_ids:
        orgs = sb.table("organizations").select("id,name,short_name,org_type,relationship") \
            .in_("id", list(org_ids)).execute().data
        org_map = {o["id"]: o for o in orgs}

    out = []
    for r in rows:
        impls = r.get("implications") or []
        if severity:
            impls = [i for i in impls if i.get("severity") == severity]
            if not impls:
                continue
        # Sort implications by severity (critical first)
        sev_order = {"critical": 0, "high": 1, "medium": 2, "low": 3, "fyi": 4}
        impls.sort(key=lambda i: sev_order.get(i.get("severity", "medium"), 2))

        out.append({
            **{k: v for k, v in r.items() if k != "implications"},
            "implications": impls,
            "primary_organization": org_map.get(r.get("primary_organization_id")) if r.get("primary_organization_id") else None,
        })

    return {"signals": out, "count": len(out)}


@router.get("/feed")
async def feed(
    limit: int = Query(default=25, ge=1, le=100),
):
    """Curated feed for the front-page terminal: signals with at least one implication, \
    ordered by severity then recency."""
    sb = get_supabase()

    # Pull recent implications joined to signals
    impls = sb.table("implications").select(
        "id,severity,confidence_score,headline,reasoning,recommended_action,recommended_owner,recommended_by_date,initiative_id,customer_org_id,status,created_at,"
        "signal:signals(id,signal_kind,title,summary,source_name,source_url,detected_at,occurred_at,primary_organization_id)"
    ).eq("status", "open").order("created_at", desc=True).limit(limit * 2).execute().data

    sev_order = {"critical": 0, "high": 1, "medium": 2, "low": 3, "fyi": 4}
    impls.sort(key=lambda i: (sev_order.get(i.get("severity", "medium"), 2), i.get("created_at") or ""))
    impls = impls[:limit]

    org_ids = {i["signal"]["primary_organization_id"] for i in impls if i["signal"] and i["signal"].get("primary_organization_id")}
    org_map: dict[str, dict] = {}
    if org_ids:
        orgs = sb.table("organizations").select("id,name,short_name,org_type,relationship") \
            .in_("id", list(org_ids)).execute().data
        org_map = {o["id"]: o for o in orgs}

    initiative_ids = {i["initiative_id"] for i in impls if i.get("initiative_id")}
    init_map: dict[str, dict] = {}
    if initiative_ids:
        inits = sb.table("initiatives").select("id,code,name").in_("id", list(initiative_ids)).execute().data
        init_map = {i["id"]: i for i in inits}

    out = []
    for i in impls:
        s = i.get("signal") or {}
        out.append({
            "implication_id": i["id"],
            "severity": i["severity"],
            "confidence_score": i.get("confidence_score"),
            "headline": i["headline"],
            "reasoning": i["reasoning"],
            "recommended_action": i.get("recommended_action"),
            "recommended_owner": i.get("recommended_owner"),
            "recommended_by_date": i.get("recommended_by_date"),
            "created_at": i["created_at"],
            "signal": {
                "id": s.get("id"),
                "title": s.get("title"),
                "summary": s.get("summary"),
                "source_name": s.get("source_name"),
                "source_url": s.get("source_url"),
                "signal_kind": s.get("signal_kind"),
                "detected_at": s.get("detected_at"),
                "occurred_at": s.get("occurred_at"),
            },
            "primary_organization": org_map.get(s.get("primary_organization_id")) if s.get("primary_organization_id") else None,
            "initiative": init_map.get(i.get("initiative_id")) if i.get("initiative_id") else None,
        })

    return {"items": out, "count": len(out)}


@router.get("/{signal_id}")
async def get_signal(signal_id: str):
    sb = get_supabase()
    sig = sb.table("signals").select("*").eq("id", signal_id).execute().data
    if not sig:
        return {"error": "not_found"}
    sig = sig[0]
    impls = sb.table("implications").select("*").eq("signal_id", signal_id).execute().data
    org = None
    if sig.get("primary_organization_id"):
        org = sb.table("organizations").select("*").eq("id", sig["primary_organization_id"]).execute().data
        org = org[0] if org else None
    return {**sig, "implications": impls, "primary_organization": org}
