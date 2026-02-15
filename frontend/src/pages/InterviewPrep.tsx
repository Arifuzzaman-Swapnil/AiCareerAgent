import { useState } from 'react';
import FileUpload from '../components/FileUpload';
import { getInterviewPrep } from '../services/api';
import toast from 'react-hot-toast';

export default function InterviewPrep() {
  const [file, setFile] = useState<File | null>(null);
  const [analysis, setAnalysis] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    if (!file) { toast.error('Please select a PDF file'); return; }
    setLoading(true);
    try {
      const res = await getInterviewPrep(file);
      setAnalysis(res.data.analysis);
      toast.success('Interview preparation guide generated!');
    } catch (err: any) {
      toast.error(err?.response?.data?.error || 'Interview prep failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page-container">
      <div className="content-card">
        <div className="page-header-section">
          <div className="page-icon">📋</div>
          <h1>Interview Preparation</h1>
          <p className="page-subtitle">Upload your resume and get a detailed interview preparation guide</p>
        </div>

        {loading ? (
          <div className="loading-overlay">
            <div className="loading-spinner-ring" />
            <div className="loading-text">Generating your interview prep guide...</div>
          </div>
        ) : (
          <>
            <FileUpload onFileSelect={setFile} label="Upload your PDF resume:" />
            <button onClick={handleSubmit} className="submit-btn" disabled={loading || !file}>
              📋 Generate Interview Prep Guide
            </button>
          </>
        )}

        {analysis && (
          <div className="output-section">
            <h3>📊 Interview Preparation Report</h3>
            <div className="output-content">{analysis}</div>
          </div>
        )}
      </div>
    </div>
  );
}
