"use client";

import { useEffect, useMemo, useState } from "react";
import { useParams } from "next/navigation";
import { ErrorBox } from "@/components/error-box";
import { LoadingPanel } from "@/components/loading-panel";
import { PageHeader } from "@/components/page-header";
import { getSessionTrace, submitAttempt, submitQuiz } from "@/lib/api";
import { labelize } from "@/lib/format";
import type { QuizQuestion, SessionTraceResponse, SourceReference } from "@/lib/types";

export default function SessionPage() {
  const params = useParams<{ id: string }>();
  const sessionId = Array.isArray(params.id) ? params.id[0] : params.id;

  const [trace, setTrace] = useState<SessionTraceResponse | null>(null);
  const [attemptText, setAttemptText] = useState("");
  const [confidenceScore, setConfidenceScore] = useState(2);
  const [confusionNote, setConfusionNote] = useState("");
  const [quizAnswers, setQuizAnswers] = useState<Record<string, string>>({});
  const [loading, setLoading] = useState(true);
  const [submittingAttempt, setSubmittingAttempt] = useState(false);
  const [submittingQuiz, setSubmittingQuiz] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!sessionId) {
      return;
    }
    getSessionTrace(sessionId)
      .then(setTrace)
      .catch((issue: unknown) => setError(issue instanceof Error ? issue.message : "Could not load the session."))
      .finally(() => setLoading(false));
  }, [sessionId]);

  const questions = useMemo(() => trace?.retrieval_quiz?.questions ?? [], [trace]);

  async function refreshTrace() {
    const refreshedTrace = await getSessionTrace(sessionId);
    setTrace(refreshedTrace);
  }

  async function handleAttemptSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setSubmittingAttempt(true);
    setError(null);
    try {
      await submitAttempt({ sessionId, attemptText, confidenceScore, confusionNote });
      await refreshTrace();
    } catch (issue) {
      setError(issue instanceof Error ? issue.message : "Could not submit the attempt.");
    } finally {
      setSubmittingAttempt(false);
    }
  }

  async function handleQuizSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setSubmittingQuiz(true);
    setError(null);
    try {
      await submitQuiz({
        sessionId,
        answers: questions.map((question) => ({
          question_id: question.question_id,
          answer_text: quizAnswers[question.question_id] ?? "",
        })),
      });
      await refreshTrace();
    } catch (issue) {
      setError(issue instanceof Error ? issue.message : "Could not submit the quiz.");
    } finally {
      setSubmittingQuiz(false);
    }
  }

  if (loading) {
    return <LoadingPanel />;
  }

  if (!trace) {
    return <ErrorBox message={error ?? "No session trace was returned by the API."} />;
  }

  return (
    <div className="space-y-8">
      <PageHeader
        eyebrow="Learning session"
        title={trace.concept.title}
        description={trace.concept.learning_outcome}
      />

      {error ? <ErrorBox message={error} /> : null}

      <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-panel">
        <div className="flex flex-wrap gap-2">
          <span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-semibold text-slate-700">
            {trace.concept.discipline}
          </span>
          <span className="rounded-full bg-indigo-50 px-3 py-1 text-xs font-semibold text-indigo-700">
            {labelize(trace.challenge.challenge_type)}
          </span>
          <span className="rounded-full bg-emerald-50 px-3 py-1 text-xs font-semibold text-emerald-700">
            Status: {labelize(trace.session.status)}
          </span>
          <span className="rounded-full bg-amber-50 px-3 py-1 text-xs font-semibold text-amber-800">
            Source: {trace.concept.source_citation_label}
          </span>
        </div>
        <h2 className="mt-5 text-lg font-semibold text-slate-950">Pre-instruction challenge</h2>
        <p className="mt-3 leading-7 text-slate-700">{trace.challenge.challenge_prompt}</p>
        <SourceBox source={trace.challenge.source} />
      </section>

      {!trace.attempt ? (
        <form onSubmit={handleAttemptSubmit} className="rounded-2xl border border-slate-200 bg-white p-6 shadow-panel">
          <h2 className="text-lg font-semibold text-slate-950">Your attempt</h2>
          <p className="mt-2 text-sm leading-6 text-slate-600">
            The full explanation is intentionally hidden until you make a meaningful attempt. Your answer will be checked
            against source-backed rubric items, not a generic chat response.
          </p>
          <textarea
            value={attemptText}
            onChange={(event) => setAttemptText(event.target.value)}
            minLength={10}
            required
            rows={7}
            className="mt-5 w-full rounded-2xl border border-slate-300 bg-white p-4 text-sm outline-none ring-indigo-600 focus:ring-2"
            placeholder="Write your reasoning, even if you are unsure."
          />
          <div className="mt-5 grid gap-4 md:grid-cols-2">
            <label className="text-sm font-medium text-slate-700">
              Confidence: {confidenceScore} / 5
              <input
                type="range"
                min="1"
                max="5"
                value={confidenceScore}
                onChange={(event) => setConfidenceScore(Number(event.target.value))}
                className="mt-3 w-full"
              />
            </label>
            <label className="text-sm font-medium text-slate-700">
              Confusion note
              <input
                value={confusionNote}
                onChange={(event) => setConfusionNote(event.target.value)}
                className="mt-3 w-full rounded-xl border border-slate-300 p-3 text-sm outline-none ring-indigo-600 focus:ring-2"
                placeholder="What part feels unclear?"
              />
            </label>
          </div>
          <button
            type="submit"
            disabled={submittingAttempt}
            className="mt-6 rounded-full bg-slate-950 px-5 py-3 text-sm font-semibold text-white hover:bg-slate-800 disabled:cursor-not-allowed disabled:bg-slate-400"
          >
            {submittingAttempt ? "Analyzing attempt..." : "Submit attempt"}
          </button>
        </form>
      ) : null}

      {trace.failure_analysis ? (
        <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-panel">
          <h2 className="text-lg font-semibold text-slate-950">Failure analysis</h2>
          <div className="mt-4 grid gap-4 md:grid-cols-3">
            <Metric label="Failure label" value={labelize(trace.failure_analysis.failure_label)} />
            <Metric label="Productive failure score" value={`${trace.failure_analysis.productive_failure_score} / 5`} />
            <Metric label="Source" value={trace.failure_analysis.source.citation_label} />
          </div>
          <p className="mt-5 leading-7 text-slate-700">{trace.failure_analysis.misconception_summary}</p>
          <p className="mt-3 text-sm leading-6 text-slate-600">
            <span className="font-semibold text-slate-950">Missing concept: </span>
            {trace.failure_analysis.missing_concept}
          </p>
          <div className="mt-5 grid gap-4 md:grid-cols-2">
            <ListPanel title="Rubric items detected" items={trace.failure_analysis.matched_rubric_items} />
            <ListPanel title="Rubric gaps to fix" items={trace.failure_analysis.missing_rubric_items} />
          </div>
        </section>
      ) : null}

      {trace.consolidation ? (
        <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-panel">
          <h2 className="text-lg font-semibold text-slate-950">Targeted consolidation</h2>
          <p className="mt-3 leading-7 text-slate-700">{trace.consolidation.acknowledgement}</p>
          <div className="mt-5 grid gap-4 md:grid-cols-2">
            <ListPanel title="What was useful" items={trace.consolidation.what_was_useful} />
            <ListPanel title="Missing or confused" items={trace.consolidation.missing_or_confused} />
          </div>
          <div className="mt-5 rounded-xl bg-slate-50 p-4 leading-7 text-slate-700">{trace.consolidation.explanation}</div>
          <div className="mt-4 rounded-xl bg-indigo-50 p-4 leading-7 text-indigo-950">
            <span className="font-semibold">Worked example: </span>
            {trace.consolidation.worked_example}
          </div>
          <div className="mt-4 rounded-xl bg-amber-50 p-4 leading-7 text-amber-950">
            <span className="font-semibold">Immediate retrieval prompt: </span>
            {trace.consolidation.immediate_retrieval_prompt}
          </div>
          <SourceBox source={trace.consolidation.source} />
        </section>
      ) : null}

      {trace.retrieval_quiz && !trace.quiz_result ? (
        <form onSubmit={handleQuizSubmit} className="rounded-2xl border border-slate-200 bg-white p-6 shadow-panel">
          <h2 className="text-lg font-semibold text-slate-950">Retrieval quiz</h2>
          <p className="mt-2 text-sm leading-6 text-slate-600">
            The answer key remains hidden until submission. The questions come from the same sample source pack.
          </p>
          <SourceBox source={trace.retrieval_quiz.source} />
          <div className="mt-5 space-y-5">
            {trace.retrieval_quiz.questions.map((question, index) => (
              <QuestionAnswer
                key={question.question_id}
                index={index}
                question={question}
                value={quizAnswers[question.question_id] ?? ""}
                onChange={(value) => setQuizAnswers((current) => ({ ...current, [question.question_id]: value }))}
              />
            ))}
          </div>
          <button
            type="submit"
            disabled={submittingQuiz || questions.some((question) => !quizAnswers[question.question_id]?.trim())}
            className="mt-6 rounded-full bg-slate-950 px-5 py-3 text-sm font-semibold text-white hover:bg-slate-800 disabled:cursor-not-allowed disabled:bg-slate-400"
          >
            {submittingQuiz ? "Scoring quiz..." : "Submit quiz"}
          </button>
        </form>
      ) : null}

      {trace.quiz_result ? (
        <section className="rounded-2xl border border-emerald-200 bg-emerald-50 p-6 shadow-panel">
          <h2 className="text-lg font-semibold text-emerald-950">Quiz result</h2>
          <div className="mt-4 grid gap-4 md:grid-cols-2">
            <Metric label="Score" value={`${Math.round(trace.quiz_result.score * 100)}%`} />
            <Metric label="Mastery estimate" value={labelize(trace.quiz_result.mastery_estimate)} />
          </div>
          <ul className="mt-5 space-y-2 text-sm leading-6 text-emerald-950">
            {trace.quiz_result.feedback.map((item) => (
              <li key={item}>• {item}</li>
            ))}
          </ul>
          <p className="mt-4 leading-7 text-emerald-950">
            <span className="font-semibold">Recommended next step: </span>
            {trace.quiz_result.recommended_next_step}
          </p>
        </section>
      ) : null}
    </div>
  );
}

function SourceBox({ source }: { source: SourceReference }) {
  return (
    <div className="mt-5 rounded-xl border border-amber-200 bg-amber-50 p-4 text-sm leading-6 text-amber-950">
      <p className="font-semibold">Source used: {source.title}</p>
      <p className="mt-1 text-xs font-semibold uppercase tracking-wide text-amber-700">{source.citation_label}</p>
      <p className="mt-2">{source.excerpt}</p>
    </div>
  );
}

function Metric({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-xl bg-slate-50 p-4">
      <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">{label}</p>
      <p className="mt-2 text-sm font-semibold text-slate-950">{value}</p>
    </div>
  );
}

function ListPanel({ title, items }: { title: string; items: string[] }) {
  return (
    <div className="rounded-xl bg-slate-50 p-4">
      <h3 className="text-sm font-semibold text-slate-950">{title}</h3>
      <ul className="mt-3 space-y-2 text-sm leading-6 text-slate-700">
        {items.length > 0 ? items.map((item) => <li key={item}>• {item}</li>) : <li>• No major gap detected.</li>}
      </ul>
    </div>
  );
}

function QuestionAnswer({
  index,
  question,
  value,
  onChange,
}: {
  index: number;
  question: QuizQuestion;
  value: string;
  onChange: (value: string) => void;
}) {
  return (
    <label className="block rounded-xl border border-slate-200 bg-slate-50 p-4">
      <span className="text-xs font-semibold uppercase tracking-wide text-indigo-700">
        Question {index + 1} · {labelize(question.question_type)}
      </span>
      <span className="mt-2 block leading-7 text-slate-800">{question.question_text}</span>
      {question.source_citation_label ? (
        <span className="mt-2 block text-xs font-semibold text-slate-500">Source: {question.source_citation_label}</span>
      ) : null}
      <textarea
        value={value}
        onChange={(event) => onChange(event.target.value)}
        required
        rows={3}
        className="mt-4 w-full rounded-xl border border-slate-300 bg-white p-3 text-sm outline-none ring-indigo-600 focus:ring-2"
        placeholder="Answer from memory."
      />
    </label>
  );
}
