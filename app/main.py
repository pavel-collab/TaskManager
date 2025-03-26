from fastapi import FastAPI
from app.db import Base, engine
from app.routes import task_routes

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(task_routes.router, prefix="/api", tags=["tasks"])

@app.get("/")
def read_root():
    return {"message": "Welcome to task manager API"}