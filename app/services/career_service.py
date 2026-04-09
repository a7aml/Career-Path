from app.schemas.career import (
    UserProfileInput,
    CareerGeneratorResponse,
    CareerMatch,
    SkillGapItem,
    RoadmapStep,
    ProjectIdea
)
from app.services.ai_service import generate_career_guidance

async def generate_career_results(profile: UserProfileInput) -> CareerGeneratorResponse:
    raw = await generate_career_guidance(profile)

    career_matches = [CareerMatch(**c) for c in raw.get("career_matches", [])]
    skills_gap = [SkillGapItem(**s) for s in raw.get("skills_gap", [])]
    roadmap = [RoadmapStep(**r) for r in raw.get("roadmap", [])]
    project_ideas = [ProjectIdea(**p) for p in raw.get("project_ideas", [])]
    summary = raw.get("summary", "")

    return CareerGeneratorResponse(
        career_matches=career_matches,
        skills_gap=skills_gap,
        roadmap=roadmap,
        project_ideas=project_ideas,
        summary=summary
    )