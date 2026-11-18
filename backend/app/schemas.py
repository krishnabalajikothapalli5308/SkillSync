from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict, EmailStr

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=10, max_length=128)

class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserOut(BaseModel):
    id: int
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)

class AnalyzeRequest(BaseModel):
    title: str = Field(min_length=2, max_length=200)
    company: str | None = Field(default=None, max_length=200)
    description: str = Field(min_length=30, max_length=20000)
    current_skills: list[str] = Field(default_factory=list)

class AnalysisOut(BaseModel):
    id: int
    title: str
    company: str | None
    extracted_skills: list[str]
    matched_skills: list[str]
    missing_skills: list[str]
    match_score: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class CVOut(BaseModel):
    filename: str
    extracted_skills: list[str]
    text_characters: int

class RoadmapRequest(BaseModel):
    missing_skills: list[str] = Field(default_factory=list, max_length=30)

class RoadmapTask(BaseModel):
    skill: str
    objective: str
    suggested_project: str
    verification: str

class RoadmapOut(BaseModel):
    tasks: list[RoadmapTask]

class HealthOut(BaseModel):
    status: str
    service: str
    redis: str
