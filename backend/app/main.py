from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.api import signals, initiatives, customers, agents, query
from app.services.scheduler import scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler.start()
    yield
    scheduler.shutdown(wait=False)


app = FastAPI(
    title="QH HQ Backend",
    version="0.2.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(signals.router, prefix="/api/signals", tags=["signals"])
app.include_router(initiatives.router, prefix="/api/initiatives", tags=["initiatives"])
app.include_router(customers.router, prefix="/api/customers", tags=["customers"])
app.include_router(agents.router, prefix="/api/agents", tags=["agents"])
app.include_router(query.router, prefix="/api/query", tags=["query"])


@app.get("/api/health")
async def health():
    return {"status": "ok", "version": "0.2.0"}
