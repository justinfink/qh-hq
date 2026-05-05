"use client";

import { useEffect, useState } from "react";
import { Search } from "lucide-react";

export default function Header({
  onSearch,
}: {
  onSearch: (q: string) => void;
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

  return (
    <header className="bb px-4 py-2 flex items-center gap-6 text-[12px]">
      <div className="flex items-center gap-2">
        <div className="live-dot" />
        <span className="text-display text-[18px] leading-none text-[var(--color-fg)]">
          QH HQ
        </span>
        <span className="font-mono text-[10px] text-[var(--color-fg-4)] uppercase tracking-widest pl-2">
          v0.1 · MOCK + PUBLIC SOURCES
        </span>
      </div>

      <nav className="flex items-center gap-5 ml-2 text-[var(--color-fg-3)]">
        <span className="text-[var(--color-fg)]">Terminal</span>
        <span className="hover:text-[var(--color-fg)] cursor-pointer">Initiatives</span>
        <span className="hover:text-[var(--color-fg)] cursor-pointer">Customers</span>
        <span className="hover:text-[var(--color-fg)] cursor-pointer">Agents</span>
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
            ⏎
          </kbd>
        </div>
      </div>

      <div className="flex items-center gap-4 text-[var(--color-fg-4)] font-mono text-[11px] tabular">
        <span className="text-[var(--color-accent)]">● LIVE</span>
        <span>{now} PT</span>
        <span>justin.fink@qualifiedhealth.com</span>
      </div>
    </header>
  );
}
