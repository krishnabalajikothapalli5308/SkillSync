"""Transparent baseline skill extraction; replace with an NLP/LLM service later."""
SKILL_KEYWORDS = {
    "Python": ["python"], "Java": ["java"], "JavaScript": ["javascript", "js"],
    "TypeScript": ["typescript"], "React": ["react"], "Node.js": ["node.js", "nodejs"],
    "FastAPI": ["fastapi"], "Django": ["django"], "Flask": ["flask"],
    "REST APIs": ["rest api", "restful", "api design"], "SQL": ["sql"],
    "PostgreSQL": ["postgresql", "postgres"], "SQLite": ["sqlite"],
    "Redis": ["redis"], "Docker": ["docker", "containerization", "containers"],
    "Kubernetes": ["kubernetes", "k8s"], "AWS": ["aws", "amazon web services"],
    "Azure": ["azure"], "GCP": ["google cloud", "gcp"],
    "CI/CD": ["ci/cd", "continuous integration", "continuous delivery"],
    "GitHub Actions": ["github actions"], "Linux": ["linux"],
    "Kafka": ["kafka"], "Microservices": ["microservices"],
    "Distributed Systems": ["distributed systems"], "System Design": ["system design"],
    "Pytest": ["pytest"], "Unit Testing": ["unit testing", "automated testing"],
    "Git": ["git", "github"], "OAuth2": ["oauth2", "oauth 2.0"],
    "JWT": ["jwt", "json web token"], "Machine Learning": ["machine learning", "ml"],
}

def extract_skills(text: str) -> list[str]:
    content = text.casefold()
    found = []
    for canonical, aliases in SKILL_KEYWORDS.items():
        if any(alias in content for alias in aliases):
            found.append(canonical)
    return sorted(found)

def compare_skills(required: list[str], current: list[str]):
    normalized = {skill.strip().casefold(): skill.strip() for skill in current if skill.strip()}
    matched = [skill for skill in required if skill.casefold() in normalized]
    missing = [skill for skill in required if skill.casefold() not in normalized]
    score = round((len(matched) / len(required)) * 100) if required else 0
    return matched, missing, score
