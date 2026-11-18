# SkillSync — Career & Skill Intelligence Platform

Full-stack career intelligence starter: registration/login, job-description analysis, CV skill extraction, learning-roadmap suggestions, per-user history, Redis caching, Docker Compose and CI.

## Run with Docker

Install and start Docker Desktop. In PowerShell, from this project folder:

```powershell
Copy-Item .env.example .env
```

Edit `.env` and set a long random `JWT_SECRET_KEY`, then run:

```powershell
docker compose up --build
```

Open frontend http://localhost:5173, API docs http://localhost:8000/docs, health http://localhost:8000/health.

## Run locally without Docker (Windows PowerShell)

Requires Python 3.13+ and Node.js 22+.

Backend terminal:

```powershell
cd backend
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

**Do not run `python app/main.py` or `python main.py`.** The backend uses package-relative imports and must be started with Uvicorn from the `backend` folder. Docker must be installed and running before `docker compose` works.

Frontend in a second terminal:

```powershell
cd frontend
npm install
npm run dev
```

Redis is optional for local development; the API continues without caching when Redis is unavailable.

## First use

1. Register (password minimum 10 characters), then sign in.
2. Paste a job description and your current skills; analyze the gap.
3. Generate a roadmap from missing skills.
4. Optionally upload a text-based PDF/DOCX CV (max 5 MB). It is processed in memory and not saved.

## API

| Method | Endpoint | Auth | Purpose |
|---|---|---:|---|
| GET | `/health` | No | API and Redis status |
| POST | `/api/auth/register` | No | Register |
| POST | `/api/auth/login` | No | Obtain JWT |
| GET | `/api/auth/me` | Yes | Current user |
| POST | `/api/analyses` | Yes | Analyze job description |
| GET | `/api/analyses` | Yes | Own analysis history |
| GET | `/api/analyses/{id}` | Yes | Read own analysis |
| POST | `/api/cv/skills` | Yes | Extract CV skills |
| POST | `/api/roadmaps` | Yes | Generate roadmap |

## Security and limitations

Passwords use Argon2 hashing; access tokens are signed JWTs with expiry. Analysis records are scoped to the authenticated user. Redis caching is short-lived and fails open to the database. CV uploads are type/size checked and parsed in memory.

The skill extractor is a keyword baseline, not an LLM. Match score is not a hiring probability. Roadmaps are suggestions. Before public deployment, configure strong secrets and exact CORS origins, and add rate limiting, email verification, password reset, refresh-token rotation, malware scanning, observability, and cloud deployment. Do not claim these are implemented.
