import { useState } from 'react';
import FileUpload from '../components/FileUpload';
import { getResumeFeedback } from '../services/api';
import type { FeedbackResult } from '../types';
import toast from 'react-hot-toast';

export default function ResumeFeedback() {
  const [file, setFile] = useState<File | null>(null);
  const [result, setResult] = useState<FeedbackResult | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    if (!file) { toast.error('Please select a PDF file'); return; }
    setLoading(true);
    try {
      const res = await getResumeFeedback(file);
      setResult(res.data);
      toast.success('Feedback generated!');
    } catch (err: any) {
      toast.error(err?.response?.data?.error || 'Feedback generation failed');
    } finally {
      setLoading(false);
    }
  };

  const scoreOffset = result ? 283 - (283 * result.score) / 100 : 283;

  return (
    <div className="page-container">
      <div className="content-card">
        <div className="page-header-section">
          <div className="page-icon">💡</div>
          <h1>Resume Feedback</h1>
          <p className="page-subtitle">Get expert analysis and improvement suggestions for your resume</p>
        </div>

        {loading ? (
          <div className="loading-overlay">
            <div className="loading-spinner-ring" />
            <div className="loading-text">Analyzing your resume...</div>
          </div>
        ) : (
          <>
            <FileUpload onFileSelect={setFile} label="Upload your PDF resume:" />
            <button onClick={handleSubmit} className="submit-btn" disabled={loading || !file}>
              📊 Generate Feedback
            </button>
          </>
        )}

        {result && (
          <div className="feedback-output">
            <div className="score-display">
              <svg width="0" height="0">
                <defs>
                  <linearGradient id="scoreGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stopColor="#667eea" />
                    <stop offset="100%" stopColor="#764ba2" />
                  </linearGradient>
                </defs>
              </svg>
              <div className="score-circle-wrapper">
                <svg className="score-circle-svg" viewBox="0 0 100 100">
                  <circle className="score-circle-bg" cx="50" cy="50" r="45" />
                  <circle
                    className="score-circle-progress"
                    cx="50" cy="50" r="45"
                    style={{ strokeDashoffset: scoreOffset, stroke: 'url(#scoreGradient)' }}
                  />
                </svg>
                <div className="score-circle-value">{result.score}</div>
              </div>
              <div className="score-text">Score: {result.score}/100</div>
            </div>

            <div className="feedback-section">
              <h3>💡 AI Feedback</h3>
              <div className="output-content">{result.feedback}</div>
            </div>

            {result.strengths.length > 0 && (
              <div className="feedback-list">
                <h4>✅ Strengths</h4>
                <ul>{result.strengths.map((s, i) => <li key={i}>{s}</li>)}</ul>
              </div>
            )}

            {result.weaknesses.length > 0 && (
              <div className="feedback-list">
                <h4>⚠️ Weaknesses</h4>
                <ul>{result.weaknesses.map((w, i) => <li key={i}>{w}</li>)}</ul>
              </div>
            )}

            {result.suggestions.length > 0 && (
              <div className="feedback-list">
                <h4>💡 Suggestions</h4>
                <ul>{result.suggestions.map((s, i) => <li key={i}>{s}</li>)}</ul>
              </div>
            )}

            {result.score_reasons.length > 0 && (
              <div className="feedback-list">
                <h4>📊 Score Breakdown</h4>
                <ul>{result.score_reasons.map((r, i) => <li key={i}>{r}</li>)}</ul>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
