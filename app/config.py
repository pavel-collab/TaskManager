from pydantic import  BaseSettings

class Settings(BaseSettings):
    DATABASE_URL = "postgresql://user:password@localhost/task_manager_db"
    SECRET_KEY = ""
    
    class Config:
        env_file = ".env"

settings = Settings()