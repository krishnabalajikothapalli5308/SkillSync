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

## Project Structure

```text
SkillSync/
│
├── backend/
│   ├── app/
│   │   ├── auth.py
│   │   ├── cache.py
│   │   ├── cv_parser.py
│   │   ├
