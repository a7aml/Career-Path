from pydantic import BaseModel
from typing import List, Optional

class UserProfileInput(BaseModel):
    major: str
    skills: List[str]
    interests: List[str]
    goals: str
    experience_level: str

class CareerMatch(BaseModel):
    title: str
    match_score: int
    description: str
    required_skills: List[str]
    why_it_fits: str

class SkillGapItem(BaseModel):
    skill_name: str
    status: str        # "have", "missing", "partial"
    priority: str      # "high", "medium", "low"

class RoadmapStep(BaseModel):
    step_order: int
    title: str
    description: str
    duration_weeks: int

class ProjectIdea(BaseModel):
    title: str
    description: str
    skills_targeted: List[str]
    difficulty: str    # "beginner", "intermediate", "advanced"

class CareerGeneratorResponse(BaseModel):
    career_matches: List[CareerMatch]
    skills_gap: List[SkillGapItem]
    roadmap: List[RoadmapStep]
    project_ideas: List[ProjectIdea]
    summary: str