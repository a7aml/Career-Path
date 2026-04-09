from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SUPABASE_URL: str
    SUPABASE_KEY: str
    SECRET_KEY: str
    APP_ENV: str = "development"
    GROQ_API_KEY: str
    GROQ_MODEL: str = "llama-3.3-70b-versatile"
    FRONTEND_URL: str = "http://127.0.0.1:5500"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()