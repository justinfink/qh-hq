"""Ad-hoc semantic query endpoint. Powers the search bar in the terminal."""
from fastapi import APIRouter
from pydantic import BaseModel

from app.db.client import get_supabase
from app.services.embeddings import embed_text

router = APIRouter()


class QueryRequest(BaseModel):
    q: str
    k: int = 8


@router.post("")
async def search(req: QueryRequest):
    """Semantic search across signals + initiatives + customers + documents."""
    vec = await embed_text(req.q, input_type="query")
    sb = get_supabase()

    sigs = sb.rpc("match_signals", {"query_embedding": vec, "match_count": req.k}).execute().data or []
    inits = sb.rpc("match_initiatives", {"query_embedding": vec, "match_count": min(req.k, 5)}).execute().data or []
    orgs = sb.rpc("match_organizations", {"query_embedding": vec, "match_count": min(req.k, 5)}).execute().data or []
    docs = sb.rpc("match_documents", {"query_embedding": vec, "match_count": min(req.k, 5)}).execute().data or []

    return {
        "query": req.q,
        "signals": sigs,
        "initiatives": inits,
        "organizations": orgs,
        "documents": docs,
    }
