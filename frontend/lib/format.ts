export function labelize(value: string): string {
  return value
    .split("_")
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join(" ");
}

export function formatScore(score: number | null): string {
  if (score === null) {
    return "No data yet";
  }
  return `${Math.round(score * 100)}%`;
}

export function formatConfidence(score: number | null): string {
  if (score === null) {
    return "No data yet";
  }
  return `${score.toFixed(1)} / 5`;
}

export function formatDateTime(value: string): string {
  return new Intl.DateTimeFormat("en-ZA", {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(new Date(value));
}
