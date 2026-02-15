export interface User {
  uid: string;
  email: string | null;
  displayName: string | null;
}

export interface DashboardData {
  feedback_score: number;
  mcq_score: number;
  mcq_total: number;
  career_match: number;
  career_suggestions: string;
  resume_summary: string;
  resume_feedback: string;
  display_name: string;
}

export interface MCQQuestion {
  question: string;
  options: string[];
  correct_answer: number;
  explanation: string;
}

export interface AnswerDetail {
  question: string;
  options: string[];
  user_answer: number;
  correct_answer: number;
  is_correct: boolean;
  explanation: string;
}

export interface InterviewResult {
  score: number;
  total: number;
  percentage: number;
  details: AnswerDetail[];
}

export interface FeedbackResult {
  score: number;
  feedback: string;
  strengths: string[];
  weaknesses: string[];
  suggestions: string[];
  score_reasons: string[];
}
