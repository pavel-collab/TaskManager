from pydantic_settings import  BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres:1234@localhost:5432/postgres"
    SECRET_KEY: str = ""
    class Config:
        env_file: str = ".env"

settings = Settings()