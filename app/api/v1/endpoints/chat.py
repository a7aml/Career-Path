from fastapi import APIRouter, HTTPException
from app.schemas.chat import ChatRequest, ChatResponse
import ollama
from app.core.config import settings

router = APIRouter()


@router.post("/message", response_model=ChatResponse)
async def chat_message(request: ChatRequest):
    try:
        system_prompt = (
            "You are a helpful career advisor AI. "
            "Give concise, practical advice for students and recent graduates. "
            "Keep responses under 200 words."
        )
        if request.career_context:
            system_prompt += f"\n\nCareer context for this user: {request.career_context}"

        messages = [{"role": "system", "content": system_prompt}]
        for msg in request.messages:
            messages.append({"role": msg.role, "content": msg.content})

        response = ollama.chat(
            model=settings.OLLAMA_MODEL,
            messages=messages,
            options={"temperature": 0.7, "num_predict": 500},
        )
        reply = response["message"]["content"].strip()
        return ChatResponse(reply=reply)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat failed: {str(e)}")
