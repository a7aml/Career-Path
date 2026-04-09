import ollama
import json
import re
from app.core.config import settings
from app.schemas.career import UserProfileInput

def build_career_prompt(profile: UserProfileInput) -> str:
    return f"""You are a career advisor. Return ONLY valid JSON, nothing else.

Student profile:
- Major: {profile.major}
- Skills: {', '.join(profile.skills)}
- Interests: {', '.join(profile.interests)}
- Experience: {profile.experience_level}
- Goals: {profile.goals}

Return this exact JSON structure:

{{
  "summary": "Two sentence career summary here.",
  "career_matches": [
    {{"title": "Data Scientist", "match_score": 87, "description": "Analyzes data to find insights.", "required_skills": ["Python", "ML", "SQL"], "why_it_fits": "Matches your Python skills and AI interest."}},
    {{"title": "ML Engineer", "match_score": 81, "description": "Builds ML systems at scale.", "required_skills": ["Python", "TensorFlow", "MLOps"], "why_it_fits": "Aligns with your AI goals."}},
    {{"title": "Data Analyst", "match_score": 74, "description": "Turns data into business insights.", "required_skills": ["SQL", "Excel", "Tableau"], "why_it_fits": "Uses your existing SQL and Excel skills."}}
  ],
  "skills_gap": [
    {{"skill_name": "Python", "status": "have", "priority": "high"}},
    {{"skill_name": "SQL", "status": "have", "priority": "high"}},
    {{"skill_name": "TensorFlow", "status": "missing", "priority": "high"}},
    {{"skill_name": "Machine Learning", "status": "missing", "priority": "high"}},
    {{"skill_name": "Data Visualization", "status": "partial", "priority": "medium"}},
    {{"skill_name": "Cloud Platforms", "status": "missing", "priority": "medium"}}
  ],
  "roadmap": [
    {{"step_order": 1, "title": "Strengthen Python", "description": "Learn pandas, numpy and matplotlib.", "duration_weeks": 2}},
    {{"step_order": 2, "title": "Learn Machine Learning", "description": "Study supervised and unsupervised learning.", "duration_weeks": 4}},
    {{"step_order": 3, "title": "Master TensorFlow", "description": "Build neural networks with TensorFlow.", "duration_weeks": 3}},
    {{"step_order": 4, "title": "Build Projects", "description": "Create 2-3 portfolio projects.", "duration_weeks": 4}},
    {{"step_order": 5, "title": "Apply for Jobs", "description": "Polish resume and apply to roles.", "duration_weeks": 2}}
  ],
  "project_ideas": [
    {{"title": "Movie Recommender", "description": "Build a recommendation system using collaborative filtering.", "skills_targeted": ["Python", "ML", "Pandas"], "difficulty": "beginner"}},
    {{"title": "Sales Forecaster", "description": "Predict sales using time series models.", "skills_targeted": ["Python", "Statistics", "Visualization"], "difficulty": "intermediate"}},
    {{"title": "Sentiment Analyzer", "description": "Analyze product reviews using NLP.", "skills_targeted": ["Python", "NLP", "TensorFlow"], "difficulty": "intermediate"}}
  ]
}}

Customize the content above based on the student profile. Keep the exact same JSON structure and key names. Return ONLY the JSON object."""

def parse_ai_response(response_text: str) -> dict:
    text = response_text.strip()

    # Remove markdown blocks
    text = re.sub(r'```json', '', text)
    text = re.sub(r'```', '', text)
    text = text.strip()

    # Extract JSON object
    start = text.find('{')
    end = text.rfind('}') + 1
    if start != -1 and end > start:
        text = text[start:end]

    # Try direct parse
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Fix common issues: trailing commas before } or ]
    text = re.sub(r',\s*}', '}', text)
    text = re.sub(r',\s*]', ']', text)

    # Try again
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Last resort: find each section individually
    result = {}
    for key in ["summary", "career_matches", "skills_gap", "roadmap", "project_ideas"]:
        pattern = rf'"{key}"\s*:\s*(\[.*?\]|".*?")'
        match = re.search(pattern, text, re.DOTALL)
        if match:
            try:
                result[key] = json.loads(match.group(1))
            except:
                result[key] = [] if key != "summary" else ""

    if result:
        return result

    raise ValueError(f"Could not parse AI response: {text[:200]}")

async def generate_career_guidance(profile: UserProfileInput) -> dict:
    prompt = build_career_prompt(profile)

    response = ollama.chat(
        model=settings.OLLAMA_MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are a career advisor. Always respond with valid JSON only. No explanations, no markdown."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        options={
            "temperature": 0.1,
            "num_predict": 3000,
        }
    )

    response_text = response['message']['content']
    return parse_ai_response(response_text)