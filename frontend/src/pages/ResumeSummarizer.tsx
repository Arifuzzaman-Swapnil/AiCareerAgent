import { useState } from 'react';
import FileUpload from '../components/FileUpload';
import { summarizeResume } from '../services/api';
import toast from 'react-hot-toast';

export default function ResumeSummarizer() {
  const [file, setFile] = useState<File | null>(null);
  const [summary, setSummary] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    if (!file) { toast.error('Please select a PDF file'); return; }
    setLoading(true);
    try {
      const res = await summarizeResume(file);
      setSummary(res.data.summary);
      toast.success('Resume summarized!');
    } catch (err: any) {
      toast.error(err?.response?.data?.error || 'Summarization failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page-container">
      <div className="content-card">
        <div className="page-header-section">
          <div className="page-icon">📝</div>
          <h1>Resume Summarizer</h1>
          <p className="page-subtitle">Extract key insights from your resume instantly</p>
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
              🔍 Summarize Resume
            </button>
          </>
        )}

        {summary && (
          <div className="output-section">
            <h3>📌 Resume Summary</h3>
            <div className="output-content">{summary}</div>
          </div>
        )}
      </div>
    </div>
  );
}
