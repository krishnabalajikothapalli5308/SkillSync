from app.skill_engine import extract_skills, compare_skills
from app.roadmap import build_roadmap

def test_extracts_known_skills():
    assert extract_skills('Build REST APIs with Python, FastAPI, Docker and Redis') == [
        'Docker', 'FastAPI', 'Python', 'REST APIs', 'Redis'
    ]

def test_skill_gap_score():
    matched, missing, score = compare_skills(['Python', 'Docker', 'AWS'], ['python', 'Docker'])
    assert matched == ['Python', 'Docker']
    assert missing == ['AWS']
    assert score == 67

def test_empty_requirements():
    assert compare_skills([], ['Python']) == ([], [], 0)

def test_roadmap_for_missing_skill():
    task = build_roadmap(['Docker'])[0]
    assert task['skill'] == 'Docker'
    assert 'containerise' in task['objective'].lower()
