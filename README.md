# AI-Powered Resume Analyzer & Recruitment Platform

A comprehensive SaaS-grade recruitment platform connecting Candidates, Recruiters, and Admins.

## Features
- **Candidate Module**: Resume parsing, AI job matching, application tracking.
- **Recruiter Module**: Job posting, AI description generation, candidate ranking.
- **Admin Module**: Analytics, user management, content moderation.

## Tech Stack
- **Backend**: Python (FastAPI)
- **Frontend**: Next.js (React) + Tailwind CSS
- **Database**: SQLite (Default) / PostgreSQL (Supported)
- **AI**: spaCy, Scikit-learn/FAISS

## Getting Started

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```
