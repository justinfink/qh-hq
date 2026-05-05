from fastapi import APIRouter, Query

from app.db.client import get_supabase

router = APIRouter()


@router.get("")
async def list_orgs(
    org_type: str | None = None,
    relationship: str | None = None,
    limit: int = Query(default=200, ge=1, le=500),
):
    sb = get_supabase()
    q = sb.table("organizations").select(
        "id,name,short_name,org_type,relationship,hq_city,hq_state,region,size_label,size_metric,size_value,description,homepage_url,metadata"
    ).order("name").limit(limit)
    if org_type:
        q = q.eq("org_type", org_type)
    if relationship:
        q = q.eq("relationship", relationship)
    rows = q.execute().data
    return {"organizations": rows, "count": len(rows)}


@router.get("/{org_id}")
async def get_org(org_id: str):
    sb = get_supabase()
    rows = sb.table("organizations").select("*").eq("id", org_id).execute().data
    if not rows:
        return {"error": "not_found"}
    org = rows[0]

    contacts = sb.table("contacts").select("*").eq("organization_id", org_id).execute().data
    deployments = sb.table("deployments").select(
        "*,product:products(id,name,category,is_qh_product,organization:organizations(id,name))"
    ).eq("customer_org_id", org_id).execute().data
    impls = sb.table("implications").select(
        "id,severity,headline,reasoning,created_at,signal:signals(id,title,source_url,detected_at)"
    ).eq("customer_org_id", org_id).order("created_at", desc=True).limit(20).execute().data

    org["contacts"] = contacts
    org["deployments"] = deployments
    org["recent_implications"] = impls
    return org
