import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import { AuthProvider, useAuth } from './context/AuthContext';
import Layout from './components/Layout/Layout';
import ProtectedRoute from './components/ProtectedRoute';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import CareerCounselor from './pages/CareerCounselor';
import ResumeSummarizer from './pages/ResumeSummarizer';
import ResumeFeedback from './pages/ResumeFeedback';
import InterviewPrep from './pages/InterviewPrep';
import MockInterview from './pages/MockInterview';
import './index.css';

function AppRoutes() {
  const { user, loading } = useAuth();

  if (loading) {
    return (
      <div className="loading-screen">
        <div className="spinner" />
        <p>Loading...</p>
      </div>
    );
  }

  return (
    <Routes>
      <Route path="/" element={user ? <Navigate to="/dashboard" /> : <Login />} />
      <Route element={<ProtectedRoute><Layout /></ProtectedRoute>}>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/career" element={<CareerCounselor />} />
        <Route path="/summarizer" element={<ResumeSummarizer />} />
        <Route path="/feedback" element={<ResumeFeedback />} />
        <Route path="/interview-prep" element={<InterviewPrep />} />
        <Route path="/interview" element={<MockInterview />} />
      </Route>
    </Routes>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Toaster position="top-right" />
        <AppRoutes />
      </AuthProvider>
    </BrowserRouter>
  );
}
