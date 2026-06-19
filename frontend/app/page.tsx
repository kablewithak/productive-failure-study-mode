import Link from "next/link";
import { PageHeader } from "@/components/page-header";

const steps = [
  "Choose a concept from law, commerce, engineering, or programming.",
  "Attempt the challenge before the full explanation appears.",
  "Receive structured failure analysis and targeted consolidation.",
  "Complete retrieval questions and review the learning-event dashboard.",
];

export default function HomePage() {
  return (
    <div className="space-y-8">
      <section className="rounded-3xl border border-slate-200 bg-white p-8 shadow-panel">
        <p className="mb-4 text-sm font-semibold uppercase tracking-[0.2em] text-indigo-600">
          Productive Failure study mode
        </p>
        <h1 className="max-w-4xl text-4xl font-bold tracking-tight text-slate-950 md:text-6xl">
          Make the student try before the AI explains.
        </h1>
        <p className="mt-5 max-w-3xl text-lg leading-8 text-slate-600">
          This prototype turns an AI study companion into a learning-behaviour engine: attempt first,
          fail safely, consolidate precisely, practise retrieval, then measure the learning event.
        </p>
        <div className="mt-8 flex flex-wrap gap-3">
          <Link href="/learn" className="rounded-full bg-slate-950 px-5 py-3 text-sm font-semibold text-white hover:bg-slate-800">
            Start a learning session
          </Link>
          <Link href="/about" className="rounded-full border border-slate-300 px-5 py-3 text-sm font-semibold text-slate-700 hover:bg-slate-100">
            Read the product rationale
          </Link>
        </div>
      </section>

      <section className="grid gap-4 md:grid-cols-4">
        {steps.map((step, index) => (
          <div key={step} className="rounded-2xl border border-slate-200 bg-white p-5">
            <div className="mb-4 flex h-10 w-10 items-center justify-center rounded-full bg-indigo-50 text-sm font-bold text-indigo-700">
              {index + 1}
            </div>
            <p className="text-sm leading-6 text-slate-700">{step}</p>
          </div>
        ))}
      </section>

      <section className="rounded-3xl border border-amber-200 bg-amber-50 p-6">
        <PageHeader
          eyebrow="Boundary"
          title="This is learning support, not assignment completion."
          description="The system deliberately withholds full explanations until an attempt exists. The prototype stores demo learning events only and does not claim real learning outcomes."
        />
      </section>
    </div>
  );
}
