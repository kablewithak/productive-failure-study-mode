"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { ErrorBox } from "@/components/error-box";
import { LoadingPanel } from "@/components/loading-panel";
import { PageHeader } from "@/components/page-header";
import { createSession, listConcepts } from "@/lib/api";
import { labelize } from "@/lib/format";
import type { Concept } from "@/lib/types";

export default function LearnPage() {
  const router = useRouter();
  const [concepts, setConcepts] = useState<Concept[]>([]);
  const [loading, setLoading] = useState(true);
  const [startingConceptId, setStartingConceptId] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    listConcepts()
      .then(setConcepts)
      .catch((issue: unknown) => setError(issue instanceof Error ? issue.message : "Could not load concepts."))
      .finally(() => setLoading(false));
  }, []);

  async function startSession(conceptId: string) {
    setStartingConceptId(conceptId);
    setError(null);
    try {
      const response = await createSession(conceptId);
      router.push(`/session/${response.session_id}`);
    } catch (issue) {
      setError(issue instanceof Error ? issue.message : "Could not create a learning session.");
      setStartingConceptId(null);
    }
  }

  return (
    <div className="space-y-8">
      <PageHeader
        eyebrow="Choose a concept"
        title="Start with a challenge, not an explanation."
        description="Each concept is seeded across a different discipline to prove the workflow is not a Python-only tutor."
      />

      {error ? <ErrorBox message={error} /> : null}
      {loading ? <LoadingPanel /> : null}

      <section className="grid gap-5 md:grid-cols-2">
        {concepts.map((concept) => (
          <article key={concept.concept_id} className="rounded-2xl border border-slate-200 bg-white p-6 shadow-panel">
            <div className="flex flex-wrap gap-2">
              <span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-semibold text-slate-700">
                {concept.discipline}
              </span>
              <span className="rounded-full bg-indigo-50 px-3 py-1 text-xs font-semibold text-indigo-700">
                {labelize(concept.challenge_type)}
              </span>
            </div>
            <h2 className="mt-4 text-xl font-bold text-slate-950">{concept.title}</h2>
            <p className="mt-2 text-sm leading-6 text-slate-600">{concept.learning_outcome}</p>
            <div className="mt-5 rounded-xl bg-slate-50 p-4 text-sm leading-6 text-slate-700">
              <span className="font-semibold text-slate-950">Challenge preview: </span>
              {concept.challenge_prompt}
            </div>
            <button
              type="button"
              onClick={() => startSession(concept.concept_id)}
              disabled={startingConceptId !== null}
              className="mt-5 w-full rounded-full bg-slate-950 px-4 py-3 text-sm font-semibold text-white hover:bg-slate-800 disabled:cursor-not-allowed disabled:bg-slate-400"
            >
              {startingConceptId === concept.concept_id ? "Creating session..." : "Attempt this concept"}
            </button>
          </article>
        ))}
      </section>
    </div>
  );
}
