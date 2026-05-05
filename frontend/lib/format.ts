import type {
  Trajectory, SignalSeverity, InitiativeStage, Velocity, Confidence,
} from "./types";

export function timeAgo(iso?: string | null): string {
  if (!iso) return "—";
  const then = new Date(iso).getTime();
  const now = Date.now();
  const diffSec = Math.floor((now - then) / 1000);
  if (diffSec < 60) return `${diffSec}s ago`;
  const diffMin = Math.floor(diffSec / 60);
  if (diffMin < 60) return `${diffMin}m ago`;
  const diffHr = Math.floor(diffMin / 60);
  if (diffHr < 24) return `${diffHr}h ago`;
  const diffDay = Math.floor(diffHr / 24);
  if (diffDay < 30) return `${diffDay}d ago`;
  const diffMo = Math.floor(diffDay / 30);
  if (diffMo < 12) return `${diffMo}mo ago`;
  return `${Math.floor(diffMo / 12)}y ago`;
}

export function fmtDate(iso?: string | null): string {
  if (!iso) return "—";
  const d = new Date(iso);
  return d.toLocaleDateString("en-US", { month: "short", day: "numeric", year: "2-digit" });
}

export function fmtUSDk(n?: number | null): string {
  if (n == null) return "—";
  if (n >= 1_000_000) return `$${(n / 1_000_000).toFixed(1)}M`;
  if (n >= 1_000) return `$${(n / 1_000).toFixed(0)}K`;
  return `$${n.toFixed(0)}`;
}

export const SEVERITY_COLOR: Record<SignalSeverity, { fg: string; bg: string; bd: string }> = {
  critical: { fg: "text-[#FF4B6E]", bg: "bg-[#FF4B6E]/10", bd: "border-[#FF4B6E]/40" },
  high:     { fg: "text-[#FFA84A]", bg: "bg-[#FFA84A]/10", bd: "border-[#FFA84A]/40" },
  medium:   { fg: "text-[#4FA8D8]", bg: "bg-[#4FA8D8]/10", bd: "border-[#4FA8D8]/40" },
  low:      { fg: "text-[#8E95A2]", bg: "bg-[#8E95A2]/10", bd: "border-[#8E95A2]/30" },
  fyi:      { fg: "text-[#5C6470]", bg: "bg-transparent",  bd: "border-[#5C6470]/30" },
};

export const TRAJECTORY_COLOR: Record<Trajectory, string> = {
  improving:    "text-[#4ECCA3]",
  stable:       "text-[#8E95A2]",
  deteriorating:"text-[#FF4B6E]",
  volatile:     "text-[#FFA84A]",
};

export const TRAJECTORY_GLYPH: Record<Trajectory, string> = {
  improving: "↗",
  stable: "→",
  deteriorating: "↘",
  volatile: "⇅",
};

export const STAGE_LABEL: Record<InitiativeStage, string> = {
  discovery: "DISCOVERY",
  greenlight: "GREENLIGHT",
  pilot: "PILOT",
  early_revenue: "EARLY REV",
  scaling: "SCALING",
  paused: "PAUSED",
};

export const VELOCITY_GLYPH: Record<Velocity, string> = {
  accelerating: "▲",
  holding: "■",
  slipping: "▼",
};

export const VELOCITY_COLOR: Record<Velocity, string> = {
  accelerating: "text-[#4ECCA3]",
  holding: "text-[#8E95A2]",
  slipping: "text-[#FFA84A]",
};

export const CONFIDENCE_COLOR: Record<Confidence, string> = {
  high: "text-[#4ECCA3]",
  medium: "text-[#8E95A2]",
  low: "text-[#FFA84A]",
};

export function relStrengthBar(strength?: number): string {
  // Renders a 10-cell strength bar like ▰▰▰▱▱▱▱▱▱▱
  const s = Math.max(0, Math.min(10, Math.round(strength ?? 0)));
  return "▰".repeat(s) + "▱".repeat(10 - s);
}

export function severityRank(s: SignalSeverity): number {
  return { critical: 0, high: 1, medium: 2, low: 3, fyi: 4 }[s];
}

export function cn(...parts: (string | false | null | undefined)[]): string {
  return parts.filter(Boolean).join(" ");
}
