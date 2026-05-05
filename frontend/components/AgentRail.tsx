"use client";

import { useEffect, useState, useCallback } from "react";
import { api, API_BASE_URL } from "@/lib/api";
import type { AgentDef, AgentRun, AgentTraceEvent } from "@/lib/types";
import { timeAgo, cn } from "@/lib/format";

interface LiveTrace {
  ts: string;
  agent_slug: string;
  kind: string;
  label: string;
}

const TRACE_LIMIT = 30;

export default function AgentRail() {
  const [agents, setAgents] = useState<AgentDef[]>([]);
  const [runs, setRuns] = useState<AgentRun[]>([]);
  const [trace, setTrace] = useState<LiveTrace[]>([]);
  const [connected, setConnected] = useState(false);

  const refresh = useCallback(() => {
    api.agents().then((r) => setAgents(r.agents)).catch(() => {});
    api.runs(15).then((r) => setRuns(r.runs)).catch(() => {});
  }, []);

  useEffect(() => {
    refresh();
    const int = setInterval(refresh, 15_000);
    return () => clearInterval(int);
  }, [refresh]);

  // SSE subscription to live trace events.
  // Vercel serverless can't hold open connections, so we close on first
  // "info" message to avoid an infinite reconnect loop.
  useEffect(() => {
    let es: EventSource | null = null;
    let reconnectAttempts = 0;
    try {
      es = new EventSource(`${API_BASE_URL}/api/agents/stream`);
      es.onopen = () => setConnected(true);
      es.onerror = () => {
        setConnected(false);
        reconnectAttempts++;
        if (reconnectAttempts >= 2) {
          es?.close();  // Stop the EventSource auto-reconnect storm
          es = null;
        }
      };
      es.onmessage = (e) => {
        try {
          const data = JSON.parse(e.data);
          if (data.type === "info") {
            // Serverless mode acknowledgement — no live stream available
            es?.close();
            return;
          }
          if (data.type !== "agent_trace") return;
          setTrace((prev) => {
            const next = [{
              ts: data.ts,
              agent_slug: data.agent_slug,
              kind: data.kind,
              label: data.label,
            }, ...prev].slice(0, TRACE_LIMIT);
            return next;
          });
        } catch {/* ignore */}
      };
    } catch {/* SSE failed */}
    return () => { es?.close(); };
  }, []);

  const [running, setRunning] = useState<Record<string, "running" | "success" | "error" | undefined>>({});
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  const trigger = useCallback(async (slug: string) => {
    setRunning((r) => ({ ...r, [slug]: "running" }));
    setErrorMsg(null);
    try {
      await api.triggerAgent(slug);
      // Trace events should arrive via SSE; the run itself is async on the backend.
      // Refresh runs after a short delay to pick up the persisted result.
      setTimeout(() => {
        api.runs(15).then((r) => setRuns(r.runs)).catch(() => {});
        setRunning((r) => ({ ...r, [slug]: "success" }));
        setTimeout(() => setRunning((r) => ({ ...r, [slug]: undefined })), 2000);
      }, 4000);
    } catch (err) {
      setRunning((r) => ({ ...r, [slug]: "error" }));
      setErrorMsg(`Run failed: ${(err as Error).message}. Check ANTHROPIC_API_KEY in backend env.`);
      setTimeout(() => setRunning((r) => ({ ...r, [slug]: undefined })), 4000);
    }
  }, []);

  return (
    <div className="h-full flex flex-col">
      {/* Agents list */}
      <div className="bb">
        <div className="px-3 py-2 flex items-center justify-between">
          <span className="font-mono text-[10px] text-[var(--color-fg-3)] uppercase tracking-widest">
            Agents · {agents.length}
          </span>
          <span className={cn(
            "font-mono text-[10px] tabular",
            connected ? "text-[var(--color-accent)]" : "text-[var(--color-fg-5)]"
          )}>
            {connected ? "● stream live" : "○ stream off"}
          </span>
        </div>
        {agents.map((a) => {
          const state = running[a.slug];
          return (
          <div key={a.slug} className="px-3 py-2 bt border-[var(--color-line)] row-hover">
            <div className="flex items-center justify-between mb-1">
              <span className="text-[12px] text-[var(--color-fg)]">{a.name}</span>
              <button
                onClick={() => trigger(a.slug)}
                disabled={state === "running"}
                className={cn(
                  "font-mono text-[10px] cursor-pointer transition-colors disabled:cursor-wait",
                  state === "running" ? "text-[var(--color-fg-4)]" :
                  state === "error" ? "text-[#FF4B6E]" :
                  state === "success" ? "text-[var(--color-accent)]" :
                  "text-[var(--color-accent)] hover:text-[var(--color-fg)]"
                )}
                title="Trigger run"
              >
                {state === "running" ? "⏵ running…" :
                 state === "error" ? "✕ failed" :
                 state === "success" ? "✓ queued" : "▶ run"}
              </button>
            </div>
            <div className="text-[10px] font-mono text-[var(--color-fg-4)] mb-1">
              {a.role}
            </div>
            <div className="flex items-center gap-3 font-mono text-[10px] text-[var(--color-fg-5)] tabular " data-marker="agent-meta-row">
              <span>{a.model.split("-").slice(0, 3).join("-")}</span>
              <span>{a.last_run_at ? timeAgo(a.last_run_at) : "never run"}</span>
              {a.last_run_status && (
                <span className={cn(
                  a.last_run_status === "success" ? "text-[var(--color-accent)]" :
                  a.last_run_status === "failed" ? "text-[#FF4B6E]" : "text-[var(--color-fg-4)]"
                )}>
                  {a.last_run_status}
                </span>
              )}
            </div>
          </div>
          );
        })}
        {errorMsg && (
          <div className="px-3 py-2 border-t border-[#FF4B6E]/30 bg-[#FF4B6E]/10">
            <p className="font-mono text-[10px] text-[#FF4B6E] leading-relaxed">{errorMsg}</p>
          </div>
        )}
      </div>

      {/* Live trace */}
      <div className="flex-1 overflow-y-auto bb">
        <div className="px-3 py-2 sticky top-0 bg-[var(--color-bg)] bb z-10 flex items-center justify-between">
          <span className="font-mono text-[10px] text-[var(--color-fg-3)] uppercase tracking-widest">
            Live trace
          </span>
          {trace.length > 0 && (
            <button
              onClick={() => setTrace([])}
              className="font-mono text-[10px] text-[var(--color-fg-5)] hover:text-[var(--color-fg-3)] cursor-pointer"
            >
              clear
            </button>
          )}
        </div>
        {trace.length === 0 ? (
          <div className="px-3 py-6 text-[var(--color-fg-5)] text-[10px] font-mono leading-relaxed">
            Trigger an agent above to watch the reasoning trace stream here in real time.
          </div>
        ) : (
          <div className="px-3 py-1 font-mono text-[10px]">
            {trace.map((t, i) => (
              <div key={i} className="py-1 leading-snug">
                <span className="text-[var(--color-fg-5)] tabular">
                  {new Date(t.ts).toLocaleTimeString("en-US", { hour12: false })}
                </span>{" "}
                <span className={cn(
                  "uppercase",
                  t.kind === "error" ? "text-[#FF4B6E]" :
                  t.kind === "complete" ? "text-[var(--color-accent)]" :
                  t.kind === "decision" ? "text-[#FFA84A]" :
                  "text-[var(--color-fg-4)]"
                )}>
                  {t.kind}
                </span>{" "}
                <span className="text-[var(--color-fg-2)]">{t.label}</span>
                <div className="text-[var(--color-fg-5)] pl-12">{t.agent_slug}</div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Recent runs */}
      <div className="overflow-y-auto" style={{ maxHeight: "280px" }}>
        <div className="px-3 py-2 sticky top-0 bg-[var(--color-bg)] bb z-10">
          <span className="font-mono text-[10px] text-[var(--color-fg-3)] uppercase tracking-widest">
            Recent runs
          </span>
        </div>
        {runs.length === 0 ? (
          <div className="px-3 py-4 text-[var(--color-fg-5)] text-[10px] font-mono">
            No runs yet.
          </div>
        ) : runs.map((r) => (
          <div key={r.id} className="px-3 py-2 bb row-hover">
            <div className="flex items-center justify-between text-[11px]">
              <span className="text-[var(--color-fg-2)]">{r.agent.name}</span>
              <span className={cn(
                "font-mono text-[10px] tabular uppercase",
                r.status === "success" ? "text-[var(--color-accent)]" :
                r.status === "failed" ? "text-[#FF4B6E]" : "text-[var(--color-fg-4)]"
              )}>
                {r.status}
              </span>
            </div>
            <div className="mt-1 font-mono text-[10px] text-[var(--color-fg-4)] tabular flex items-center gap-3">
              <span>{timeAgo(r.started_at)}</span>
              {r.signals_ingested > 0 && <span>+{r.signals_ingested} sig</span>}
              {r.implications_generated > 0 && <span>+{r.implications_generated} imp</span>}
              {r.tokens_input > 0 && <span>{(r.tokens_input + r.tokens_output).toLocaleString()} tok</span>}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
