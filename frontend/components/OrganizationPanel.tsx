"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import type { Organization, Trajectory } from "@/lib/types";
import { TRAJECTORY_COLOR, TRAJECTORY_GLYPH, relStrengthBar, timeAgo, cn } from "@/lib/format";
import { ExternalLink } from "lucide-react";

interface OrgFull extends Organization {
  contacts?: Array<{ id: string; name: string; title?: string; role_category?: string; notes?: string }>;
  deployments?: Array<unknown>;
  recent_implications?: Array<{ id: string; severity: string; headline: string; created_at: string }>;
}

export default function OrganizationPanel({ orgId }: { orgId: string | null }) {
  const [org, setOrg] = useState<OrgFull | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!orgId) { setOrg(null); return; }
    setLoading(true);
    api.organization(orgId)
      .then((data) => setOrg(data as OrgFull))
      .catch(() => setOrg(null))
      .finally(() => setLoading(false));
  }, [orgId]);

  if (!orgId) {
    return (
      <div className="h-full flex items-center justify-center px-6">
        <div className="text-center max-w-sm">
          <div className="font-mono text-[10px] text-[var(--color-fg-5)] uppercase tracking-widest mb-2">
            No organization selected
          </div>
          <div className="text-[12px] text-[var(--color-fg-4)] leading-relaxed">
            Pick from the relationship map to see headwinds, tailwinds, and the live signal
            stream tied to that org.
          </div>
        </div>
      </div>
    );
  }
  if (loading || !org) {
    return <div className="px-4 py-6 text-[var(--color-fg-5)] text-[11px] font-mono">Loading…</div>;
  }

  const dyn = org.metadata?.dynamics;
  const traj = (dyn?.trajectory ?? "stable") as Trajectory;

  return (
    <div className="h-full overflow-y-auto">
      <div className="bb px-4 py-2 flex items-center justify-between">
        <span className="font-mono text-[10px] text-[var(--color-fg-3)] uppercase tracking-widest">
          Organization
        </span>
        <span className="font-mono text-[10px] text-[var(--color-fg-5)] uppercase tracking-wider">
          {org.relationship?.replace(/_/g, " ")}
        </span>
      </div>

      <div className="px-4 py-4">
        <h2 className="text-display text-[24px] leading-tight">{org.name}</h2>
        <div className="mt-1 font-mono text-[10px] text-[var(--color-fg-4)] tabular">
          {org.size_label}
          {org.hq_city && org.hq_state && ` · ${org.hq_city}, ${org.hq_state}`}
        </div>
        {org.homepage_url && (
          <a
            href={org.homepage_url}
            target="_blank"
            rel="noreferrer"
            className="mt-1 inline-flex items-center gap-1 font-mono text-[10px] text-[var(--color-accent)] hover:underline"
          >
            {org.homepage_url.replace(/^https?:\/\//, "")}
            <ExternalLink size={10} />
          </a>
        )}

        {org.description && (
          <p className="mt-4 text-[12px] text-[var(--color-fg-2)] leading-relaxed">
            {org.description}
          </p>
        )}

        {/* Dynamics block */}
        {dyn && (
          <section className="mt-5 border border-[var(--color-line)] bg-[var(--color-bg-1)]">
            <div className="px-3 py-2 bb flex items-center justify-between">
              <span className="font-mono text-[10px] text-[var(--color-fg-3)] uppercase tracking-widest">
                Relationship dynamics
              </span>
              <span className={cn("font-mono text-[10px]", TRAJECTORY_COLOR[traj])}>
                {TRAJECTORY_GLYPH[traj]} {traj}
              </span>
            </div>

            <div className="px-3 py-2 grid grid-cols-2 gap-3 font-mono text-[10px]">
              <div>
                <div className="text-[var(--color-fg-5)] uppercase tracking-wider mb-1">Strength</div>
                <div className="tabular">
                  <span className={cn(
                    (dyn.relationship_strength ?? 0) >= 7 ? "text-[var(--color-accent)]" :
                    (dyn.relationship_strength ?? 0) >= 4 ? "text-[var(--color-fg-3)]" : "text-[#FFA84A]"
                  )}>
                    {relStrengthBar(dyn.relationship_strength)}
                  </span>{" "}
                  <span className="text-[var(--color-fg-2)]">{dyn.relationship_strength ?? "—"}/10</span>
                </div>
              </div>
              <div>
                <div className="text-[var(--color-fg-5)] uppercase tracking-wider mb-1">Strategic value</div>
                <div className="text-[var(--color-fg-2)] uppercase">{dyn.strategic_value || "—"}</div>
              </div>
            </div>

            {dyn.tailwinds && dyn.tailwinds.length > 0 && (
              <div className="px-3 py-2 bt">
                <div className="font-mono text-[10px] text-[var(--color-accent)] uppercase tracking-wider mb-1.5">
                  ↗ Tailwinds
                </div>
                <ul className="space-y-1">
                  {dyn.tailwinds.map((t, i) => (
                    <li key={i} className="text-[12px] text-[var(--color-fg-2)] leading-snug pl-2 border-l border-[var(--color-accent-dim)]">
                      {t}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {dyn.headwinds && dyn.headwinds.length > 0 && (
              <div className="px-3 py-2 bt">
                <div className="font-mono text-[10px] text-[#FF4B6E] uppercase tracking-wider mb-1.5">
                  ↘ Headwinds
                </div>
                <ul className="space-y-1">
                  {dyn.headwinds.map((t, i) => (
                    <li key={i} className="text-[12px] text-[var(--color-fg-2)] leading-snug pl-2 border-l border-[#FF4B6E]/40">
                      {t}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {dyn.qh_leverage && dyn.qh_leverage.length > 0 && (
              <div className="px-3 py-2 bt">
                <div className="font-mono text-[10px] text-[var(--color-fg-3)] uppercase tracking-wider mb-1.5">
                  QH leverage
                </div>
                <ul className="space-y-1">
                  {dyn.qh_leverage.map((t, i) => (
                    <li key={i} className="text-[12px] text-[var(--color-fg-3)] leading-snug pl-2">· {t}</li>
                  ))}
                </ul>
              </div>
            )}

            {dyn.qh_exposure && dyn.qh_exposure.length > 0 && (
              <div className="px-3 py-2 bt">
                <div className="font-mono text-[10px] text-[var(--color-fg-3)] uppercase tracking-wider mb-1.5">
                  QH exposure
                </div>
                <ul className="space-y-1">
                  {dyn.qh_exposure.map((t, i) => (
                    <li key={i} className="text-[12px] text-[var(--color-fg-3)] leading-snug pl-2">· {t}</li>
                  ))}
                </ul>
              </div>
            )}

            {dyn.watch_signals && dyn.watch_signals.length > 0 && (
              <div className="px-3 py-2 bt">
                <div className="font-mono text-[10px] text-[var(--color-fg-3)] uppercase tracking-wider mb-1.5">
                  Watch signals
                </div>
                <ul className="space-y-1">
                  {dyn.watch_signals.map((t, i) => (
                    <li key={i} className="text-[12px] text-[var(--color-fg-4)] leading-snug pl-2 italic">· {t}</li>
                  ))}
                </ul>
              </div>
            )}
          </section>
        )}

        {/* Contacts */}
        {org.contacts && org.contacts.length > 0 && (
          <section className="mt-5">
            <div className="font-mono text-[10px] text-[var(--color-fg-3)] uppercase tracking-widest mb-2">
              Named contacts · {org.contacts.length}
            </div>
            <div className="space-y-2">
              {org.contacts.map((c) => (
                <div key={c.id} className="border border-[var(--color-line)] px-3 py-2">
                  <div className="text-[12px] text-[var(--color-fg)]">{c.name}</div>
                  <div className="font-mono text-[10px] text-[var(--color-fg-4)] tabular mt-0.5">
                    {c.title}
                  </div>
                  {c.notes && (
                    <div className="text-[11px] text-[var(--color-fg-3)] mt-1.5 leading-snug">{c.notes}</div>
                  )}
                </div>
              ))}
            </div>
          </section>
        )}

        {/* Recent implications */}
        {org.recent_implications && org.recent_implications.length > 0 && (
          <section className="mt-5 bt pt-4">
            <div className="font-mono text-[10px] text-[var(--color-fg-3)] uppercase tracking-widest mb-2">
              Recent agent-surfaced implications
            </div>
            <div className="space-y-2">
              {org.recent_implications.slice(0, 8).map((imp) => (
                <div key={imp.id} className="text-[12px] text-[var(--color-fg-2)] leading-snug">
                  <span className="font-mono text-[10px] text-[var(--color-fg-4)] uppercase mr-2 tabular">
                    {imp.severity}
                  </span>
                  {imp.headline}
                  <div className="font-mono text-[10px] text-[var(--color-fg-5)] tabular mt-0.5">
                    {timeAgo(imp.created_at)}
                  </div>
                </div>
              ))}
            </div>
          </section>
        )}
      </div>
    </div>
  );
}
