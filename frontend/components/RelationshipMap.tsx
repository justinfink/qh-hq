"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import type { Organization, Trajectory } from "@/lib/types";
import { TRAJECTORY_COLOR, TRAJECTORY_GLYPH, relStrengthBar, cn } from "@/lib/format";

const RELATIONSHIP_LABEL: Record<string, string> = {
  customer: "CUSTOMER",
  pilot: "PILOT",
  prospect: "PROSPECT",
  partner: "PARTNER",
  competitor: "COMPETITOR",
  investor: "INVESTOR",
  regulator_watch: "REG WATCH",
  ecosystem: "ECOSYSTEM",
};

const REL_COLOR: Record<string, string> = {
  customer: "text-[var(--color-accent)]",
  pilot: "text-[var(--color-accent)]",
  prospect: "text-[#4FA8D8]",
  partner: "text-[#4FA8D8]",
  competitor: "text-[#FF4B6E]",
  investor: "text-[#4ECCA3]",
  regulator_watch: "text-[#FFA84A]",
  ecosystem: "text-[var(--color-fg-3)]",
};

export default function RelationshipMap({
  selectedId,
  onSelect,
}: {
  selectedId: string | null;
  onSelect: (id: string) => void;
}) {
  const [orgs, setOrgs] = useState<Organization[]>([]);
  const [filter, setFilter] = useState<string>("all");

  useEffect(() => {
    api.organizations()
      .then((r) => setOrgs(r.organizations))
      .catch(() => {});
  }, []);

  const groupOrder = ["customer", "pilot", "prospect", "partner", "competitor", "investor", "regulator_watch", "ecosystem"];
  const grouped = groupOrder.map((rel) => ({
    rel,
    orgs: orgs.filter((o) => o.relationship === rel && o.name !== "Qualified Health"),
  })).filter((g) => g.orgs.length > 0);

  const filtered = filter === "all" ? grouped : grouped.filter((g) => g.rel === filter);

  return (
    <div className="h-full flex flex-col">
      <div className="bb px-3 py-2 flex items-center justify-between">
        <span className="font-mono text-[10px] text-[var(--color-fg-3)] uppercase tracking-widest">
          Relationship Map · {orgs.filter((o) => o.name !== "Qualified Health").length}
        </span>
        <select
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
          className="bg-[var(--color-bg-1)] border border-[var(--color-line)] text-[var(--color-fg-3)] font-mono text-[10px] px-1.5 py-0.5 cursor-pointer"
        >
          <option value="all">all</option>
          {groupOrder.map((g) => (
            <option key={g} value={g}>{RELATIONSHIP_LABEL[g]}</option>
          ))}
        </select>
      </div>

      <div className="flex-1 overflow-y-auto">
        {filtered.map((group) => (
          <div key={group.rel}>
            <div className="px-3 py-1.5 bg-[var(--color-bg-1)] bb">
              <span className={cn("font-mono text-[10px] uppercase tracking-widest tabular", REL_COLOR[group.rel])}>
                {RELATIONSHIP_LABEL[group.rel]} · {group.orgs.length}
              </span>
            </div>
            {group.orgs.map((org) => {
              const dyn = org.metadata?.dynamics;
              const traj = (dyn?.trajectory ?? "stable") as Trajectory;
              const isSel = org.id === selectedId;
              return (
                <button
                  key={org.id}
                  onClick={() => onSelect(org.id)}
                  className={cn(
                    "w-full text-left px-3 py-2 bb row-hover cursor-pointer block",
                    isSel && "bg-[var(--color-bg-2)]"
                  )}
                >
                  <div className="flex items-center justify-between">
                    <span className="text-[12px] text-[var(--color-fg)]">
                      {org.short_name || org.name}
                    </span>
                    <span className={cn("font-mono text-[12px]", TRAJECTORY_COLOR[traj])}>
                      {TRAJECTORY_GLYPH[traj]}
                    </span>
                  </div>
                  {dyn?.relationship_strength != null && (
                    <div className="font-mono text-[10px] text-[var(--color-fg-5)] tabular leading-tight mt-0.5">
                      <span className={cn(
                        dyn.relationship_strength >= 7 ? "text-[var(--color-accent)]" :
                        dyn.relationship_strength >= 4 ? "text-[var(--color-fg-3)]" :
                        "text-[#FFA84A]"
                      )}>
                        {relStrengthBar(dyn.relationship_strength)}
                      </span>{" "}
                      <span>{dyn.relationship_strength}/10</span>
                    </div>
                  )}
                </button>
              );
            })}
          </div>
        ))}
      </div>
    </div>
  );
}
