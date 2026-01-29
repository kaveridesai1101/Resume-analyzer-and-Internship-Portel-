# 🤖 Resume Intelligence & Internship Portal 🚀

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white)](https://nextjs.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![AICTE Aligned](https://img.shields.io/badge/AICTE-Aligned-blue?style=for-the-badge)](https://www.aicte-india.org/)

An enterprise-grade, **AI-powered ecosystem** designed to bridge the gap between students and opportunities. This platform leverages advanced NLP to analyze resumes and match them with the perfect internships.

---

## ✨ Key Features

### 👨‍🎓 For Students (Candidates)
- **🧠 AI Resume Parsing**: Instant extraction of skills, education, and experience.
- **🎯 Smart Job Matching**: Matches your profile with jobs using a proprietary ranking algorithm.
- **📄 Interactive Dashboard**: Track applications, view insights, and manage profile in real-time.
- **⚡ One-Click Apply**: Seamless application process for verified internships.

### 💼 For Recruiters
- **📢 Smart Job Posting**: AI-assisted job description generation.
- **📈 Candidate Scoring**: Instantly rank candidates based on their skill match percentage.
- **🛠️ Applicant Management**: Move candidates through different hiring stages with ease.
- **📊 Analytics**: View hiring trends and candidate source metrics.

### 🛡️ For Portal Admins
- **🔐 User Management**: Complete control over student and recruiter accounts.
- **🏢 Company Verification**: Ensure only legitimate companies post opportunities.
- **📡 System Monitoring**: Real-time status updates via WebSockets.

---

## 🛠️ Tech Stack

- **Frontend**: Next.js 15+ (App Router), Tailwind CSS v4, Framer Motion, Lucide Icons.
- **Backend**: FastAPI (Python 3.9+), Pydantic v2, SQLAlchemy.
- **AI/ML**: NLP for Resume Parsing, FAISS for Semantic Search, Sklearn for scoring.
- **Real-time**: WebSockets for instant notifications.
- **Database**: SQLite (Development) / PostgreSQL (Production ready).

---

## 🚀 Getting Started

### 📋 Prerequisites
- Python 3.9+
- Node.js 18+
- npm or yarn

### 🔧 Installation

#### 1. Clone the repository
```bash
git clone https://github.com/kaveridesai1101/Resume-analyzer-and-Internship-Portel-.git
cd Resume-analyzer-and-Internship-Portel-
```

#### 2. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

#### 3. Frontend Setup
```bash
cd ../frontend
npm install
npm run dev
```

The app will be available at:
- **Frontend**: [http://localhost:3000](http://localhost:3000)
- **Backend API**: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- **Interactive API Docs**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 📁 Project Structure

```text
├── backend/            # FastAPI Project Root
│   ├── app/            # Application Logic (API, Models, Schemas)
│   ├── uploads/        # Stored Resumes
│   └── main.py         # Entry Point
├── frontend/           # Next.js Project Root
│   ├── app/            # Pages & Global Styles
│   ├── components/     # UI Reusable Components
│   └── lib/            # Utilities & Auth Logic
└── README.md
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

Designed with ❤️ for Students and Recruiters.
