import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = os.environ.get(
        'DATABASE_URL', 
        'postgresql://postgres:1234@localhost:5432/postgres'
    )
    SECRET_KEY: str = ''

    class Config:
        env_file: str = '.env'


settings = Settings()

engine = create_engine(settings.DATABASE_URL)

session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()
