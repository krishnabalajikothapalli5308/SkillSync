RESOURCE_MAP = {
    "Docker": ("Containerise a small FastAPI service with a multi-stage or slim image.",
               "Build the image and run the container; document its port and environment variables."),
    "AWS": ("Deploy a small API to an AWS service appropriate to your budget and learning goals.",
            "Provide a working health endpoint and explain IAM permissions and secret handling."),
    "Redis": ("Add a short-lived cache for a read-heavy API endpoint.",
              "Demonstrate cache hit, cache miss, expiry and invalidation."),
    "CI/CD": ("Create a pipeline that runs tests and builds an application image.",
              "Show a passing GitHub Actions run and explain what blocks a failed deployment."),
    "GitHub Actions": ("Automate linting and tests on every pull request.",
                       "Open a pull request and show the workflow passing."),
    "Kubernetes": ("Deploy a small container using a Deployment and Service manifest.",
                   "Explain replicas, readiness probes and configuration."),
    "Kafka": ("Build a producer-consumer demo for a background event.",
              "Show message processing and explain retry and duplicate-delivery handling."),
    "Distributed Systems": ("Document a failure scenario involving retries and duplicate requests.",
                            "Explain idempotency, timeouts and consistency trade-offs."),
    "System Design": ("Design a URL shortener or job-analysis service.",
                      "Present API contracts, data model, scaling bottlenecks and trade-offs."),
    "PostgreSQL": ("Move a development data model from SQLite to PostgreSQL.",
                   "Run migrations and verify indexes and constraints."),
    "Unit Testing": ("Add tests for success cases, validation errors and edge cases.",
                    "Show deterministic tests running in CI."),
    "Linux": ("Run and inspect the service from a Linux environment.",
              "Demonstrate process, port, log and file-permission troubleshooting."),
}

def build_roadmap(missing_skills: list[str]):
    tasks = []
    for skill in missing_skills[:10]:
        objective, verification = RESOURCE_MAP.get(
            skill, (f"Study {skill} fundamentals and apply them in a small, focused feature.",
                    f"Demonstrate a working implementation of {skill} and explain its trade-offs.")
        )
        tasks.append({
            "skill": skill,
            "objective": objective,
            "suggested_project": f"Add a focused {skill} capability to SkillSync.",
            "verification": verification,
        })
    return tasks
