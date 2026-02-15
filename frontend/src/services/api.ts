import axios from 'axios';

const api = axios.create({
  baseURL: '/api',
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Auth
export const loginToBackend = (idToken: string) =>
  api.post('/auth/login', { idToken });

export const logoutFromBackend = () =>
  api.post('/auth/logout');

export const checkAuthStatus = () =>
  api.get('/auth/status');

// Dashboard
export const getDashboard = () =>
  api.get('/dashboard');

// Career
export const getCareerSuggestions = (resume: string) =>
  api.post('/tools/career', { resume });

// Resume - these use FormData for file upload
export const summarizeResume = (file: File) => {
  const formData = new FormData();
  formData.append('resume_pdf', file);
  return api.post('/tools/resume/summarize', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
    timeout: 120000,
  });
};

export const getResumeFeedback = (file: File) => {
  const formData = new FormData();
  formData.append('resume_pdf', file);
  return api.post('/tools/resume/feedback', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
    timeout: 120000,
  });
};

// Interview
export const getInterviewPrep = (file: File) => {
  const formData = new FormData();
  formData.append('resume_pdf', file);
  return api.post('/tools/interview/prep', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
    timeout: 120000,
  });
};

export const generateInterviewQuestions = (file: File) => {
  const formData = new FormData();
  formData.append('resume_pdf', file);
  return api.post('/tools/interview/generate', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
    timeout: 120000,
  });
};

export const getExistingQuestions = () =>
  api.get('/tools/interview/questions');

export const submitInterview = (mcqAnswers: number[]) =>
  api.post('/tools/interview/submit', { mcq_answers: mcqAnswers });

export const getInterviewResults = () =>
  api.get('/tools/interview/results');

export default api;
