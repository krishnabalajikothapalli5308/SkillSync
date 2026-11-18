# SkillSync — AI-Powered Career & Skill Intelligence Platform

**Turn job descriptions into your next career move.**

SkillSync is a full-stack career intelligence platform that helps users understand job requirements, evaluate their existing skills, identify skill gaps, and generate personalized learning roadmaps.

Instead of randomly learning technologies, users can make informed decisions about what to learn next based on their target roles.

---

## Overview

SkillSync connects a user's existing technical skills with the requirements of their desired job role.

Users can create an account, upload their CV, analyze job descriptions, view matched and missing skills, and generate actionable learning roadmaps.

## Key Features

### 1. User Authentication
- User registration and login.
- Password hashing and JWT-based authentication.
- Protected user-specific resources.

### 2. CV Skill Extraction
- Upload PDF and DOCX resumes.
- Extract text and identify technical skills.
- Use extracted skills directly in job analysis.
- Process uploaded documents in memory.

### 3. Job Description Analysis
- Enter job title, company, and job description.
- Compare job requirements against existing skills.
- Identify matched skills and missing skills.
- Calculate a skill-match percentage.

### 4. Personalized Learning Roadmaps
- Generate learning tasks based on identified skill gaps.
- Provide learning objectives.
- Suggest practical projects.
- Define ways to demonstrate acquired skills.

### 5. Private Analysis History
- Save job analyses to the user's account.
- Retrieve previous analyses.
- Keep user workspaces separate.

### 6. Redis Caching
- Redis integration for frequently accessed data.
- Cache-related operations to improve response efficiency.
- Graceful fallback when Redis is unavailable.

---

## Tech Stack

| Layer | Technologies |
|---|---|
| Frontend | React, JavaScript, CSS |
| Build Tool | Vite |
| Backend | Python, FastAPI |
| Database | SQLite, SQLAlchemy |
| Authentication | JWT, Password Hashing |
| Caching | Redis |
| Document Processing | PDF and DOCX parsing |
| Testing | Pytest, Vitest |
| Containerization | Docker, Docker Compose |
| Version Control | Git, GitHub |

---

## System Architecture

```text
              USER
               |
               v
       React Frontend
          (Vite)
               |
          HTTP Requests
               |
               v
        FastAPI Backend
               |
       +-------+--------+
       |       |        |
       v       v        v
  Authentication  Skill   CV Parser
       |          Engine      |
       |             |        |
       +-------------+--------+
                     |
             +-------+-------+
             |               |
             v               v
          SQLite           Redis
         Database          Cache
             |
             v
       Analysis History
             |
             v
      Learning Roadmap
```

---

Project Structure

SkillSync/
│
├── backend/
│   ├── app/
│   │   ├── auth.py
│   │   ├── cache.py
│   │   ├── cv_parser.py
│   │   ├── database.py
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── roadmap.py
│   │   ├── schemas.py
│   │   ├── security.py
│   │   └── skill_engine.py
│   │
│   ├── tests/
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── style.css
│   ├── package.json
│   └── vite.config.js
│
├── .github/
├── .env.example
├── .gitignore
├── docker-compose.yml
└── README.md

Getting Started

Prerequisites

Install the following:

Python 3.13+

Node.js and npm

Git

Redis and Docker are optional for running the application locally, depending on your configuration.

1. Clone the repository

git clone https://github.com/krishnabalajikothapalli5308/SkillSync.git
cd SkillSync

2. Configure the backend

cd backend
python -m venv venv

Activate the virtual environment on Windows:

.\venv\Scripts\Activate.ps1

Install dependencies:

pip install -r requirements.txt

Configure the environment variables using the project's .env.example as a reference. Set a secure JWT secret before using the application beyond local development.

Start the backend:

python -m uvicorn app.main:app --reload

Backend API:

http://localhost:8000

Interactive API documentation:

http://localhost:8000/docs

Health check:

http://localhost:8000/health

3. Configure the frontend

Open another terminal:

cd frontend
npm install
npm run dev

Frontend:

http://localhost:5173

Configure VITE_API_URL if your backend is running at a different address.

Testing

Run backend tests from the project root:

python -m pytest backend/tests -v

Build the frontend:

cd frontend
npm run build

Future Improvements

Semantic skill matching using NLP.

Integration with external job platforms.

More advanced recommendation algorithms.

Learning progress tracking.

Cloud deployment and production monitoring.

Enhanced analytics and career insights.

Why SkillSync?

Traditional job searching focuses on whether a candidate matches a job description.

SkillSync takes the next step:

It helps candidates understand what they are missing and how to work towards it.

The goal is to make career preparation more structured, measurable, and personalized.

Author

Krishna Balaji Kothapalli

Computer Science Undergraduate | Full-Stack Development | AI/ML

GitHub: krishnabalajikothapalli5308

SkillSync — Build skills with direction. Move forward with confidence.
