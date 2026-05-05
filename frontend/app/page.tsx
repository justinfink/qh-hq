"use client";

import { useState } from "react";
import Header from "@/components/Header";
import InitiativesRail from "@/components/InitiativesRail";
import SignalFeed from "@/components/SignalFeed";
import SignalDetail from "@/components/SignalDetail";
import AgentRail from "@/components/AgentRail";
import InitiativePanel from "@/components/InitiativePanel";
import RelationshipMap from "@/components/RelationshipMap";
import OrganizationPanel from "@/components/OrganizationPanel";
import SearchModal from "@/components/SearchModal";
import type { FeedItem } from "@/lib/types";

type Mode = "feed" | "initiative" | "org";

export default function Terminal() {
  const [selectedFeedItem, setSelectedFeedItem] = useState<FeedItem | null>(null);
  const [selectedInitiative, setSelectedInitiative] = useState<string | null>(null);
  const [selectedOrg, setSelectedOrg] = useState<string | null>(null);
  const [filter, setFilter] = useState<FeedItem["severity"] | "all">("all");
  const [mode, setMode] = useState<Mode>("feed");
  const [searchOpen, setSearchOpen] = useState(false);
  const [searchQ, setSearchQ] = useState("");

  return (
    <div className="h-screen w-screen flex flex-col overflow-hidden bg-[var(--color-bg)]">
      <Header onSearch={(q) => { setSearchQ(q); setSearchOpen(true); }} />
      <SearchModal open={searchOpen} initialQ={searchQ} onClose={() => setSearchOpen(false)} />

      <div className="flex-1 grid grid-cols-[260px_1fr_420px_280px] overflow-hidden">
        <aside className="br overflow-hidden">
          <InitiativesRail
            selectedId={selectedInitiative}
            onSelect={(id) => { setSelectedInitiative(id); setMode("initiative"); }}
          />
        </aside>

        <main className="br overflow-hidden">
          <SignalFeed
            selectedId={selectedFeedItem?.implication_id ?? null}
            onSelect={(item) => { setSelectedFeedItem(item); setMode("feed"); }}
            filter={filter}
            onFilterChange={setFilter}
          />
        </main>

        <section className="br overflow-hidden">
          {mode === "feed" && <SignalDetail item={selectedFeedItem} />}
          {mode === "initiative" && <InitiativePanel initiativeId={selectedInitiative} />}
          {mode === "org" && <OrganizationPanel orgId={selectedOrg} />}
        </section>

        <aside className="overflow-hidden grid grid-rows-[1fr_400px]">
          <div className="bb overflow-hidden">
            <AgentRail />
          </div>
          <div className="overflow-hidden">
            <RelationshipMap
              selectedId={selectedOrg}
              onSelect={(id) => { setSelectedOrg(id); setMode("org"); }}
            />
          </div>
        </aside>
      </div>

      <footer className="bt px-4 py-1.5 flex items-center justify-between font-mono text-[10px] text-[var(--color-fg-5)] tabular">
        <div className="flex items-center gap-4">
          <span>QH HQ TERMINAL · v0.1</span>
          <span>built by Justin Fink for QH Strategy &amp; Ops Intern</span>
          <a href="https://qualifiedhealthai.com" target="_blank" rel="noreferrer" className="hover:text-[var(--color-accent)]">
            qualifiedhealthai.com
          </a>
        </div>
        <div className="flex items-center gap-4">
          <span>backend · :8000</span>
          <span>db · supabase pgvector</span>
          <span>llm · claude opus 4.7 · haiku 4.5</span>
          <span>embed · voyage-3-large</span>
        </div>
      </footer>
    </div>
  );
}
