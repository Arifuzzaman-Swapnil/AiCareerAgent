import { useState, useRef, type DragEvent, type ChangeEvent } from 'react';

interface FileUploadProps {
  onFileSelect: (file: File) => void;
  label?: string;
}

export default function FileUpload({ onFileSelect, label = 'PDF Resume Upload' }: FileUploadProps) {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isDragOver, setIsDragOver] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFile = (file: File) => {
    if (file.type !== 'application/pdf') {
      alert('Please select a PDF file only.');
      return;
    }
    if (file.size > 10 * 1024 * 1024) {
      alert('File size must be less than 10MB');
      return;
    }
    setSelectedFile(file);
    onFileSelect(file);
  };

  const handleDrop = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragOver(false);
    if (e.dataTransfer.files.length > 0) {
      handleFile(e.dataTransfer.files[0]);
    }
  };

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      handleFile(e.target.files[0]);
    }
  };

  return (
    <div className="file-upload-container">
      <label className="file-upload-label">{label}</label>
      <div
        className={`file-upload-area ${isDragOver ? 'dragover' : ''} ${selectedFile ? 'has-file' : ''}`}
        onDragOver={(e) => { e.preventDefault(); setIsDragOver(true); }}
        onDragLeave={() => setIsDragOver(false)}
        onDrop={handleDrop}
        onClick={() => fileInputRef.current?.click()}
      >
        <input
          type="file"
          ref={fileInputRef}
          accept=".pdf"
          onChange={handleChange}
          style={{ display: 'none' }}
        />
        {selectedFile ? (
          <>
            <span className="file-upload-icon">✅</span>
            <div className="file-upload-text">
              <span className="file-upload-main">{selectedFile.name}</span>
              <span className="file-upload-sub">Click to change file</span>
            </div>
          </>
        ) : (
          <>
            <span className="file-upload-icon">📁</span>
            <div className="file-upload-text">
              <span className="file-upload-main">Click to upload or drag and drop</span>
              <span className="file-upload-sub">PDF files only (Max 10MB)</span>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
