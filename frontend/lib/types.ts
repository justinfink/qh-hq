// Mirror of backend schemas. Keep in sync with app/models/schemas.py.

export type OrgType =
  | "idn" | "amc" | "asc" | "specialty_msa" | "pharma" | "payer"
  | "ai_vendor" | "governance_competitor" | "cloud_provider"
  | "ehr_vendor" | "thought_leadership" | "regulator" | "investor"
  | "consultancy" | "other";

export type RelationshipToQH =
  | "customer" | "pilot" | "prospect" | "partner" | "competitor"
  | "investor" | "regulator_watch" | "ecosystem" | "unknown";

export type InitiativeKind =
  | "nbl" | "core_product" | "partnership" | "strategic_project" | "internal_op";

export type InitiativeStage =
  | "discovery" | "greenlight" | "pilot" | "early_revenue" | "scaling" | "paused";

export type WorkstreamKind = "product" | "gtm" | "partnerships" | "regulatory" | "finance";
export type Confidence = "high" | "medium" | "low";
export type Velocity = "accelerating" | "holding" | "slipping";
export type Trajectory = "improving" | "stable" | "deteriorating" | "volatile";
export type SignalSeverity = "critical" | "high" | "medium" | "low" | "fyi";
export type SignalKind =
  | "funding" | "product_launch" | "partnership" | "customer_win"
  | "leadership_change" | "regulatory" | "m_and_a" | "public_failure"
  | "conference_talk" | "hiring_signal" | "patent" | "thought_leadership" | "other";

export interface RelationshipDynamics {
  relationship_strength?: number;
  trajectory?: Trajectory;
  strategic_value?: "critical" | "high" | "medium" | "low";
  tailwinds?: string[];
  headwinds?: string[];
  qh_leverage?: string[];
  qh_exposure?: string[];
  watch_signals?: string[];
}

export interface Organization {
  id: string;
  name: string;
  short_name?: string | null;
  org_type: OrgType;
  relationship: RelationshipToQH;
  hq_city?: string | null;
  hq_state?: string | null;
  region?: string | null;
  size_label?: string | null;
  size_metric?: string | null;
  size_value?: number | null;
  description?: string | null;
  homepage_url?: string | null;
  metadata?: { dynamics?: RelationshipDynamics; [k: string]: unknown };
}

export interface Workstream {
  id: string;
  initiative_id: string;
  kind: WorkstreamKind;
  status?: string | null;
  owner?: string | null;
  summary?: string | null;
  next_action?: string | null;
  next_action_due?: string | null;
  last_movement_at?: string | null;
}

export interface Initiative {
  id: string;
  code?: string | null;
  name: string;
  kind: InitiativeKind;
  thesis?: string | null;
  stage: InitiativeStage;
  confidence: Confidence;
  velocity: Velocity;
  primary_owner?: string | null;
  exec_sponsor?: string | null;
  fte_allocated?: number | null;
  spend_quarterly_usd?: number | null;
  target_revenue_year_one_usd?: number | null;
  target_design_partners?: number | null;
  current_design_partners?: number | null;
  top_blocker?: string | null;
  next_milestone?: string | null;
  next_milestone_date?: string | null;
  workstreams?: Workstream[];
  recent_implications?: ImplicationLite[];
  metadata?: Record<string, unknown>;
}

export interface Signal {
  id: string;
  signal_kind: SignalKind;
  title: string;
  summary?: string | null;
  source_name?: string | null;
  source_url?: string | null;
  source_type?: string | null;
  primary_organization_id?: string | null;
  detected_at: string;
  occurred_at?: string | null;
  is_seed?: boolean;
}

export interface ImplicationLite {
  id: string;
  severity: SignalSeverity;
  headline: string;
  reasoning: string;
  recommended_action?: string | null;
  created_at?: string | null;
  signal?: Pick<Signal, "id" | "title" | "source_name" | "source_url" | "detected_at">;
}

export interface FeedItem {
  implication_id: string;
  severity: SignalSeverity;
  confidence_score?: number | null;
  headline: string;
  reasoning: string;
  recommended_action?: string | null;
  recommended_owner?: string | null;
  recommended_by_date?: string | null;
  created_at: string;
  signal: {
    id: string;
    title: string;
    summary?: string;
    source_name?: string;
    source_url?: string;
    signal_kind: SignalKind;
    detected_at?: string;
    occurred_at?: string;
  };
  primary_organization?: Organization | null;
  initiative?: Pick<Initiative, "id" | "code" | "name"> | null;
}

export interface AgentDef {
  slug: string;
  name: string;
  role: string;
  description: string;
  model: string;
  is_active: boolean;
  schedule_cron?: string | null;
  last_run_at?: string | null;
  last_run_status?: string | null;
}

export interface AgentRun {
  id: string;
  trigger?: string | null;
  started_at: string;
  completed_at?: string | null;
  status: string;
  signals_ingested: number;
  implications_generated: number;
  tokens_input: number;
  tokens_output: number;
  output_summary?: string | null;
  error_message?: string | null;
  agent: { slug: string; name: string; role: string; model: string };
}

export interface AgentTraceEvent {
  type: "agent_trace";
  run_id: string;
  agent_slug: string;
  ts: string;
  kind: string;
  label: string;
  detail: Record<string, unknown>;
}
