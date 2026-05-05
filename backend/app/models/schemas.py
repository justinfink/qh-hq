"""Pydantic schemas for API responses. Mirrors DB enums."""
from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, Field

OrgType = Literal[
    "idn", "amc", "asc", "specialty_msa", "pharma", "payer",
    "ai_vendor", "governance_competitor", "cloud_provider",
    "ehr_vendor", "thought_leadership", "regulator", "investor", "consultancy", "other",
]

RelationshipToQH = Literal[
    "customer", "pilot", "prospect", "partner", "competitor",
    "investor", "regulator_watch", "ecosystem", "unknown",
]

InitiativeKind = Literal["nbl", "core_product", "partnership", "strategic_project", "internal_op"]
InitiativeStage = Literal["discovery", "greenlight", "pilot", "early_revenue", "scaling", "paused"]
WorkstreamKind = Literal["product", "gtm", "partnerships", "regulatory", "finance"]
Confidence = Literal["high", "medium", "low"]
Velocity = Literal["accelerating", "holding", "slipping"]
SignalSeverity = Literal["critical", "high", "medium", "low", "fyi"]
SignalKind = Literal[
    "funding", "product_launch", "partnership", "customer_win",
    "leadership_change", "regulatory", "m_and_a", "public_failure",
    "conference_talk", "hiring_signal", "patent", "thought_leadership", "other",
]


class Organization(BaseModel):
    id: str
    name: str
    short_name: str | None = None
    org_type: OrgType
    relationship: RelationshipToQH = "unknown"
    hq_city: str | None = None
    hq_state: str | None = None
    region: str | None = None
    size_label: str | None = None
    size_metric: str | None = None
    size_value: float | None = None
    description: str | None = None
    homepage_url: str | None = None
    metadata: dict = Field(default_factory=dict)
    created_at: datetime | None = None


class Contact(BaseModel):
    id: str
    organization_id: str | None = None
    name: str
    title: str | None = None
    role_category: str | None = None
    linkedin_url: str | None = None
    notes: str | None = None


class Initiative(BaseModel):
    id: str
    code: str | None = None
    name: str
    kind: InitiativeKind
    thesis: str | None = None
    stage: InitiativeStage
    confidence: Confidence
    velocity: Velocity
    primary_owner: str | None = None
    exec_sponsor: str | None = None
    fte_allocated: float | None = None
    spend_quarterly_usd: float | None = None
    target_revenue_year_one_usd: float | None = None
    target_design_partners: int | None = None
    current_design_partners: int | None = 0
    top_blocker: str | None = None
    next_milestone: str | None = None
    next_milestone_date: date | None = None
    metadata: dict = Field(default_factory=dict)


class Workstream(BaseModel):
    id: str
    initiative_id: str
    kind: WorkstreamKind
    status: str | None = None
    owner: str | None = None
    summary: str | None = None
    next_action: str | None = None
    next_action_due: date | None = None
    last_movement_at: datetime | None = None


class Signal(BaseModel):
    id: str
    signal_kind: SignalKind
    title: str
    summary: str | None = None
    body: str | None = None
    source_name: str | None = None
    source_url: str | None = None
    source_type: str | None = None
    primary_organization_id: str | None = None
    detected_at: datetime
    occurred_at: datetime | None = None
    is_seed: bool = False


class Implication(BaseModel):
    id: str
    signal_id: str
    initiative_id: str | None = None
    customer_org_id: str | None = None
    severity: SignalSeverity
    confidence_score: float | None = None
    headline: str
    reasoning: str
    recommended_action: str | None = None
    recommended_owner: str | None = None
    recommended_by_date: date | None = None
    rank_score: float | None = None
    status: str = "open"
    created_at: datetime | None = None


class SignalWithImplications(Signal):
    implications: list[Implication] = Field(default_factory=list)
    primary_organization: Organization | None = None


class AgentDef(BaseModel):
    id: str
    slug: str
    name: str
    role: str
    description: str | None = None
    model: str
    is_active: bool = True
    schedule_cron: str | None = None
    last_run_at: datetime | None = None
    last_run_status: str | None = None


class AgentRun(BaseModel):
    id: str
    agent_id: str
    trigger: str | None = None
    started_at: datetime
    completed_at: datetime | None = None
    status: str
    input_summary: str | None = None
    output_summary: str | None = None
    trace: list[dict] = Field(default_factory=list)
    signals_ingested: int = 0
    implications_generated: int = 0
    tokens_input: int = 0
    tokens_output: int = 0
    error_message: str | None = None
