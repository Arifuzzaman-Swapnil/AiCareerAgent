import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { getDashboard } from '../services/api';
import type { DashboardData } from '../types';

export default function Dashboard() {
  const [data, setData] = useState<DashboardData | null>(null);
  const [activeFeature, setActiveFeature] = useState(0);
  const [heroVisible, setHeroVisible] = useState(false);

  const features = [
    { title: 'Career Guidance', desc: 'AI-powered career path recommendations tailored to your unique skills and aspirations', icon: '🎯', color: '#6366f1' },
    { title: 'Resume Analysis', desc: 'Deep analysis with scoring, feedback, and actionable improvement suggestions', icon: '📄', color: '#8b5cf6' },
    { title: 'Interview Prep', desc: 'Smart MCQ generation from your resume with detailed performance tracking', icon: '🎤', color: '#06b6d4' },
    { title: 'Skill Insights', desc: 'Track your career readiness and identify areas for growth', icon: '📊', color: '#ec4899' },
  ];

  useEffect(() => {
    getDashboard().then(res => setData(res.data.data)).catch(() => {});
    setHeroVisible(true);
    const interval = setInterval(() => setActiveFeature(prev => (prev + 1) % features.length), 4000);
    return () => clearInterval(interval);
  }, []);

  const tools = [
    { path: '/career', icon: '🎯', title: 'Career Counsellor', desc: 'Get AI-powered career suggestions based on your skills, experience, and interests.', badge: 'AI Powered' },
    { path: '/summarizer', icon: '📝', title: 'Resume Summarizer', desc: 'Extract key insights and highlights from your resume instantly.', badge: 'Smart' },
    { path: '/feedback', icon: '📊', title: 'Resume Feedback', desc: 'Get expert analysis with a detailed score and improvement tips.', badge: 'Expert' },
    { path: '/interview-prep', icon: '📋', title: 'Interview Prep', desc: 'Upload your resume and get a customized interview preparation guide.', badge: 'Personalized' },
    { path: '/interview', icon: '🎤', title: 'Mock Interview', desc: 'Practice with 30 MCQ questions generated from your resume.', badge: 'Practice' },
    { path: '/summarizer', icon: '📄', title: 'Resume Builder', desc: 'Create professional resumes with AI-powered assistance.', badge: 'Coming Soon' },
  ];

  return (
    <div className="dashboard-page">
      {/* Stats */}
      <div className="stats-grid">
        <div className="stat-card" style={{ borderTop: '2px solid #6366f1' }}>
          <div className="stat-icon">📊</div>
          <div className="stat-value">{data?.feedback_score || '—'}</div>
          <div className="stat-label">Resume Score</div>
        </div>
        <div className="stat-card" style={{ borderTop: '2px solid #8b5cf6' }}>
          <div className="stat-icon">🎯</div>
          <div className="stat-value">{data ? `${data.mcq_score || 0}/${data.mcq_total || 0}` : '—'}</div>
          <div className="stat-label">MCQ Score</div>
        </div>
        <div className="stat-card" style={{ borderTop: '2px solid #06b6d4' }}>
          <div className="stat-icon">💡</div>
          <div className="stat-value">{data?.career_match ? `${data.career_match}%` : '—'}</div>
          <div className="stat-label">Career Match</div>
        </div>
        <div className="stat-card" style={{ borderTop: '2px solid #10b981' }}>
          <div className="stat-icon">👤</div>
          <div className="stat-value">{data?.display_name?.split(' ')[0] || 'User'}</div>
          <div className="stat-label">Welcome Back</div>
        </div>
      </div>

      {/* Premium Hero Section */}
      <section className={`hero-section ${heroVisible ? 'hero-visible' : ''}`}>
        <div className="hero-content hero-premium">
          {/* Animated background elements */}
          <div className="hero-bg-grid" />
          <div className="hero-glow hero-glow-1" />
          <div className="hero-glow hero-glow-2" />
          <div className="hero-glow hero-glow-3" />

          {/* Floating particles */}
          <div className="hero-particles">
            {Array.from({ length: 20 }).map((_, i) => (
              <div key={i} className="hero-particle" style={{
                left: `${Math.random() * 100}%`,
                top: `${Math.random() * 100}%`,
                animationDelay: `${Math.random() * 5}s`,
                animationDuration: `${3 + Math.random() * 4}s`,
                width: `${2 + Math.random() * 3}px`,
                height: `${2 + Math.random() * 3}px`,
              }} />
            ))}
          </div>

          {/* Badge */}
          <div className="hero-badge">
            <span className="hero-badge-dot" />
            AI-Powered Career Platform
          </div>

          {/* Title with animated gradient */}
          <h1 className="hero-title hero-title-animated">
            Your Career,
            <br />
            <span className="hero-title-highlight">Supercharged.</span>
          </h1>

          <p className="hero-subtitle">
            Intelligent career guidance, resume optimization, and interview preparation — all powered by AI to help you land your dream role.
          </p>

          {/* CTA Buttons */}
          <div className="hero-cta-group">
            <Link to="/career" className="hero-cta-primary">
              Get Started
              <svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M3 8h10M9 4l4 4-4 4" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/></svg>
            </Link>
            <Link to="/feedback" className="hero-cta-secondary">
              Analyze Resume
            </Link>
          </div>

          {/* Animated Feature Cards */}
          <div className="hero-features-grid">
            {features.map((f, i) => (
              <div
                key={i}
                className={`hero-feature-card ${i === activeFeature ? 'hero-feature-active' : ''}`}
                onClick={() => setActiveFeature(i)}
                style={{ '--feature-color': f.color } as React.CSSProperties}
              >
                <div className="hero-feature-icon">{f.icon}</div>
                <div className="hero-feature-info">
                  <div className="hero-feature-title">{f.title}</div>
                  <div className={`hero-feature-desc ${i === activeFeature ? 'hero-feature-desc-visible' : ''}`}>
                    {f.desc}
                  </div>
                </div>
                <div className="hero-feature-indicator" />
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Services */}
      <section className="tools-section">
        <h2 className="section-title">Our Services</h2>
        <div className="tools-grid">
          {tools.map((tool, i) => (
            <Link key={tool.path + tool.title} to={tool.path} className="tool-card" style={{ animationDelay: `${i * 0.06}s` }}>
              <div className="tool-badge">{tool.badge}</div>
              <div className="tool-icon">{tool.icon}</div>
              <h3 className="tool-title">{tool.title}</h3>
              <p className="tool-description">{tool.desc}</p>
            </Link>
          ))}
        </div>
      </section>
    </div>
  );
}
