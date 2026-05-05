from fastapi import APIRouter

from app.db.client import get_supabase

router = APIRouter()


@router.get("")
async def list_initiatives():
    sb = get_supabase()
    rows = sb.table("initiatives").select(
        "id,code,name,kind,thesis,stage,confidence,velocity,primary_owner,exec_sponsor,"
        "fte_allocated,spend_quarterly_usd,target_revenue_year_one_usd,target_design_partners,current_design_partners,"
        "top_blocker,next_milestone,next_milestone_date,metadata,"
        "workstreams(id,kind,status,owner,summary,next_action,next_action_due,last_movement_at)"
    ).order("kind").order("name").execute().data
    return {"initiatives": rows, "count": len(rows)}


@router.get("/{initiative_id}")
async def get_initiative(initiative_id: str):
    sb = get_supabase()
    rows = sb.table("initiatives").select(
        "*,workstreams(*),initiative_targets(organization_id,status,notes,organizations(id,name,org_type,relationship))"
    ).eq("id", initiative_id).execute().data
    if not rows:
        return {"error": "not_found"}

    init = rows[0]

    # Pull recent implications tied to this initiative
    impls = sb.table("implications").select(
        "id,severity,headline,reasoning,recommended_action,created_at,"
        "signal:signals(id,title,source_name,source_url,detected_at)"
    ).eq("initiative_id", initiative_id).order("created_at", desc=True).limit(20).execute().data
    init["recent_implications"] = impls
    return init
