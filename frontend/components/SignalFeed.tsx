"use client";

import { useEffect, useState, useCallback } from "react";
import { api } from "@/lib/api";
import type { FeedItem } from "@/lib/types";
import { SEVERITY_COLOR, timeAgo, cn } from "@/lib/format";

const SEVERITY_ORDER: Array<FeedItem["severity"]> = ["critical", "high", "medium", "low", "fyi"];

export default function SignalFeed({
  selectedId,
  onSelect,
  filter,
  onFilterChange,
}: {
  selectedId: string | null;
  onSelect: (item: FeedItem) => void;
  filter: FeedItem["severity"] | "all";
  onFilterChange: (f: FeedItem["severity"] | "all") => void;
}) {
  const [items, setItems] = useState<FeedItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [refreshTick, setRefreshTick] = useState(0);

  const refresh = useCallback(() => {
    api.feed()
      .then((r) => setItems(r.items))
      .catch(() => {/* offline */})
      .finally(() => setLoading(false));
  }, []);

  useEffect(() => {
    refresh();
    const int = setInterval(refresh, 30_000);
    return () => clearInterval(int);
  }, [refresh, refreshTick]);

  const filtered = filter === "all" ? items : items.filter((i) => i.severity === filter);

  const counts: Record<string, number> = { all: items.length };
  for (const s of SEVERITY_ORDER) counts[s] = items.filter((i) => i.severity === s).length;

  return (
    <div className="h-full flex flex-col">
      <div className="bb px-4 py-2 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <span className="font-mono text-[10px] text-[var(--color-fg-3)] uppercase tracking-widest">
            Signal Feed
          </span>
          <span className="font-mono text-[10px] text-[var(--color-fg-5)]">
            agent-surfaced · ranked by QH-implication severity
          </span>
        </div>
        <div className="flex items-center gap-1 font-mono text-[10px]">
          {(["all", ...SEVERITY_ORDER] as const).map((s) => (
            <button
              key={s}
              onClick={() => onFilterChange(s)}
              className={cn(
                "px-2 py-0.5 cursor-pointer uppercase tracking-wider",
                filter === s ? "text-[var(--color-fg)] bg-[var(--color-bg-2)]" : "text-[var(--color-fg-4)] hover:text-[var(--color-fg-2)]"
              )}
            >
              {s} <span className="tabular text-[var(--color-fg-5)]">{counts[s] ?? 0}</span>
            </button>
          ))}
          <button
            onClick={() => setRefreshTick((t) => t + 1)}
            className="ml-2 px-2 py-0.5 text-[var(--color-fg-4)] hover:text-[var(--color-accent)] cursor-pointer"
          >
            ↻
          </button>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto">
        {loading && (
          <div className="px-4 py-6 text-[var(--color-fg-5)] text-[11px] font-mono">
            Connecting to backend… ensure FastAPI is running on :8000
          </div>
        )}
        {!loading && filtered.length === 0 && (
          <div className="px-4 py-6 text-[var(--color-fg-5)] text-[11px] font-mono">
            No signals at this severity. Run news_scout + implication_mapper to ingest.
          </div>
        )}
        {filtered.map((item) => {
          const sc = SEVERITY_COLOR[item.severity];
          const isSel = item.implication_id === selectedId;
          return (
            <button
              key={item.implication_id}
              onClick={() => onSelect(item)}
              className={cn(
                "block w-full text-left px-4 py-3 bb row-hover cursor-pointer",
                isSel && "bg-[var(--color-bg-2)]"
              )}
            >
              <div className="flex items-start gap-3">
                <div className={cn("font-mono text-[9px] uppercase tracking-widest tabular shrink-0 w-16 pt-0.5", sc.fg)}>
                  {item.severity}
                </div>
                <div className="flex-1 min-w-0">
                  <div className="text-[13px] text-[var(--color-fg)] leading-snug pr-4">
                    {item.headline}
                  </div>
                  <div className="mt-1.5 flex items-center gap-3 font-mono text-[10px] text-[var(--color-fg-4)] tabular">
                    <span>{item.signal.signal_kind.replace(/_/g, " ")}</span>
                    {item.primary_organization && (
                      <span className="text-[var(--color-fg-3)]">
                        {item.primary_organization.short_name || item.primary_organization.name}
                      </span>
                    )}
                    {item.initiative && (
                      <span className="text-[var(--color-accent)]">
                        → {item.initiative.code}
                      </span>
                    )}
                    <span className="ml-auto">{timeAgo(item.signal.detected_at || item.created_at)}</span>
                  </div>
                </div>
              </div>
            </button>
          );
        })}
      </div>
    </div>
  );
}
