"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import type { Initiative } from "@/lib/types";
import {
  STAGE_LABEL, VELOCITY_GLYPH, VELOCITY_COLOR, CONFIDENCE_COLOR,
  fmtUSDk, fmtDate, cn,
} from "@/lib/format";

export default function InitiativePanel({ initiativeId }: { initiativeId: string | null }) {
  const [init, setInit] = useState<Initiative | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!initiativeId) { setInit(null); return; }
    setLoading(true);
    api.initiative(initiativeId)
      .then((data) => setInit(data))
      .catch(() => setInit(null))
      .finally(() => setLoading(false));
  }, [initiativeId]);

  if (!initiativeId) {
    return (
      <div className="h-full flex items-center justify-center px-6">
        <div className="text-center max-w-sm">
          <div className="font-mono text-[10px] text-[var(--color-fg-5)] uppercase tracking-widest mb-2">
            No initiative selected
          </div>
          <div className="text-[12px] text-[var(--color-fg-4)] leading-relaxed">
            Pick an initiative from the left rail to see workstreams, blockers, and recent
            agent-surfaced implications tied to it.
          </div>
        </div>
      </div>
    );
  }

  if (loading || !init) {
    return <div className="px-4 py-6 text-[var(--color-fg-5)] text-[11px] font-mono">Loading…</div>;
  }

  return (
    <div className="h-full overflow-y-auto">
      <div className="bb px-4 py-2 flex items-center justify-between">
        <span className="font-mono text-[10px] text-[var(--color-fg-3)] uppercase tracking-widest">
          Initiative · {init.code}
        </span>
      </div>

      <div className="px-4 py-4">
        <h2 className="text-display text-[22px] leading-tight">{init.name}</h2>

        <div className="mt-2 flex flex-wrap items-center gap-3 font-mono text-[10px] tabular">
          <span className="text-[var(--color-fg-4)]">{STAGE_LABEL[init.stage]}</span>
          <span className={cn(VELOCITY_COLOR[init.velocity])}>{VELOCITY_GLYPH[init.velocity]} {init.velocity}</span>
          <span className={cn(CONFIDENCE_COLOR[init.confidence])}>{init.confidence} conf</span>
          {init.fte_allocated && <span className="text-[var(--color-fg-4)]">{init.fte_allocated.toFixed(1)} FTE</span>}
          {init.spend_quarterly_usd && <span className="text-[var(--color-fg-4)]">{fmtUSDk(init.spend_quarterly_usd)}/qtr</span>}
        </div>

        {init.thesis && (
          <p className="mt-4 text-[13px] text-[var(--color-fg-2)] leading-relaxed">
            {init.thesis}
          </p>
        )}

        {/* Owner / sponsor */}
        <div className="mt-4 grid grid-cols-2 gap-4 font-mono text-[10px]">
          <div>
            <div className="text-[var(--color-fg-5)] uppercase tracking-wider mb-1">Owner</div>
            <div className="text-[var(--color-fg-2)]">{init.primary_owner || "—"}</div>
          </div>
          <div>
            <div className="text-[var(--color-fg-5)] uppercase tracking-wider mb-1">Exec sponsor</div>
            <div className="text-[var(--color-fg-2)]">{init.exec_sponsor || "—"}</div>
          </div>
        </div>

        {/* Blocker */}
        {init.top_blocker && (
          <div className="mt-4 border-l-2 border-[#FFA84A] pl-3">
            <div className="font-mono text-[10px] text-[#FFA84A] uppercase tracking-wider mb-1">
              Top blocker
            </div>
            <p className="text-[12px] text-[var(--color-fg-2)] leading-relaxed">{init.top_blocker}</p>
          </div>
        )}

        {/* Next milestone */}
        {init.next_milestone && (
          <div className="mt-4 border-l-2 border-[var(--color-accent)] pl-3">
            <div className="font-mono text-[10px] text-[var(--color-accent)] uppercase tracking-wider mb-1">
              Next milestone · {fmtDate(init.next_milestone_date)}
            </div>
            <p className="text-[12px] text-[var(--color-fg-2)] leading-relaxed">{init.next_milestone}</p>
          </div>
        )}

        {/* Workstreams */}
        {init.workstreams && init.workstreams.length > 0 && (
          <section className="mt-6">
            <div className="font-mono text-[10px] text-[var(--color-fg-3)] uppercase tracking-widest mb-2">
              Workstreams
            </div>
            <div className="space-y-3">
              {init.workstreams.map((ws) => (
                <div key={ws.id} className="border border-[var(--color-line)] bg-[var(--color-bg-1)] p-3">
                  <div className="flex items-center justify-between font-mono text-[10px] mb-1">
                    <span className="text-[var(--color-accent)] uppercase tracking-wider">{ws.kind}</span>
                    <span className="text-[var(--color-fg-5)] tabular">
                      {ws.owner} {ws.next_action_due ? `· due ${fmtDate(ws.next_action_due)}` : ""}
                    </span>
                  </div>
                  {ws.status && <p className="text-[12px] text-[var(--color-fg-2)] leading-snug">{ws.status}</p>}
                  {ws.next_action && (
                    <p className="text-[11px] text-[var(--color-fg-4)] mt-1 italic">
                      next · {ws.next_action}
                    </p>
                  )}
                </div>
              ))}
            </div>
          </section>
        )}

        {/* Recent implications */}
        {init.recent_implications && init.recent_implications.length > 0 && (
          <section className="mt-6 bt pt-4">
            <div className="font-mono text-[10px] text-[var(--color-fg-3)] uppercase tracking-widest mb-2">
              Agent-surfaced implications
            </div>
            <div className="space-y-2">
              {init.recent_implications.slice(0, 5).map((imp) => (
                <div key={imp.id} className="text-[12px] text-[var(--color-fg-2)] leading-snug">
                  <span className="font-mono text-[10px] text-[var(--color-fg-4)] uppercase mr-2 tabular">
                    {imp.severity}
                  </span>
                  {imp.headline}
                </div>
              ))}
            </div>
          </section>
        )}
      </div>
    </div>
  );
}
