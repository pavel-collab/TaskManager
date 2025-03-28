from fastapi import FastAPI
from app.db import Base, engine
from app.routes import task_routes
from app.routes import project_routes
from app.routes import user_routes

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(task_routes.router, prefix="/api", tags=["tasks"])
app.include_router(user_routes.router, prefix="/api", tags=["users"])
app.include_router(project_routes.router, prefix="/api", tags=["projects"])

@app.get("/")
def read_root():
    return {"message": "Welcome to task manager API"}