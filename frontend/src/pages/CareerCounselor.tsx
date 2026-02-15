import { useState, type FormEvent } from 'react';
import { getCareerSuggestions } from '../services/api';
import toast from 'react-hot-toast';

export default function CareerCounselor() {
  const [resumeText, setResumeText] = useState('');
  const [suggestion, setSuggestion] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (!resumeText.trim()) { toast.error('Please enter your resume text'); return; }
    setLoading(true);
    try {
      const res = await getCareerSuggestions(resumeText);
      setSuggestion(res.data.suggestion);
      toast.success('Career suggestions generated!');
    } catch (err: any) {
      toast.error(err?.response?.data?.error || 'Failed to get suggestions');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page-container">
      <div className="content-card">
        <div className="page-header-section">
          <div className="page-icon">🎯</div>
          <h1>Career Counsellor</h1>
          <p className="page-subtitle">Discover your ideal career path with AI-powered guidance</p>
        </div>

        {loading ? (
          <div className="loading-overlay">
            <div className="loading-spinner-ring" />
            <div className="loading-text">Analyzing your profile...</div>
          </div>
        ) : (
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label className="form-label">Paste your resume or describe your skills:</label>
              <textarea
                className="form-textarea"
                value={resumeText}
                onChange={e => setResumeText(e.target.value)}
                required
                placeholder="Enter your education, experience, skills, and interests here..."
                rows={8}
              />
            </div>
            <button type="submit" className="submit-btn" disabled={loading}>
              🎯 Get Career Suggestions
            </button>
          </form>
        )}

        {suggestion && (
          <div className="output-section">
            <h3>🎯 Suggested Career Paths</h3>
            <div className="output-content">{suggestion}</div>
          </div>
        )}
      </div>
    </div>
  );
}
