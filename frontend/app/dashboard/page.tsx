"use client";

import { useEffect, useState } from "react";
import { ErrorBox } from "@/components/error-box";
import { LoadingPanel } from "@/components/loading-panel";
import { PageHeader } from "@/components/page-header";
import { StatusCard } from "@/components/status-card";
import { getDashboardMetrics } from "@/lib/api";
import { formatConfidence, formatDateTime, formatScore, labelize } from "@/lib/format";
import type { DashboardMetricsResponse } from "@/lib/types";

export default function DashboardPage() {
  const [metrics, setMetrics] = useState<DashboardMetricsResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getDashboardMetrics()
      .then(setMetrics)
      .catch((issue: unknown) => setError(issue instanceof Error ? issue.message : "Could not load dashboard metrics."))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="space-y-8">
      <PageHeader
        eyebrow="Learning event dashboard"
        title="Measure the study behaviour, not fake outcome proof."
        description="These metrics show sessions, attempts, failure labels, quiz scores, and concept coverage from the local backend repository."
      />

      {error ? <ErrorBox message={error} /> : null}
      {loading ? <LoadingPanel /> : null}

      {metrics ? (
        <>
          <section className="grid gap-4 md:grid-cols-4">
            <StatusCard label="Total sessions" value={metrics.total_sessions} />
            <StatusCard label="Completed sessions" value={metrics.completed_sessions} />
            <StatusCard label="Average confidence" value={formatConfidence(metrics.average_confidence_score)} />
            <StatusCard label="Average quiz score" value={formatScore(metrics.average_quiz_score)} />
          </section>

          <section className="grid gap-5 md:grid-cols-2">
            <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-panel">
              <h2 className="text-lg font-semibold text-slate-950">Failure label distribution</h2>
              {metrics.failure_label_distribution.length === 0 ? (
                <p className="mt-4 text-sm text-slate-600">No attempts have been submitted yet.</p>
              ) : (
                <div className="mt-5 space-y-3">
                  {metrics.failure_label_distribution.map((item) => (
                    <div key={item.failure_label}>
                      <div className="flex justify-between text-sm">
                        <span className="font-medium text-slate-700">{labelize(item.failure_label)}</span>
                        <span className="text-slate-500">{item.count}</span>
                      </div>
                      <div className="mt-2 h-2 rounded-full bg-slate-100">
                        <div
                          className="h-2 rounded-full bg-indigo-600"
                          style={{ width: `${Math.max(8, item.count * 18)}%` }}
                        />
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>

            <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-panel">
              <h2 className="text-lg font-semibold text-slate-950">Concepts attempted</h2>
              {metrics.concepts_attempted.length === 0 ? (
                <p className="mt-4 text-sm text-slate-600">No concepts have been attempted yet.</p>
              ) : (
                <div className="mt-5 space-y-3">
                  {metrics.concepts_attempted.map((concept) => (
                    <div key={concept.concept_id} className="rounded-xl bg-slate-50 p-4">
                      <p className="font-semibold text-slate-950">{concept.title}</p>
                      <p className="mt-1 text-sm text-slate-600">
                        {concept.discipline} · {concept.attempt_count} attempt{concept.attempt_count === 1 ? "" : "s"}
                      </p>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </section>

          <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-panel">
            <h2 className="text-lg font-semibold text-slate-950">Recent learning events</h2>
            {metrics.recent_learning_events.length === 0 ? (
              <p className="mt-4 text-sm text-slate-600">Complete a session from the Learn page to populate this table.</p>
            ) : (
              <div className="mt-5 overflow-x-auto">
                <table className="w-full min-w-[760px] text-left text-sm">
                  <thead className="border-b border-slate-200 text-xs uppercase tracking-wide text-slate-500">
                    <tr>
                      <th className="py-3 pr-4">Concept</th>
                      <th className="py-3 pr-4">Status</th>
                      <th className="py-3 pr-4">Failure label</th>
                      <th className="py-3 pr-4">Confidence</th>
                      <th className="py-3 pr-4">Quiz score</th>
                      <th className="py-3 pr-4">Updated</th>
                    </tr>
                  </thead>
                  <tbody>
                    {metrics.recent_learning_events.map((event) => (
                      <tr key={event.session_id} className="border-b border-slate-100 text-slate-700">
                        <td className="py-3 pr-4 font-medium text-slate-950">{event.concept_title}</td>
                        <td className="py-3 pr-4">{labelize(event.status)}</td>
                        <td className="py-3 pr-4">{event.failure_label ? labelize(event.failure_label) : "Not attempted"}</td>
                        <td className="py-3 pr-4">{event.confidence_score ?? "—"}</td>
                        <td className="py-3 pr-4">{event.quiz_score === null ? "—" : formatScore(event.quiz_score)}</td>
                        <td className="py-3 pr-4">{formatDateTime(event.updated_at)}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </section>
        </>
      ) : null}
    </div>
  );
}
