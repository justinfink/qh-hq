import type {
  Organization, Initiative, FeedItem, AgentDef, AgentRun, Signal,
} from "./types";

const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

async function get<T>(path: string): Promise<T> {
  const res = await fetch(`${API}${path}`, { cache: "no-store" });
  if (!res.ok) throw new Error(`${res.status} ${res.statusText} at ${path}`);
  return res.json();
}

async function post<T>(path: string, body?: unknown): Promise<T> {
  const res = await fetch(`${API}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: body ? JSON.stringify(body) : undefined,
    cache: "no-store",
  });
  if (!res.ok) throw new Error(`${res.status} ${res.statusText} at ${path}`);
  return res.json();
}

export const api = {
  feed: () => get<{ items: FeedItem[]; count: number }>("/api/signals/feed"),
  signals: (params: { severity?: string; days?: number; limit?: number } = {}) => {
    const q = new URLSearchParams();
    if (params.severity) q.set("severity", params.severity);
    if (params.days) q.set("days", String(params.days));
    if (params.limit) q.set("limit", String(params.limit));
    const qs = q.toString();
    return get<{ signals: unknown[] }>(`/api/signals${qs ? `?${qs}` : ""}`);
  },
  signal: (id: string) => get<Signal & Record<string, unknown>>(`/api/signals/${id}`),
  initiatives: () => get<{ initiatives: Initiative[]; count: number }>("/api/initiatives"),
  initiative: (id: string) => get<Initiative>(`/api/initiatives/${id}`),
  organizations: (params: { org_type?: string; relationship?: string } = {}) => {
    const q = new URLSearchParams();
    if (params.org_type) q.set("org_type", params.org_type);
    if (params.relationship) q.set("relationship", params.relationship);
    const qs = q.toString();
    return get<{ organizations: Organization[] }>(`/api/customers${qs ? `?${qs}` : ""}`);
  },
  organization: (id: string) => get<Organization & Record<string, unknown>>(`/api/customers/${id}`),
  agents: () => get<{ agents: AgentDef[] }>("/api/agents"),
  runs: (limit = 25) => get<{ runs: AgentRun[] }>(`/api/agents/runs?limit=${limit}`),
  triggerAgent: (slug: string) => post(`/api/agents/${slug}/run`),
  search: (q: string, k = 8) => post<{
    query: string;
    signals: unknown[];
    initiatives: unknown[];
    organizations: unknown[];
    documents: unknown[];
  }>("/api/query", { q, k }),
};

export const API_BASE_URL = API;
