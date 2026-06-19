export type ChallengeType =
  | "scenario_analysis"
  | "calculation_attempt"
  | "concept_explanation"
  | "case_application"
  | "compare_and_contrast"
  | "diagnose_error"
  | "short_problem_solving";

export type FailureLabel =
  | "missing_core_concept"
  | "misapplied_rule_or_formula"
  | "wrong_representation"
  | "unsupported_guess"
  | "surface_level_answer"
  | "partial_prior_knowledge"
  | "confuses_similar_concepts"
  | "calculation_without_reasoning"
  | "correct_but_incomplete"
  | "strong_attempt";

export type SessionStatus = "created" | "attempt_submitted" | "consolidated" | "quiz_completed" | "abandoned";
export type QuestionType = "short_answer" | "multiple_choice" | "scenario_transfer" | "calculation";
export type MasteryEstimate = "needs_review" | "developing" | "almost_there" | "secure";

export interface SourceReference {
  source_id: string;
  title: string;
  citation_label: string;
  excerpt: string;
}

export interface RubricItem {
  rubric_item_id: string;
  criterion: string;
  expected_markers: string[];
  feedback_if_missing: string;
  weight: number;
}

export interface GroundedRetrievalSeed {
  question_id: string;
  question_text: string;
  question_type: QuestionType;
  expected_answer: string;
  scoring_guidance: string;
}

export interface Concept {
  concept_id: string;
  title: string;
  discipline: string;
  module_context: string;
  learning_outcome: string;
  prerequisite_knowledge: string[];
  challenge_type: ChallengeType;
  challenge_prompt: string;
  expected_reasoning_steps: string[];
  common_misconceptions: string[];
  canonical_explanation: string;
  retrieval_question_seeds: string[];
  canonical_answer: string;
  worked_example: string;
  source: SourceReference;
  rubric_items: RubricItem[];
  retrieval_questions: GroundedRetrievalSeed[];
}

export interface ConceptSummary {
  concept_id: string;
  title: string;
  discipline: string;
  module_context: string;
  learning_outcome: string;
  challenge_type: ChallengeType;
  source_title: string;
  source_citation_label: string;
}

export interface ChallengePreview {
  concept_id: string;
  challenge_type: ChallengeType;
  challenge_prompt: string;
  source: SourceReference;
}

export interface CreateSessionResponse {
  session_id: string;
  concept: ConceptSummary;
  challenge: ChallengePreview;
}

export interface LearningSession {
  session_id: string;
  concept_id: string;
  student_alias: string | null;
  status: SessionStatus;
  created_at: string;
  updated_at: string;
}

export interface StudentAttempt {
  attempt_id: string;
  session_id: string;
  attempt_text: string;
  confidence_score: number;
  confusion_note: string | null;
  created_at: string;
}

export interface FailureAnalysis {
  analysis_id: string;
  attempt_id: string;
  failure_label: FailureLabel;
  prior_knowledge_detected: string[];
  missing_concept: string;
  misconception_summary: string;
  productive_failure_score: number;
  feedback_strategy: string;
  should_consolidate: boolean;
  source: SourceReference;
  matched_rubric_items: string[];
  missing_rubric_items: string[];
  created_at: string;
}

export interface ConsolidationResponse {
  response_id: string;
  analysis_id: string;
  acknowledgement: string;
  what_was_useful: string[];
  missing_or_confused: string[];
  explanation: string;
  worked_example: string;
  immediate_retrieval_prompt: string;
  source: SourceReference;
  created_at: string;
}

export interface QuizQuestion {
  question_id: string;
  question_text: string;
  question_type: QuestionType;
  options: string[] | null;
  source_citation_label: string | null;
}

export interface RetrievalQuiz {
  quiz_id: string;
  session_id: string;
  questions: QuizQuestion[];
  source: SourceReference;
  created_at: string;
}

export interface SubmitAttemptResponse {
  attempt_id: string;
  failure_analysis: FailureAnalysis;
  consolidation: ConsolidationResponse;
  retrieval_quiz: RetrievalQuiz;
}

export interface QuizResultFeedback {
  result_id: string;
  quiz_id: string;
  session_id: string;
  score: number;
  feedback: string[];
  mastery_estimate: MasteryEstimate;
  recommended_next_step: string;
  created_at: string;
}

export interface SessionTraceResponse {
  session: LearningSession;
  concept: ConceptSummary;
  challenge: ChallengePreview;
  attempt: StudentAttempt | null;
  failure_analysis: FailureAnalysis | null;
  consolidation: ConsolidationResponse | null;
  retrieval_quiz: RetrievalQuiz | null;
  quiz_result: QuizResultFeedback | null;
}

export interface DashboardMetricsResponse {
  total_sessions: number;
  completed_sessions: number;
  average_confidence_score: number | null;
  average_quiz_score: number | null;
  failure_label_distribution: Array<{ failure_label: FailureLabel; count: number }>;
  recent_learning_events: Array<{
    session_id: string;
    concept_id: string;
    concept_title: string;
    discipline: string;
    status: SessionStatus;
    failure_label: FailureLabel | null;
    confidence_score: number | null;
    quiz_score: number | null;
    created_at: string;
    updated_at: string;
  }>;
  concepts_attempted: Array<{
    concept_id: string;
    title: string;
    discipline: string;
    attempt_count: number;
  }>;
}
