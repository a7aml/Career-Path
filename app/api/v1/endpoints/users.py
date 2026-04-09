from fastapi import APIRouter, Depends, HTTPException
from app.api.deps import get_current_user
from app.db.session import supabase

router = APIRouter()


@router.get("/profile")
async def get_profile(user=Depends(get_current_user)):
    try:
        result = supabase.table("profiles").select("*").eq("id", user.id).single().execute()
        return result.data
    except Exception as e:
        raise HTTPException(status_code=404, detail="Profile not found")
