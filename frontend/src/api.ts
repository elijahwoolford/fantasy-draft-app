export type DraftResponse = {
  draftOrder: string[];
  odds: number[];
};

function formatErrorDetail(detail: unknown): string {
  if (typeof detail === "string") return detail;
  if (Array.isArray(detail)) {
    return detail
      .map((e) => (typeof e === "object" && e && "msg" in e ? String((e as { msg: string }).msg) : String(e)))
      .join("; ");
  }
  return "Request failed";
}

export async function postDraft(teams: string[]): Promise<DraftResponse> {
  const res = await fetch("/api/draft", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ teams }),
  });
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    const detail = (body as { detail?: unknown }).detail;
    throw new Error(formatErrorDetail(detail ?? res.statusText));
  }
  return res.json() as Promise<DraftResponse>;
}
