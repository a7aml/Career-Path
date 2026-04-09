from fastapi import APIRouter, HTTPException
from openai import OpenAI
from app.schemas.chat import ChatRequest, ChatResponse
from app.core.config import settings

router = APIRouter()

_groq = OpenAI(
    api_key=settings.GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1",
)


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

        response = _groq.chat.completions.create(
            model=settings.GROQ_MODEL,
            messages=messages,
            temperature=0.7,
            max_tokens=500,
        )
        reply = response.choices[0].message.content.strip()
        return ChatResponse(reply=reply)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat failed: {str(e)}")
