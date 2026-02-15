import { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';

export default function Navbar() {
  const { logout } = useAuth();
  const location = useLocation();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const navLinks = [
    { path: '/dashboard', label: 'Dashboard' },
    { path: '/career', label: 'Career Guide' },
    { path: '/summarizer', label: 'Resume' },
    { path: '/feedback', label: 'Feedback' },
    { path: '/interview-prep', label: 'Prep' },
    { path: '/interview', label: 'Interview' },
  ];

  const handleLogout = async () => {
    try {
      await logout();
    } catch (err) {
      console.error('Logout failed:', err);
    }
  };

  return (
    <header className="header">
      <div className="nav-container">
        <Link to="/dashboard" className="logo">
          <span className="logo-icon">💼</span>
          Career Assistant
        </Link>

        <nav className={`nav-links ${mobileMenuOpen ? 'active' : ''}`}>
          {navLinks.map((link) => (
            <Link
              key={link.path}
              to={link.path}
              className={location.pathname === link.path ? 'active' : ''}
              onClick={() => setMobileMenuOpen(false)}
            >
              {link.label}
            </Link>
          ))}
          <button onClick={handleLogout} className="logout-btn mobile-logout">
            Logout
          </button>
        </nav>

        <div className="nav-right">
          <button onClick={handleLogout} className="logout-btn desktop-logout">
            Logout
          </button>
          <button
            className="mobile-menu-btn"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            aria-label="Toggle menu"
          >
            {mobileMenuOpen ? '✕' : '☰'}
          </button>
        </div>
      </div>
    </header>
  );
}
