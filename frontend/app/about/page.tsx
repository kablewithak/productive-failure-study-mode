import { PageHeader } from "@/components/page-header";

const limitations = [
  "No real student data should be entered.",
  "No uploaded university material is used in this version.",
  "The AI behaviour is deterministic mock mode, not live model inference.",
  "The prototype does not prove improved student outcomes.",
  "The local JSON store is a development adapter, not production infrastructure.",
];

const nextSteps = [
  "Ground challenges in uploaded course material through a restricted retrieval boundary.",
  "Add spaced follow-up sessions after the initial retrieval quiz.",
  "Add multilingual simplification after the attempt-first boundary, not before it.",
  "Run controlled learning-outcome evals before making outcome claims.",
];

export default function AboutPage() {
  return (
    <div className="space-y-8">
      <PageHeader
        eyebrow="Research to product behaviour"
        title="Attempt First Mode operationalizes Productive Failure as a study workflow."
        description="The product bet is simple: AI tutors should not explain too quickly. Students need a safe moment to expose what they understand before receiving polished instruction."
      />

      <section className="grid gap-5 md:grid-cols-2">
        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-panel">
          <h2 className="text-lg font-semibold text-slate-950">Product hypothesis</h2>
          <p className="mt-3 leading-7 text-slate-600">
            A student selects a concept, attempts a short pre-instruction challenge, receives structured
            failure analysis, gets targeted consolidation, and then completes retrieval practice. The dashboard
            records behaviour, not fake proof of mastery.
          </p>
        </div>
        <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-panel">
          <h2 className="text-lg font-semibold text-slate-950">Stack</h2>
          <p className="mt-3 leading-7 text-slate-600">
            Next.js, React, TypeScript, Tailwind, FastAPI, Pydantic v2, deterministic mock AI, repository adapters,
            local JSON persistence, and backend tests.
          </p>
        </div>
      </section>

      <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-panel">
        <h2 className="text-lg font-semibold text-slate-950">Limitations</h2>
        <ul className="mt-4 space-y-3 text-sm leading-6 text-slate-700">
          {limitations.map((item) => (
            <li key={item} className="flex gap-3">
              <span className="mt-2 h-2 w-2 shrink-0 rounded-full bg-slate-400" />
              {item}
            </li>
          ))}
        </ul>
      </section>

      <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-panel">
        <h2 className="text-lg font-semibold text-slate-950">Next product moves</h2>
        <ul className="mt-4 space-y-3 text-sm leading-6 text-slate-700">
          {nextSteps.map((item) => (
            <li key={item} className="flex gap-3">
              <span className="mt-2 h-2 w-2 shrink-0 rounded-full bg-indigo-500" />
              {item}
            </li>
          ))}
        </ul>
      </section>
    </div>
  );
}
