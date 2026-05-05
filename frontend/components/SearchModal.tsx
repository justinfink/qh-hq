"use client";

import { useEffect, useRef, useState } from "react";
import { api } from "@/lib/api";
import { cn } from "@/lib/format";
import { Search, X } from "lucide-react";

interface SearchHit {
  id: string;
  title?: string;
  name?: string;
  similarity: number;
  [k: string]: unknown;
}

interface SearchResults {
  signals: SearchHit[];
  initiatives: SearchHit[];
  organizations: SearchHit[];
  documents: SearchHit[];
}

export default function SearchModal({
  open,
  initialQ,
  onClose,
}: {
  open: boolean;
  initialQ: string;
  onClose: () => void;
}) {
  const [q, setQ] = useState(initialQ);
  const [results, setResults] = useState<SearchResults | null>(null);
  const [loading, setLoading] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (open) {
      setQ(initialQ);
      setTimeout(() => inputRef.current?.focus(), 50);
      if (initialQ) run(initialQ);
    } else {
      setResults(null);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [open, initialQ]);

  useEffect(() => {
    function onKey(e: KeyboardEvent) {
      if (e.key === "Escape") onClose();
    }
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [onClose]);

  async function run(query: string) {
    if (!query.trim()) return;
    setLoading(true);
    try {
      const r = await api.search(query, 6);
      setResults(r as unknown as SearchResults);
    } finally {
      setLoading(false);
    }
  }

  if (!open) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-start justify-center pt-20 bg-black/60 backdrop-blur-sm">
      <div className="w-full max-w-3xl border border-[var(--color-line)] bg-[var(--color-bg-1)] shadow-2xl">
        <div className="bb px-4 py-3 flex items-center gap-3">
          <Search size={14} className="text-[var(--color-accent)]" />
          <input
            ref={inputRef}
            value={q}
            onChange={(e) => setQ(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") run(q);
            }}
            placeholder="Semantic query · vector search across all entities…"
            className="flex-1 bg-transparent outline-none text-[14px] text-[var(--color-fg)] placeholder:text-[var(--color-fg-5)]"
          />
          <button onClick={onClose} className="text-[var(--color-fg-4)] hover:text-[var(--color-fg)]">
            <X size={14} />
          </button>
        </div>

        <div className="max-h-[60vh] overflow-y-auto px-4 py-3">
          {loading && (
            <div className="font-mono text-[11px] text-[var(--color-fg-4)]">embedding query… retrieving via cosine distance…</div>
          )}
          {!loading && !results && (
            <div className="font-mono text-[11px] text-[var(--color-fg-5)]">
              Try: <span className="text-[var(--color-fg-3)]">&ldquo;Hippocratic AI threats to marketplace NBL&rdquo;</span>{" · "}
              <span className="text-[var(--color-fg-3)]">&ldquo;CMS regulatory tailwinds for payer NBL&rdquo;</span>{" · "}
              <span className="text-[var(--color-fg-3)]">&ldquo;multi-EHR prospects&rdquo;</span>
            </div>
          )}
          {results && (
            <div className="space-y-5">
              <SearchSection title="Signals" hits={results.signals} render={(h) => h.title as string} />
              <SearchSection title="Initiatives" hits={results.initiatives} render={(h) => h.name as string} />
              <SearchSection title="Organizations" hits={results.organizations} render={(h) => h.name as string} />
              {results.documents.length > 0 && (
                <SearchSection title="Documents" hits={results.documents} render={(h) => h.title as string} />
              )}
            </div>
          )}
        </div>

        <div className="bt px-4 py-2 flex items-center justify-between font-mono text-[10px] text-[var(--color-fg-5)]">
          <span>1024-dim BGE-large embedding · pgvector cosine · top 6 per category</span>
          <span>esc to close</span>
        </div>
      </div>
    </div>
  );
}

function SearchSection({
  title,
  hits,
  render,
}: {
  title: string;
  hits: SearchHit[];
  render: (h: SearchHit) => string;
}) {
  if (!hits || hits.length === 0) return null;
  return (
    <section>
      <div className="font-mono text-[10px] text-[var(--color-fg-3)] uppercase tracking-widest mb-2">
        {title}
      </div>
      <div className="space-y-1">
        {hits.map((h) => (
          <div key={h.id} className="flex items-start gap-3 py-1">
            <span className={cn(
              "font-mono text-[10px] tabular w-12 shrink-0 pt-0.5",
              h.similarity > 0.7 ? "text-[var(--color-accent)]" :
              h.similarity > 0.5 ? "text-[var(--color-fg-3)]" : "text-[var(--color-fg-5)]"
            )}>
              {(h.similarity * 100).toFixed(0)}%
            </span>
            <span className="text-[12px] text-[var(--color-fg-2)] leading-snug flex-1">
              {render(h)}
            </span>
          </div>
        ))}
      </div>
    </section>
  );
}
