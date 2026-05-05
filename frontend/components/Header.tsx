"use client";

import { useEffect, useState } from "react";
import { Search } from "lucide-react";
import { cn } from "@/lib/format";

export type TerminalMode = "feed" | "initiative" | "org";

export default function Header({
  onSearch,
  mode,
  onModeChange,
  onJumpInitiatives,
  onJumpCustomers,
  onJumpAgents,
}: {
  onSearch: (q: string) => void;
  mode: TerminalMode;
  onModeChange: (m: TerminalMode) => void;
  onJumpInitiatives: () => void;
  onJumpCustomers: () => void;
  onJumpAgents: () => void;
}) {
  const [now, setNow] = useState<string>("");
  const [q, setQ] = useState("");

  useEffect(() => {
    const tick = () => {
      const d = new Date();
      setNow(
        d
          .toLocaleString("en-US", {
            month: "short",
            day: "2-digit",
            hour: "2-digit",
            minute: "2-digit",
            second: "2-digit",
            hour12: false,
            timeZone: "America/Los_Angeles",
          })
          .replace(",", "")
      );
    };
    tick();
    const int = setInterval(tick, 1000);
    return () => clearInterval(int);
  }, []);

  // Keyboard shortcuts: cmd+k for search, 1/2/3/4 for nav
  useEffect(() => {
    function onKey(e: KeyboardEvent) {
      const t = e.target as HTMLElement;
      const isInput = t.tagName === "INPUT" || t.tagName === "TEXTAREA";
      if ((e.metaKey || e.ctrlKey) && e.key === "k") {
        e.preventDefault();
        onSearch("");
        return;
      }
      if (isInput) return;
      if (e.key === "1") onModeChange("feed");
      else if (e.key === "2") onJumpInitiatives();
      else if (e.key === "3") onJumpCustomers();
      else if (e.key === "4") onJumpAgents();
    }
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [onSearch, onModeChange, onJumpInitiatives, onJumpCustomers, onJumpAgents]);

  const navItem = (label: string, isActive: boolean, onClick: () => void, kbd: string) => (
    <button
      onClick={onClick}
      className={cn(
        "px-2 py-1 cursor-pointer transition-colors flex items-baseline gap-1.5",
        isActive
          ? "text-[var(--color-fg)] bg-[var(--color-bg-2)]"
          : "text-[var(--color-fg-3)] hover:text-[var(--color-fg)]"
      )}
    >
      <span>{label}</span>
      <kbd className="font-mono text-[9px] text-[var(--color-fg-5)] tabular">{kbd}</kbd>
    </button>
  );

  return (
    <header className="bb px-4 py-2 flex items-center gap-6 text-[12px]">
      <div className="flex items-center gap-2">
        <div className="live-dot" />
        <span className="text-display text-[18px] leading-none text-[var(--color-fg)]">QH HQ</span>
        <span className="font-mono text-[10px] text-[var(--color-fg-4)] uppercase tracking-widest pl-2">
          v0.1 · public sources
        </span>
      </div>

      <nav className="flex items-center gap-0.5 ml-2">
        {navItem("Feed", mode === "feed", () => onModeChange("feed"), "1")}
        {navItem("Initiatives", false, onJumpInitiatives, "2")}
        {navItem("Customers", false, onJumpCustomers, "3")}
        {navItem("Agents", false, onJumpAgents, "4")}
      </nav>

      <div className="flex-1 flex justify-center">
        <div className="bl br pl-2 pr-3 flex items-center gap-2 w-full max-w-xl bg-[var(--color-bg-1)] py-1.5">
          <Search size={12} className="text-[var(--color-fg-4)]" />
          <input
            type="text"
            value={q}
            onChange={(e) => setQ(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter" && q.trim()) onSearch(q.trim());
            }}
            placeholder="Semantic query — e.g. 'Hippocratic AI threats to marketplace NBL'"
            className="bg-transparent text-[12px] outline-none flex-1 text-[var(--color-fg-2)] placeholder:text-[var(--color-fg-5)]"
          />
          <kbd className="font-mono text-[10px] text-[var(--color-fg-5)] border border-[var(--color-fg-5)]/30 px-1 rounded">
            ⌘K
          </kbd>
        </div>
      </div>

      <div className="flex items-center gap-3 text-[var(--color-fg-4)] font-mono text-[11px] tabular">
        <a
          href="https://github.com/justinfink/qh-hq"
          target="_blank"
          rel="noreferrer"
          className="hover:text-[var(--color-fg)] transition-colors"
          title="View source on GitHub"
        >
          source
        </a>
        <span className="text-[var(--color-accent)]">● LIVE</span>
        <span>{now} PT</span>
      </div>
    </header>
  );
}
