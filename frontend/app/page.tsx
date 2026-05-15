"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import Header, { type TerminalMode } from "@/components/Header";
import InitiativesRail from "@/components/InitiativesRail";
import SignalFeed from "@/components/SignalFeed";
import SignalDetail from "@/components/SignalDetail";
import AgentRail from "@/components/AgentRail";
import InitiativePanel from "@/components/InitiativePanel";
import RelationshipMap from "@/components/RelationshipMap";
import OrganizationPanel from "@/components/OrganizationPanel";
import SearchModal from "@/components/SearchModal";
import type { FeedItem } from "@/lib/types";

export default function Terminal() {
  const [selectedFeedItem, setSelectedFeedItem] = useState<FeedItem | null>(null);
  const [selectedInitiative, setSelectedInitiative] = useState<string | null>(null);
  const [selectedOrg, setSelectedOrg] = useState<string | null>(null);
  const [filter, setFilter] = useState<FeedItem["severity"] | "all">("all");
  const [mode, setMode] = useState<TerminalMode>("feed");
  const [searchOpen, setSearchOpen] = useState(false);
  const [searchQ, setSearchQ] = useState("");

  const initiativesRef = useRef<HTMLElement>(null);
  const customersRef = useRef<HTMLElement>(null);
  const agentsRef = useRef<HTMLElement>(null);

  const flash = useCallback((el: HTMLElement | null) => {
    if (!el) return;
    el.scrollIntoView({ behavior: "smooth", block: "nearest" });
    el.style.transition = "outline-color 1.4s";
    el.style.outline = "1px solid var(--color-accent)";
    el.style.outlineOffset = "-1px";
    setTimeout(() => { el.style.outline = "1px solid transparent"; }, 1400);
  }, []);

  return (
    <div className="h-screen w-screen flex flex-col overflow-hidden bg-[var(--color-bg)]">
      <Header
        onSearch={(q) => { setSearchQ(q); setSearchOpen(true); }}
        mode={mode}
        onModeChange={(m) => { setMode(m); }}
        onJumpInitiatives={() => flash(initiativesRef.current)}
        onJumpCustomers={() => flash(customersRef.current)}
        onJumpAgents={() => flash(agentsRef.current)}
      />
      <SearchModal open={searchOpen} initialQ={searchQ} onClose={() => setSearchOpen(false)} />

      <div className="flex-1 grid grid-cols-[260px_1fr_420px_280px] overflow-hidden">
        <aside ref={initiativesRef} className="br overflow-hidden">
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
          <div ref={agentsRef as React.RefObject<HTMLDivElement>} className="bb overflow-hidden">
            <AgentRail />
          </div>
          <div ref={customersRef as React.RefObject<HTMLDivElement>} className="overflow-hidden">
            <RelationshipMap
              selectedId={selectedOrg}
              onSelect={(id) => { setSelectedOrg(id); setMode("org"); }}
            />
          </div>
        </aside>
      </div>

      <footer className="bt px-4 py-1.5 flex items-center justify-between font-mono text-[10px] text-[var(--color-fg-5)] tabular">
        <div className="flex items-center gap-4">
          <span>QH HQ TERMINAL · v0.2</span>
          <span>built by{" "}
            <a href="https://justinryanventures.com" target="_blank" rel="noreferrer" className="text-[var(--color-fg-3)] hover:text-[var(--color-accent)]">
              Justin Fink
            </a>{" "}for the QH Strategy &amp; Ops MBA Intern application
          </span>
          <a href="https://www.linkedin.com/in/justinryanfink" target="_blank" rel="noreferrer" className="hover:text-[var(--color-accent)]">linkedin</a>
          <a href="mailto:justin.ryan.fink@gmail.com" className="hover:text-[var(--color-accent)]">email</a>
          <a href="https://github.com/justinfink/qh-hq" target="_blank" rel="noreferrer" className="hover:text-[var(--color-accent)]">source</a>
        </div>
        <div className="flex items-center gap-4">
          <span>db · supabase pgvector</span>
          <span>llm · claude opus 4.7 + haiku 4.5</span>
          <span>embed · voyage-3-large / bge-large</span>
        </div>
      </footer>
    </div>
  );
}
