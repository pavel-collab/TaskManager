from fastapi.testclient import TestClient
from fastapi import FastAPI
import pytest
from app.db import Base, engine
from sqlalchemy.orm import sessionmaker

#! Запуск тестов pytest test_app.py

app = FastAPI()
client = TestClient(app)
# #????
# TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# # Создание тестовой базы данных
# @pytest.fixture(scope="module")
# def test_db():
#     Base.metadata.create_all(bind=engine)
#     yield
#     Base.metadata.drop_all(bind=engine)
    
# @pytest.fixture(autouse=True)
# def override_get_db(test_db):
#     app.dependency_overrides[SessionLocal] = TestingSessionLocal
#     yield
#     app.dependency_overrides.pop(SessionLocal, None)
    
#TODO: write lot of test. Test all of the CRUD operationd for all of the tables
#TODO: write positive and negative scinarious
def test_create_user():
    response = client.post("/users/", json={"name": "John"})
    assert response.status_code == 200
    assert response.json() == {"name": "John"}

def test_read_user():
    response = client.post("/users/", json={"name": "Jane"})
    user_id = response.json()["id"]

    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json() == {"id": user_id, "name": "Jane"}

def test_read_nonexistent_user():
    response = client.get("/users/9999")
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}