from fastapi import APIRouter, HTTPException
from app.schemas.career import UserProfileInput, CareerGeneratorResponse
from app.services.career_service import generate_career_results

router = APIRouter()

@router.post("/generate", response_model=CareerGeneratorResponse)
async def generate_career(profile: UserProfileInput):
    try:
        results = await generate_career_results(profile)
        return results
    except ValueError as e:
        raise HTTPException(status_code=422, detail=f"AI response parsing error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Career generation failed: {str(e)}")