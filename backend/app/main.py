import os
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .database import Base, engine, get_db
from .models import User, JobAnalysis
from .schemas import (RegisterRequest, LoginRequest, TokenOut, UserOut, AnalyzeRequest,
                      AnalysisOut, CVOut, RoadmapRequest, RoadmapOut, HealthOut)
from .security import hash_password, verify_password, create_access_token
from .auth import get_current_user
from .skill_engine import extract_skills, compare_skills
from .cv_parser import extract_cv_text
from .roadmap import build_roadmap
from .cache import cache_get, cache_set, cache_delete_pattern, redis_status

Base.metadata.create_all(bind=engine)
app = FastAPI(title="SkillSync API", version="2.0.0",
              description="Career intelligence platform with authentication, CV parsing and skill-gap roadmaps.")

origins = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173").split(",")
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True,
                   allow_methods=["GET", "POST", "OPTIONS"], allow_headers=["Authorization", "Content-Type"])

@app.get("/health", response_model=HealthOut, tags=["Operations"])
def health():
    status = redis_status()
    return {"status": "ok", "service": "skillsync-api", "redis": status}

@app.post("/api/auth/register", response_model=UserOut, status_code=201, tags=["Authentication"])
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    email = payload.email.lower()
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(status_code=409, detail="An account with this email already exists.")
    user = User(email=email, password_hash=hash_password(payload.password))
    db.add(user); db.commit(); db.refresh(user)
    return user

@app.post("/api/auth/login", response_model=TokenOut, tags=["Authentication"])
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email.lower()).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect email or password.")
    return {"access_token": create_access_token(str(user.id)), "token_type": "bearer"}

@app.get("/api/auth/me", response_model=UserOut, tags=["Authentication"])
def me(user: User = Depends(get_current_user)):
    return user

@app.post("/api/analyses", response_model=AnalysisOut, tags=["Analysis"])
def create_analysis(payload: AnalyzeRequest, db: Session = Depends(get_db),
                    user: User = Depends(get_current_user)):
    required = extract_skills(payload.description)
    matched, missing, score = compare_skills(required, payload.current_skills)
    record = JobAnalysis(user_id=user.id, title=payload.title, company=payload.company,
                         description=payload.description, extracted_skills=required,
                         matched_skills=matched, missing_skills=missing, match_score=score)
    db.add(record); db.commit(); db.refresh(record)
    cache_delete_pattern(f"analyses:{user.id}:*")
    return record

@app.get("/api/analyses", response_model=list[AnalysisOut], tags=["Analysis"])
def list_analyses(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    key = f"analyses:{user.id}:list"
    cached = cache_get(key)
    if cached is not None:
        return cached
    records = db.query(JobAnalysis).filter(JobAnalysis.user_id == user.id).order_by(
        JobAnalysis.created_at.desc()).limit(50).all()
    result = [AnalysisOut.model_validate(row).model_dump(mode="json") for row in records]
    cache_set(key, result, ttl=45)
    return result

@app.get("/api/analyses/{analysis_id}", response_model=AnalysisOut, tags=["Analysis"])
def get_analysis(analysis_id: int, db: Session = Depends(get_db),
                 user: User = Depends(get_current_user)):
    record = db.query(JobAnalysis).filter(JobAnalysis.id == analysis_id,
                                          JobAnalysis.user_id == user.id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return record

@app.post("/api/cv/skills", response_model=CVOut, tags=["CV"])
async def parse_cv(file: UploadFile = File(...), user: User = Depends(get_current_user)):
    text = await extract_cv_text(file)
    return {"filename": file.filename or "uploaded-cv",
            "extracted_skills": extract_skills(text), "text_characters": len(text)}

@app.post("/api/roadmaps", response_model=RoadmapOut, tags=["Learning Roadmap"])
def roadmap(payload: RoadmapRequest, user: User = Depends(get_current_user)):
    return {"tasks": build_roadmap(payload.missing_skills)}

