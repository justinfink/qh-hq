"use client";

import { useEffect, useMemo, useState, useCallback } from "react";
import { api } from "@/lib/api";
import type { FeedItem, Initiative, Organization } from "@/lib/types";
import { SEVERITY_COLOR, timeAgo, cn } from "@/lib/format";

const SEVERITY_ORDER: Array<FeedItem["severity"]> = ["critical", "high", "medium", "low", "fyi"];
type SortMode = "severity" | "newest";
const SEV_RANK: Record<FeedItem["severity"], number> = {
  critical: 0, high: 1, medium: 2, low: 3, fyi: 4,
};

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
  const [initiatives, setInitiatives] = useState<Initiative[]>([]);
  const [orgs, setOrgs] = useState<Organization[]>([]);
  const [loading, setLoading] = useState(true);
  const [refreshTick, setRefreshTick] = useState(0);

  const [sortMode, setSortMode] = useState<SortMode>("severity");
  const [initiativeFilter, setInitiativeFilter] = useState<string>("all");
  const [orgFilter, setOrgFilter] = useState<string>("all");

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

  // Load filter dropdown sources once
  useEffect(() => {
    api.initiatives().then((r) => setInitiatives(r.initiatives)).catch(() => {});
    api.organizations().then((r) => setOrgs(r.organizations)).catch(() => {});
  }, []);

  // Apply filters then sort
  const filtered = useMemo(() => {
    let out = items;
    if (filter !== "all") out = out.filter((i) => i.severity === filter);
    if (initiativeFilter !== "all") out = out.filter((i) => i.initiative?.id === initiativeFilter);
    if (orgFilter !== "all") out = out.filter((i) => i.primary_organization?.id === orgFilter);

    if (sortMode === "newest") {
      out = [...out].sort((a, b) => (b.created_at || "").localeCompare(a.created_at || ""));
    } else {
      out = [...out].sort((a, b) => {
        const sevDiff = SEV_RANK[a.severity] - SEV_RANK[b.severity];
        if (sevDiff !== 0) return sevDiff;
        return (b.created_at || "").localeCompare(a.created_at || "");
      });
    }
    return out;
  }, [items, filter, initiativeFilter, orgFilter, sortMode]);

  const counts: Record<string, number> = { all: items.length };
  for (const s of SEVERITY_ORDER) counts[s] = items.filter((i) => i.severity === s).length;

  // Initiatives that actually have items in the current feed (severity filter applied)
  const visibleInitiativeIds = useMemo(() => {
    const base = filter === "all" ? items : items.filter((i) => i.severity === filter);
    return new Set(base.map((i) => i.initiative?.id).filter(Boolean) as string[]);
  }, [items, filter]);
  const visibleOrgIds = useMemo(() => {
    const base = filter === "all" ? items : items.filter((i) => i.severity === filter);
    return new Set(base.map((i) => i.primary_organization?.id).filter(Boolean) as string[]);
  }, [items, filter]);

  const selectClass =
    "bg-[var(--color-bg-1)] border border-[var(--color-line)] text-[var(--color-fg-2)] " +
    "font-mono text-[10px] px-1.5 py-0.5 cursor-pointer uppercase tracking-wider focus:outline-none " +
    "focus:border-[var(--color-accent)]";

  return (
    <div className="h-full flex flex-col">
      {/* Top row: title + sort + dropdowns + refresh */}
      <div className="bb px-4 py-2 flex items-center justify-between gap-3">
        <div className="flex items-center gap-3 min-w-0">
          <span className="font-mono text-[10px] text-[var(--color-fg-3)] uppercase tracking-widest shrink-0">
            Signal Feed
          </span>
          <span className="font-mono text-[10px] text-[var(--color-fg-5)] truncate">
            agent-surfaced · {sortMode === "severity" ? "ranked by severity, then recency" : "newest first"}
          </span>
        </div>
        <div className="flex items-center gap-2 font-mono text-[10px] shrink-0">
          {/* Sort toggle */}
          <div className="flex items-center bl br border-[var(--color-line)] overflow-hidden">
            <button
              onClick={() => setSortMode("severity")}
              className={cn(
                "px-2 py-0.5 cursor-pointer uppercase tracking-wider",
                sortMode === "severity"
                  ? "text-[var(--color-fg)] bg-[var(--color-bg-2)]"
                  : "text-[var(--color-fg-4)] hover:text-[var(--color-fg-2)]"
              )}
            >
              severity
            </button>
            <button
              onClick={() => setSortMode("newest")}
              className={cn(
                "px-2 py-0.5 cursor-pointer uppercase tracking-wider bl border-[var(--color-line)]",
                sortMode === "newest"
                  ? "text-[var(--color-fg)] bg-[var(--color-bg-2)]"
                  : "text-[var(--color-fg-4)] hover:text-[var(--color-fg-2)]"
              )}
            >
              newest
            </button>
          </div>

          {/* Initiative filter */}
          <select
            value={initiativeFilter}
            onChange={(e) => setInitiativeFilter(e.target.value)}
            className={selectClass}
            title="Filter by initiative"
          >
            <option value="all">init: all</option>
            {initiatives
              .filter((i) => visibleInitiativeIds.has(i.id))
              .map((i) => (
                <option key={i.id} value={i.id}>
                  {i.code || i.name}
                </option>
              ))}
          </select>

          {/* Org filter */}
          <select
            value={orgFilter}
            onChange={(e) => setOrgFilter(e.target.value)}
            className={selectClass}
            title="Filter by organization"
          >
            <option value="all">org: all</option>
            {orgs
              .filter((o) => visibleOrgIds.has(o.id))
              .map((o) => (
                <option key={o.id} value={o.id}>
                  {o.short_name || o.name}
                </option>
              ))}
          </select>

          <button
            onClick={() => setRefreshTick((t) => t + 1)}
            className="px-2 py-0.5 text-[var(--color-fg-4)] hover:text-[var(--color-accent)] cursor-pointer"
            title="Refresh"
          >
            ↻
          </button>
        </div>
      </div>

      {/* Severity row */}
      <div className="bb px-4 py-1.5 flex items-center gap-1 font-mono text-[10px]">
        {(["all", ...SEVERITY_ORDER] as const).map((s) => (
          <button
            key={s}
            onClick={() => onFilterChange(s)}
            className={cn(
              "px-2 py-0.5 cursor-pointer uppercase tracking-wider",
              filter === s
                ? "text-[var(--color-fg)] bg-[var(--color-bg-2)]"
                : "text-[var(--color-fg-4)] hover:text-[var(--color-fg-2)]"
            )}
          >
            {s} <span className="tabular text-[var(--color-fg-5)]">{counts[s] ?? 0}</span>
          </button>
        ))}
        <span className="ml-auto text-[var(--color-fg-5)]">
          showing {filtered.length} of {items.length}
        </span>
      </div>

      <div className="flex-1 overflow-y-auto">
        {loading && (
          <div className="px-4 py-6 text-[var(--color-fg-5)] text-[11px] font-mono">
            Loading feed…
          </div>
        )}
        {!loading && filtered.length === 0 && (
          <div className="px-4 py-6 text-[var(--color-fg-5)] text-[11px] font-mono">
            No items match these filters. Try widening severity or clearing the initiative/org filter.
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
