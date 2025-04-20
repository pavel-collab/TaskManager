from fastapi.testclient import TestClient
import pytest
from app.db import Base, engine, session_local
from sqlalchemy.orm import sessionmaker
from app.main import app

#! Запуск тестов pytest test_app.py

#????
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создание тестовой базы данных
@pytest.fixture(scope="module")
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

client = TestClient(app)
    
@pytest.fixture(autouse=True)
def override_get_db(test_db):
    app.dependency_overrides[session_local] = TestingSessionLocal
    yield
    app.dependency_overrides.pop(session_local, None)
    
@pytest.fixture
def setup_database():
    # Здесь вы можете настроить базу данных для тестирования
    # Например, создать таблицы и добавить тестовые данные
    yield
    # Очистка базы данных после тестов


def test_create_user(setup_database):
    response = client.post(
        "/api/users/",
        json={
            "username": "john_doe",
            "email": "john@example.com",
            "password": "password123",
            "role": "DEVELOPER",
            "rating": 20
        }
    )
    assert response.status_code == 200
    assert response.json()["user"]["username"] == "john_doe"


# def test_create_user_with_existing_username(setup_database):
#     # Создаем пользователя
#     client.post(
#         "/api/users/",
#         json={
#             "username": "john_doe",
#             "email": "john@example.com",
#             "password": "password123",
#             "role": "DEVELOPER",
#             "rating": 20
#         }
#     )
    
#     # Пытаемся создать пользователя с тем же именем
#     response = client.post(
#         "/api/users/",
#         json={
#             "username": "john_doe",
#             "email": "john2@example.com",
#             "password": "password456",
#             "role": "DEVELOPER",
#             "rating": 30
#         }
#     )
#     assert response.status_code == 400  # Предполагаем, что код 400 - это ошибка
#     assert "detail" in response.json()


def test_get_all_users(setup_database):
    response = client.get("/api/users/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_user_by_id(setup_database):
    response = client.get("/api/users/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1


def test_get_nonexistent_user_by_id(setup_database):
    response = client.get("/api/users/999")  # Предполагаем, что пользователя с id 999 нет
    assert response.status_code == 404  # Ожидаем, что код 404 - это не найдено
    assert "detail" in response.json()


def test_update_user(setup_database):
    response = client.put(
        "/api/users/1",
        json={
            "username": "john_doe",
            "email": "john@example.com",
            "password": "password123",
            "role": "DEVELOPER"
        }
    )
    assert response.status_code == 200
    assert response.json()["user"]["username"] == "john_doe"


def test_update_nonexistent_user(setup_database):
    response = client.put(
        "/api/users/999",  # Предполагаем, что пользователя с id 999 нет
        json={
            "username": "john_doe",
            "email": "john@example.com",
            "password": "password123",
            "role": "DEVELOPER"
        }
    )
    assert response.status_code == 404  # Ожидаем, что код 404 - это не найдено
    assert "detail" in response.json()


def test_delete_user(setup_database):
    response = client.delete("/api/users/john_doe")
    assert response.status_code == 200


def test_delete_nonexistent_user(setup_database):
    response = client.delete("/api/users/non_existent_user")  # Имя пользователя, которого нет
    assert response.status_code == 404  # Ожидаем, что код 404 - это не найдено
    assert "detail" in response.json()