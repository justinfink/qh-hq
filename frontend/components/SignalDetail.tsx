"use client";

import type { FeedItem } from "@/lib/types";
import { SEVERITY_COLOR, timeAgo, fmtDate, cn } from "@/lib/format";
import { ExternalLink } from "lucide-react";

export default function SignalDetail({ item }: { item: FeedItem | null }) {
  if (!item) {
    return (
      <div className="h-full flex items-center justify-center px-6 py-12">
        <div className="text-center max-w-md">
          <div className="font-mono text-[10px] text-[var(--color-fg-5)] uppercase tracking-widest mb-2">
            No signal selected
          </div>
          <div className="text-[12px] text-[var(--color-fg-4)] leading-relaxed">
            Pick a signal from the feed to see the agent&rsquo;s reasoning, the QH-specific
            implication, the recommended action, and the relationship dynamics in play.
          </div>
        </div>
      </div>
    );
  }

  const sc = SEVERITY_COLOR[item.severity];

  return (
    <div className="h-full overflow-y-auto">
      <div className="bb px-4 py-2 flex items-center justify-between">
        <span className="font-mono text-[10px] text-[var(--color-fg-3)] uppercase tracking-widest">
          Signal Detail
        </span>
        <span className="font-mono text-[10px] text-[var(--color-fg-5)] tabular">
          {item.signal.id.slice(0, 8)}
        </span>
      </div>

      <div className="px-4 py-4">
        {/* Severity strip */}
        <div className={cn("inline-block font-mono text-[10px] uppercase tracking-widest px-2 py-0.5 border", sc.fg, sc.bd, sc.bg)}>
          {item.severity} · {item.signal.signal_kind.replace(/_/g, " ")}
        </div>

        {/* Headline */}
        <h2 className="text-display text-[24px] leading-tight mt-3 text-[var(--color-fg)]">
          {item.headline}
        </h2>

        {/* Meta row */}
        <div className="mt-3 flex flex-wrap items-center gap-x-4 gap-y-1 font-mono text-[10px] text-[var(--color-fg-4)] tabular">
          {item.primary_organization && (
            <span>
              <span className="text-[var(--color-fg-5)]">org · </span>
              <span className="text-[var(--color-fg-2)]">
                {item.primary_organization.name}
              </span>
            </span>
          )}
          {item.initiative && (
            <span>
              <span className="text-[var(--color-fg-5)]">initiative · </span>
              <span className="text-[var(--color-accent)]">
                {item.initiative.code} {item.initiative.name}
              </span>
            </span>
          )}
          <span>
            <span className="text-[var(--color-fg-5)]">detected · </span>
            <span>{timeAgo(item.signal.detected_at)}</span>
          </span>
          {item.confidence_score != null && (
            <span>
              <span className="text-[var(--color-fg-5)]">conf · </span>
              <span>{(item.confidence_score * 100).toFixed(0)}%</span>
            </span>
          )}
        </div>

        {/* Reasoning */}
        <section className="mt-6">
          <div className="font-mono text-[10px] text-[var(--color-fg-3)] uppercase tracking-widest mb-2">
            Agent reasoning
          </div>
          <p className="text-[13px] text-[var(--color-fg-2)] leading-relaxed whitespace-pre-wrap">
            {item.reasoning}
          </p>
        </section>

        {/* Recommended action */}
        {item.recommended_action && (
          <section className="mt-6 border border-[var(--color-line)] bg-[var(--color-bg-1)] p-3">
            <div className="font-mono text-[10px] text-[var(--color-accent)] uppercase tracking-widest mb-2">
              Recommended action
            </div>
            <p className="text-[13px] text-[var(--color-fg)] leading-relaxed">
              {item.recommended_action}
            </p>
            <div className="mt-2 flex items-center gap-3 font-mono text-[10px] text-[var(--color-fg-4)] tabular">
              {item.recommended_owner && (
                <span>
                  <span className="text-[var(--color-fg-5)]">owner · </span>
                  {item.recommended_owner}
                </span>
              )}
              {item.recommended_by_date && (
                <span>
                  <span className="text-[var(--color-fg-5)]">by · </span>
                  {fmtDate(item.recommended_by_date)}
                </span>
              )}
            </div>
          </section>
        )}

        {/* Source */}
        <section className="mt-6 bt pt-4">
          <div className="font-mono text-[10px] text-[var(--color-fg-3)] uppercase tracking-widest mb-2">
            Source
          </div>
          <div className="text-[12px] text-[var(--color-fg-2)] leading-snug">
            {item.signal.title}
          </div>
          <div className="mt-2 flex items-center gap-3 font-mono text-[10px] text-[var(--color-fg-4)] tabular">
            <span>{item.signal.source_name}</span>
            {item.signal.source_url && (
              <a
                href={item.signal.source_url}
                target="_blank"
                rel="noreferrer"
                className="text-[var(--color-accent)] hover:underline inline-flex items-center gap-1"
              >
                open <ExternalLink size={10} />
              </a>
            )}
          </div>
          {item.signal.summary && (
            <p className="mt-3 text-[12px] text-[var(--color-fg-3)] leading-relaxed">
              {item.signal.summary}
            </p>
          )}
        </section>
      </div>
    </div>
  );
}
