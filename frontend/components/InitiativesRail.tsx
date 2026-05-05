"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import type { Initiative } from "@/lib/types";
import {
  STAGE_LABEL, VELOCITY_GLYPH, VELOCITY_COLOR, CONFIDENCE_COLOR, fmtUSDk, fmtDate, cn,
} from "@/lib/format";

const KIND_LABEL: Record<string, string> = {
  nbl: "NBL",
  partnership: "PARTNER",
  strategic_project: "STRAT",
  core_product: "CORE",
  internal_op: "OPS",
};

export default function InitiativesRail({
  selectedId,
  onSelect,
}: {
  selectedId: string | null;
  onSelect: (id: string) => void;
}) {
  const [initiatives, setInitiatives] = useState<Initiative[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.initiatives()
      .then((res) => setInitiatives(res.initiatives))
      .catch(() => {/* offline */})
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="h-full flex flex-col">
      <div className="bb px-3 py-2 flex items-center justify-between">
        <span className="font-mono text-[10px] text-[var(--color-fg-3)] uppercase tracking-widest">
          Initiatives · {initiatives.length}
        </span>
        <span className="font-mono text-[10px] text-[var(--color-fg-5)]">
          ↑↓ nav
        </span>
      </div>

      <div className="flex-1 overflow-y-auto">
        {loading && (
          <div className="px-3 py-6 text-[var(--color-fg-5)] text-[11px] font-mono">
            Loading initiatives…
          </div>
        )}
        {!loading && initiatives.length === 0 && (
          <div className="px-3 py-6 text-[var(--color-fg-5)] text-[11px] font-mono">
            No initiatives. Run seed script.
          </div>
        )}
        {initiatives.map((init) => {
          const isSel = init.id === selectedId;
          const kindLabel = KIND_LABEL[init.kind] ?? init.kind.toUpperCase();
          return (
            <button
              key={init.id}
              onClick={() => onSelect(init.id)}
              className={cn(
                "w-full text-left px-3 py-2 bb row-hover cursor-pointer block",
                isSel && "bg-[var(--color-bg-2)]"
              )}
            >
              <div className="flex items-center justify-between gap-2 mb-1">
                <span className="font-mono text-[10px] text-[var(--color-accent)] tabular">
                  {init.code}
                </span>
                <span className="font-mono text-[9px] text-[var(--color-fg-5)] uppercase tracking-wider">
                  {kindLabel}
                </span>
              </div>
              <div className="text-[12px] text-[var(--color-fg)] leading-snug mb-1.5 pr-1">
                {init.name}
              </div>
              <div className="flex items-center gap-2 text-[10px] font-mono">
                <span className="text-[var(--color-fg-4)]">
                  {STAGE_LABEL[init.stage]}
                </span>
                <span className={cn(VELOCITY_COLOR[init.velocity])}>
                  {VELOCITY_GLYPH[init.velocity]}
                </span>
                <span className={cn(CONFIDENCE_COLOR[init.confidence])}>
                  {init.confidence.toUpperCase()}
                </span>
                <span className="text-[var(--color-fg-5)] tabular ml-auto">
                  {init.fte_allocated ? `${init.fte_allocated.toFixed(1)} FTE` : ""}
                </span>
              </div>
              {init.next_milestone_date && (
                <div className="mt-1.5 text-[10px] font-mono text-[var(--color-fg-4)] tabular">
                  next · {fmtDate(init.next_milestone_date)}
                </div>
              )}
            </button>
          );
        })}
      </div>
    </div>
  );
}
