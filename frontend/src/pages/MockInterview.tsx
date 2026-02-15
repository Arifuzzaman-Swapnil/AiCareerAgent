import { useState, useEffect } from 'react';
import FileUpload from '../components/FileUpload';
import { generateInterviewQuestions, getExistingQuestions, submitInterview } from '../services/api';
import type { MCQQuestion, InterviewResult } from '../types';
import toast from 'react-hot-toast';

export default function MockInterview() {
  const [file, setFile] = useState<File | null>(null);
  const [questions, setQuestions] = useState<MCQQuestion[]>([]);
  const [answers, setAnswers] = useState<number[]>([]);
  const [result, setResult] = useState<InterviewResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [startTime] = useState(new Date());
  const [elapsed, setElapsed] = useState('00:00:00');

  useEffect(() => {
    getExistingQuestions().then(res => {
      if (res.data.questions && res.data.questions.length > 0) {
        setQuestions(res.data.questions);
        setAnswers(new Array(res.data.questions.length).fill(-1));
      }
    }).catch(() => {});
  }, []);

  useEffect(() => {
    if (questions.length === 0 || result) return;
    const timer = setInterval(() => {
      const now = new Date();
      const diff = Math.floor((now.getTime() - startTime.getTime()) / 1000);
      const h = Math.floor(diff / 3600).toString().padStart(2, '0');
      const m = Math.floor((diff % 3600) / 60).toString().padStart(2, '0');
      const s = (diff % 60).toString().padStart(2, '0');
      setElapsed(`${h}:${m}:${s}`);
    }, 1000);
    return () => clearInterval(timer);
  }, [questions.length, result, startTime]);

  const handleGenerate = async () => {
    if (!file) { toast.error('Please select a PDF file'); return; }
    setLoading(true);
    try {
      const res = await generateInterviewQuestions(file);
      setQuestions(res.data.questions);
      setAnswers(new Array(res.data.questions.length).fill(-1));
      setResult(null);
      toast.success(`${res.data.total_questions} questions generated!`);
    } catch (err: any) {
      toast.error(err?.response?.data?.error || 'Failed to generate questions');
    } finally {
      setLoading(false);
    }
  };

  const selectAnswer = (qIndex: number, optionIndex: number) => {
    if (result) return;
    const newAnswers = [...answers];
    newAnswers[qIndex] = optionIndex;
    setAnswers(newAnswers);
  };

  const handleSubmit = async () => {
    setSubmitting(true);
    try {
      const res = await submitInterview(answers);
      setResult(res.data);
      toast.success('Interview submitted!');
    } catch (err: any) {
      toast.error(err?.response?.data?.error || 'Submission failed');
    } finally {
      setSubmitting(false);
    }
  };

  const answeredCount = answers.filter(a => a !== -1).length;

  return (
    <div className="interview-page">
      <div className="interview-sidebar">
        <h3>📊 Progress</h3>
        <div className="sidebar-score">
          <div className="sidebar-score-number">{answeredCount}</div>
          <div>of {questions.length || '—'} Answered</div>
          <div className="progress-bar">
            <div className="progress-fill" style={{ width: `${questions.length > 0 ? (answeredCount / questions.length) * 100 : 0}%` }} />
          </div>
        </div>
        <div className="sidebar-timer">⏱ {elapsed}</div>
      </div>

      <div className="interview-main">
        <div className="content-card">
          <div className="page-header-section">
            <div className="page-icon">🎯</div>
            <h1>Mock Interview</h1>
            <p className="page-subtitle">Upload your resume and get 30 technical MCQ questions</p>
          </div>

          {questions.length === 0 && (
            <div className="upload-section-interview">
              {loading ? (
                <div className="loading-overlay">
                  <div className="loading-spinner-ring" />
                  <div className="loading-text">Generating 30 MCQ questions...</div>
                </div>
              ) : (
                <>
                  <h3>📄 Upload Your Resume</h3>
                  <p>Upload your PDF resume to generate personalized technical questions</p>
                  <FileUpload onFileSelect={setFile} label="" />
                  <button onClick={handleGenerate} className="submit-btn" disabled={loading || !file}>
                    🚀 Generate 30 MCQ Questions
                  </button>
                </>
              )}
            </div>
          )}

          {questions.length > 0 && !result && (
            <>
              <h2 className="section-heading">📝 Technical MCQ Questions ({questions.length} Questions)</h2>
              {questions.map((q, qIdx) => (
                <div key={qIdx} className="question-container" style={{ animationDelay: `${qIdx * 0.05}s` }}>
                  <div className="question-number">Question {qIdx + 1}</div>
                  <div className="question-text">{q.question}</div>
                  <div className="options-container">
                    {q.options.map((opt, optIdx) => (
                      <label
                        key={optIdx}
                        className={`option ${answers[qIdx] === optIdx ? 'selected' : ''}`}
                        onClick={() => selectAnswer(qIdx, optIdx)}
                      >
                        <input type="radio" name={`q${qIdx}`} checked={answers[qIdx] === optIdx} readOnly />
                        <span>{opt}</span>
                      </label>
                    ))}
                  </div>
                </div>
              ))}
              <div className="submit-section-center">
                <button onClick={handleSubmit} className="submit-btn" disabled={submitting}>
                  {submitting ? 'Processing...' : '🚀 Submit Interview'}
                </button>
              </div>
            </>
          )}

          {result && (
            <div className="results-section">
              <div className="results-header-block">
                <div className="final-score">{result.score}/{result.total}</div>
                <h3>🎉 Interview Complete!</h3>
              </div>
              <div className="score-breakdown">
                <div className="score-item"><div className="score-item-number">{result.score}</div><div>Correct</div></div>
                <div className="score-item"><div className="score-item-number">{result.total}</div><div>Total</div></div>
                <div className="score-item"><div className="score-item-number">{Math.round(result.percentage)}%</div><div>Score</div></div>
              </div>
              <div className="results-details">
                <h4>Detailed Results:</h4>
                {result.details.map((d, i) => (
                  <div key={i} className={`result-item ${d.is_correct ? 'correct' : 'incorrect'}`}>
                    <strong>{d.is_correct ? '✅' : '❌'} Question {i + 1}:</strong> {d.question}<br />
                    <strong>Your Answer:</strong> {d.user_answer >= 0 && d.options ? d.options[d.user_answer] : 'Not answered'}<br />
                    <strong>Correct Answer:</strong> {d.options ? d.options[d.correct_answer] : ''}<br />
                    {d.explanation && <><strong>Explanation:</strong> {d.explanation}</>}
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
