# AI Career Assistant

A full-stack AI-powered career platform that helps users with career guidance, resume analysis, and interview preparation — all powered by OpenAI GPT-4o-mini.

![Python](https://img.shields.io/badge/Python-Flask-blue?logo=python)
![React](https://img.shields.io/badge/React-TypeScript-61DAFB?logo=react)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-412991?logo=openai)
![Firebase](https://img.shields.io/badge/Firebase-Auth%20%2B%20Firestore-FFCA28?logo=firebase)

---

## Features

### Career Counsellor
AI-powered career recommendations based on your skills, interests, and experience. Get personalized career path suggestions with actionable next steps.

### Resume Summarizer
Upload your PDF resume and get an instant AI-generated summary highlighting your key qualifications, skills, and experience.

### Resume Feedback
Comprehensive resume analysis with:
- Score out of 100 with animated visual indicator
- Strengths and weaknesses breakdown
- Specific improvement suggestions
- Detailed score reasoning

### Interview Preparation
Upload your resume and receive a detailed, personalized interview preparation guide covering common questions, technical topics, and strategies.

### Mock Interview
Practice with 30 AI-generated MCQ questions based on your resume:
- Questions auto-generated from your resume content
- Real-time scoring and performance tracking
- Detailed results with correct/incorrect breakdown

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | React 19, TypeScript, Vite 7 |
| **Backend** | Python Flask (REST API) |
| **AI/LLM** | OpenAI GPT-4o-mini |
| **Auth** | Firebase Authentication |
| **Database** | Firebase Firestore |
| **PDF Processing** | PyMuPDF (fitz) |
| **Styling** | Custom CSS (dark theme, glassmorphism) |

---

## Project Structure

```
career_assistant/
├── app/                          # Flask Backend
│   ├── __init__.py               # App factory (Flask + CORS)
│   ├── openai_api.py             # OpenAI API wrapper
│   ├── firebase_config.py        # Firebase Admin SDK setup
│   ├── pdf_utils.py              # PDF text extraction
│   └── routes/
│       ├── auth_routes.py        # Login/Logout/Status endpoints
│       ├── dashboard_routes.py   # Dashboard data endpoint
│       └── ai_routes.py          # All AI tool endpoints
├── frontend/                     # React + TypeScript Frontend
│   ├── src/
│   │   ├── App.tsx               # Router & protected routes
│   │   ├── index.css             # Full design system (dark theme)
│   │   ├── context/
│   │   │   └── AuthContext.tsx    # Firebase auth state provider
│   │   ├── services/
│   │   │   └── api.ts            # Axios API client
│   │   ├── components/
│   │   │   ├── FileUpload.tsx     # Drag & drop PDF upload
│   │   │   └── Layout/
│   │   │       └── Navbar.tsx     # Navigation bar
│   │   ├── pages/
│   │   │   ├── Login.tsx          # Split-panel login/register
│   │   │   ├── Dashboard.tsx      # Stats + hero + services
│   │   │   ├── CareerCounselor.tsx
│   │   │   ├── ResumeSummarizer.tsx
│   │   │   ├── ResumeFeedback.tsx # SVG score circle animation
│   │   │   ├── InterviewPrep.tsx
│   │   │   └── MockInterview.tsx  # 30 MCQ quiz with timer
│   │   └── types/
│   │       └── index.ts          # TypeScript interfaces
│   ├── package.json
│   ├── tsconfig.json
│   └── vite.config.ts            # Proxy /api -> Flask:5000
├── requirements.txt
├── run.py                        # Flask entry point
└── .gitignore
```

---

## Getting Started

### Prerequisites

- Python 3.9+
- Node.js 20+
- Firebase project with Auth & Firestore enabled
- OpenAI API key

### 1. Clone the repository

```bash
git clone https://github.com/Arifuzzaman-Swapnil/AiCareerAgent.git
cd AiCareerAgent
```

### 2. Setup Backend

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

Place your Firebase service account JSON file as `firebase_service_account.json` in the project root.

### 4. Setup Frontend

```bash
cd frontend
npm install
```

### 5. Run the Application

**Terminal 1 — Backend (Flask):**
```bash
python run.py
```
Flask runs on `http://localhost:5000`

**Terminal 2 — Frontend (Vite):**
```bash
cd frontend
npm run dev
```
Frontend runs on `http://localhost:5173` (auto-proxies `/api` to Flask)

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/login` | Firebase login + session |
| POST | `/api/auth/logout` | Clear session |
| GET | `/api/auth/status` | Check auth status |
| GET | `/api/dashboard` | Get user stats |
| POST | `/api/tools/career` | Career counselling |
| POST | `/api/tools/resume/summarize` | Resume summarization |
| POST | `/api/tools/resume/feedback` | Resume feedback + score |
| POST | `/api/tools/interview/prep` | Interview prep guide |
| POST | `/api/tools/interview/generate` | Generate 30 MCQs |
| GET | `/api/tools/interview/questions` | Get generated questions |
| POST | `/api/tools/interview/submit` | Submit MCQ answers |
| GET | `/api/tools/interview/results` | Get interview results |

---

## Design

- Premium dark theme (`#030014` background)
- Glassmorphism cards with `backdrop-filter: blur()`
- Animated hero section with floating particles, glow orbs, and grid background
- Split-panel login (branding + form)
- Animated SVG score circles
- Responsive design (desktop, tablet, mobile)
- Custom scrollbar and selection colors
- Inter + Poppins typography

---

## License

This project is open source and available under the [MIT License](LICENSE).

---

**Built with OpenAI GPT-4o-mini, React, and Flask**
