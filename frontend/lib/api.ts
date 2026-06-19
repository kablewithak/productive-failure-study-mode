import type {
  Concept,
  CreateSessionResponse,
  DashboardMetricsResponse,
  SessionTraceResponse,
  SubmitAttemptResponse,
  QuizResultFeedback,
} from "./types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000";

class ApiClientError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "ApiClientError";
  }
}

async function requestJson<T>(path: string, init?: RequestInit): Promise<T> {
  const headers = new Headers(init?.headers);
  headers.set("content-type", "application/json");

  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...init,
    headers,
    cache: "no-store",
  });

  if (!response.ok) {
    let detail = `${response.status} ${response.statusText}`;
    try {
      const payload = (await response.json()) as { detail?: unknown };
      if (typeof payload.detail === "string") {
        detail = payload.detail;
      } else if (payload.detail && typeof payload.detail === "object") {
        detail = JSON.stringify(payload.detail);
      }
    } catch {
      // Keep status-based detail.
    }
    throw new ApiClientError(`API request failed for ${path}: ${detail}`);
  }

  return (await response.json()) as T;
}

export async function listConcepts(): Promise<Concept[]> {
  const payload = await requestJson<{ concepts: Concept[] }>("/concepts");
  return payload.concepts;
}

export async function createSession(conceptId: string): Promise<CreateSessionResponse> {
  return requestJson<CreateSessionResponse>("/sessions", {
    method: "POST",
    body: JSON.stringify({ concept_id: conceptId, student_alias: "demo-student" }),
  });
}

export async function getSessionTrace(sessionId: string): Promise<SessionTraceResponse> {
  return requestJson<SessionTraceResponse>(`/sessions/${sessionId}`);
}

export async function submitAttempt(input: {
  sessionId: string;
  attemptText: string;
  confidenceScore: number;
  confusionNote: string;
}): Promise<SubmitAttemptResponse> {
  return requestJson<SubmitAttemptResponse>(`/sessions/${input.sessionId}/attempt`, {
    method: "POST",
    body: JSON.stringify({
      attempt_text: input.attemptText,
      confidence_score: input.confidenceScore,
      confusion_note: input.confusionNote.trim() === "" ? null : input.confusionNote,
    }),
  });
}

export async function submitQuiz(input: {
  sessionId: string;
  answers: Array<{ question_id: string; answer_text: string }>;
}): Promise<{ quiz_result: QuizResultFeedback; recommended_next_step: string }> {
  return requestJson<{ quiz_result: QuizResultFeedback; recommended_next_step: string }>(
    `/sessions/${input.sessionId}/quiz`,
    {
      method: "POST",
      body: JSON.stringify({ answers: input.answers }),
    },
  );
}

export async function getDashboardMetrics(): Promise<DashboardMetricsResponse> {
  return requestJson<DashboardMetricsResponse>("/dashboard");
}
