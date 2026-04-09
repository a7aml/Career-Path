from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.session import supabase
from app.api.v1.router import api_router

app = FastAPI(
    title="CareerPath AI",
    description="AI-powered career guidance for students and graduates",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def root():
    return {"message": "Welcome to CareerPath AI"}

@app.get("/health")
def health_check():
    try:
        supabase.table("profiles").select("id").limit(1).execute()
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": str(e)}