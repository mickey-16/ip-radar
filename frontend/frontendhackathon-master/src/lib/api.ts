const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || "").replace(/\/$/, "");

export interface IntelligenceRecord {
  source?: string;
  category?: string;
  evidence?: string;
  confidence?: string | number;
  date?: string;
  [key: string]: unknown;
}

export interface ThreatAnalysisResponse {
  ip_address: string;
  threat_score: number;
  risk_level: string;
  confidence?: number;
  categories?: string[];
  sources?: Record<string, unknown>;
  api_results?: Record<string, unknown>;
  geolocation?: {
    country?: string;
    city?: string;
    latitude?: number;
    longitude?: number;
    [key: string]: unknown;
  };
  darkweb_intelligence?: {
    found_in_darkweb: boolean;
    tor_exit_node: boolean;
    breach_activity: { found: boolean; breach_count: number; breaches: unknown[] };
    malware_urls: { found: boolean; url_count: number; urls: unknown[] };
    threat_level: string;
    indicators: string[];
  };
  [key: string]: unknown;
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...(init?.headers || {}),
    },
  });

  if (!response.ok) {
    let message = `Request failed (${response.status})`;
    try {
      const body = await response.json() as { error?: string };
      if (body.error) message = body.error;
    } catch {
      // Keep the status-based message when the response is not JSON.
    }
    throw new Error(message);
  }

  return response.json() as Promise<T>;
}

export function analyzeIP(ipAddress: string, useCache = false) {
  return request<ThreatAnalysisResponse>("/api/analyze", {
    method: "POST",
    body: JSON.stringify({ ip_address: ipAddress, use_cache: useCache }),
  });
}

export async function downloadReport(ipAddress: string): Promise<Blob> {
  const response = await fetch(
    `${API_BASE_URL}/api/download-report/${encodeURIComponent(ipAddress)}`,
  );
  if (!response.ok) {
    throw new Error(`Report download failed (${response.status})`);
  }
  return response.blob();
}

export function transformToIntelligenceRecords(
  sources: Record<string, unknown>,
): IntelligenceRecord[] {
  return Object.entries(sources).flatMap(([source, value]) => {
    if (!value || typeof value !== "object") return [];
    const sourceData = value as Record<string, unknown>;
    const records = Array.isArray(sourceData.records)
      ? sourceData.records
      : [sourceData];

    return records
      .filter((record): record is Record<string, unknown> => (
        Boolean(record) && typeof record === "object"
      ))
      .map((record) => ({
        source,
        category: String(record.category ?? record.classification ?? "Threat intelligence"),
        evidence: String(record.evidence ?? record.description ?? record.message ?? "-"),
        confidence: record.confidence ?? record.confidence_score ?? "-",
        date: String(record.date ?? record.last_seen ?? "-"),
      }));
  });
}
