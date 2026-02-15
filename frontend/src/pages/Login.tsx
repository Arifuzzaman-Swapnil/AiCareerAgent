import { useState, type FormEvent } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import toast from 'react-hot-toast';

export default function Login() {
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [fullName, setFullName] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const { login, register } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (!isLogin && password !== confirmPassword) {
      toast.error('Passwords do not match');
      return;
    }
    if (!isLogin && password.length < 6) {
      toast.error('Password must be at least 6 characters');
      return;
    }
    setLoading(true);
    try {
      if (isLogin) {
        await login(email, password);
      } else {
        await register(email, password, fullName);
      }
      navigate('/dashboard');
    } catch (err: any) {
      const code = err?.code || '';
      if (code === 'auth/user-not-found') toast.error('No account found with this email');
      else if (code === 'auth/wrong-password') toast.error('Incorrect password');
      else if (code === 'auth/invalid-email') toast.error('Invalid email format');
      else if (code === 'auth/email-already-in-use') toast.error('Email already registered');
      else if (code === 'auth/weak-password') toast.error('Password is too weak');
      else if (code === 'auth/too-many-requests') toast.error('Too many attempts. Try later.');
      else toast.error(err?.message || 'Authentication failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-page">
      <div className="login-bg-shapes">
        <div className="login-bg-shape" />
        <div className="login-bg-shape" />
        <div className="login-bg-shape" />
      </div>

      <div className="login-branding">
        <div className="login-brand-icon">💼</div>
        <div className="login-brand-title">Career Assistant</div>
        <div className="login-brand-subtitle">
          AI-powered platform for career guidance, resume analysis, and interview preparation.
        </div>
        <div className="login-brand-features">
          <div className="login-brand-feature">
            <div className="login-brand-feature-icon">🎯</div>
            <span>Smart career path recommendations</span>
          </div>
          <div className="login-brand-feature">
            <div className="login-brand-feature-icon">📊</div>
            <span>Resume scoring & optimization tips</span>
          </div>
          <div className="login-brand-feature">
            <div className="login-brand-feature-icon">🎤</div>
            <span>30-question mock interview practice</span>
          </div>
          <div className="login-brand-feature">
            <div className="login-brand-feature-icon">💡</div>
            <span>Personalized interview preparation</span>
          </div>
        </div>
      </div>

      <div className="login-form-side">
        <div className="login-container">
          <div className="login-logo">💼</div>
          <h1>{isLogin ? 'Welcome back' : 'Create account'}</h1>
          <p className="login-subtitle">
            {isLogin ? 'Sign in to continue to your dashboard' : 'Get started with Career Assistant'}
          </p>

          <form onSubmit={handleSubmit}>
            {!isLogin && (
              <div className="input-group">
                <label>Full Name</label>
                <input type="text" value={fullName} onChange={e => setFullName(e.target.value)} placeholder="John Doe" required />
              </div>
            )}
            <div className="input-group">
              <label>Email</label>
              <input type="email" value={email} onChange={e => setEmail(e.target.value)} placeholder="you@example.com" required />
            </div>
            <div className="input-group">
              <label>Password</label>
              <input type="password" value={password} onChange={e => setPassword(e.target.value)} placeholder="Min. 6 characters" required />
            </div>
            {!isLogin && (
              <div className="input-group">
                <label>Confirm Password</label>
                <input type="password" value={confirmPassword} onChange={e => setConfirmPassword(e.target.value)} placeholder="Repeat password" required />
              </div>
            )}
            <button type="submit" className="login-btn" disabled={loading}>
              {loading ? (isLogin ? 'Signing in...' : 'Creating account...') : (isLogin ? 'Sign in' : 'Create account')}
            </button>
          </form>

          <div className="auth-toggle">
            <p>
              {isLogin ? "Don't have an account? " : 'Already have an account? '}
              <a href="#" onClick={(e) => { e.preventDefault(); setIsLogin(!isLogin); }}>
                {isLogin ? 'Sign up' : 'Sign in'}
              </a>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
