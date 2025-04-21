from fastapi.testclient import TestClient
import pytest
from app.db import Base, engine, session_local
from sqlalchemy.orm import sessionmaker
from app.main import app
from tests.helpers.helper import (helper_fill_users,
                                  helper_fill_projects,
                                  helper_fill_tasks)

#! Запуск тестов pytest test_app.py

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
client = TestClient(app)
    
@pytest.fixture
def setup_db_for_test_users():
    try:
        Base.metadata.drop_all(bind=engine)
    except Exception as ex:
        ... 
    # Здесь вы можете настроить базу данных для тестирования
    # Например, создать таблицы и добавить тестовые данные
    Base.metadata.create_all(bind=engine)
    yield
    # Очистка базы данных после тестов
    
@pytest.fixture
def setup_db_for_test_projects():
    try:
        Base.metadata.drop_all(bind=engine)
    except Exception as ex:
        ...
    Base.metadata.create_all(bind=engine)
    helper_fill_users(client=client)
    yield
    
@pytest.fixture
def setup_db_for_test_tasks():
    try:
        Base.metadata.drop_all(bind=engine)
    except Exception as ex:
        ...
    Base.metadata.create_all(bind=engine)
    helper_fill_users(client=client)
    helper_fill_projects(client=client)
    yield
    
@pytest.fixture
def setup_db_for_test_comments():
    try:
        Base.metadata.drop_all(bind=engine)
    except Exception as ex:
        ...
    Base.metadata.create_all(bind=engine)
    helper_fill_users(client=client)
    helper_fill_projects(client=client)
    helper_fill_tasks(client=client)
    yield

def setup_db_for_test_project_members():
    try:
        Base.metadata.drop_all(bind=engine)
    except Exception as ex:
        ...
    Base.metadata.create_all(bind=engine)
    helper_fill_users(client=client)
    helper_fill_projects(client=client)
    yield

################################################################TESTS FOR USERS################################################################

def test_create_user(setup_db_for_test_users):
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


def test_get_all_users():
    response = client.get("/api/users/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_user_by_id():
    response = client.get("/api/users/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1


def test_get_nonexistent_user_by_id():
    response = client.get("/api/users/999")  # Предполагаем, что пользователя с id 999 нет
    assert response.status_code == 404  # Ожидаем, что код 404 - это не найдено
    assert "detail" in response.json()


def test_update_user():
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


def test_update_nonexistent_user():
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


def test_delete_user():
    response = client.delete("/api/users/john_doe")
    assert response.status_code == 200


def test_delete_nonexistent_user():
    response = client.delete("/api/users/non_existent_user")  # Имя пользователя, которого нет
    assert response.status_code == 404  # Ожидаем, что код 404 - это не найдено
    assert "detail" in response.json()
    
################################################################TESTS FOR PROJECTS################################################################

def test_create_project(setup_db_for_test_projects):
    response = client.post(
        "/api/projects/",
        json={
            "title": "Project_1",
            "description": "My first project",
            "owner_id": 1,
            "status": "TODO",
            "project_start_date": "2024-09-01T00:00:00",
            "project_end_date": "2024-09-30T00:00:00"
        }
    )
    assert response.status_code == 200  # Предполагаем, что код 201 - это успешное создание
    assert response.json()["project"]["title"] == "Project_1"


# def test_create_project_with_invalid_owner():
#     response = client.post(
#         "/api/projects/",
#         json={
#             "title": "Project_2",
#             "description": "My second project",
#             "owner_id": 9999,  # Предполагаем, что такого пользователя не существует
#             "status": "TODO",
#             "project_start_date": "2024-09-01T00:00:00",
#             "project_end_date": "2024-09-30T00:00:00"
#         }
#     )
#     assert response.status_code == 400  # Ожидаем, что код 400 - это ошибка
#     assert "detail" in response.json()


def test_get_all_projects():
    response = client.get("/api/projects/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_project_by_id():
    response = client.get("/api/projects/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1  # Проверяем, что получаем правильный проект


def test_get_nonexistent_project_by_id():
    response = client.get("/api/projects/999")  # Предполагаем, что проекта с id 999 нет
    assert response.status_code == 404  # Ожидаем, что код 404 - это не найдено
    assert "detail" in response.json()


def test_update_project():
    response = client.put(
        "/api/projects/1",
        json={
            "title": "Project new",
            "description": "My first project",
            "owner_id": 3,
            "status": "TODO",
            "project_start_date": "2024-09-01T00:00:00",
            "project_end_date": "2024-09-30T00:00:00"
        }
    )
    assert response.status_code == 200  # Предполагаем, что код 200 - это успешное обновление
    assert response.json()["project"]["title"] == "Project new"


def test_update_nonexistent_project():
    response = client.put(
        "/api/projects/999",  # Предполагаем, что проекта с id 999 нет
        json={
            "title": "Project new",
            "description": "My first project",
            "owner_id": 3,
            "status": "TODO",
            "project_start_date": "2024-09-01T00:00:00",
            "project_end_date": "2024-09-30T00:00:00"
        }
    )
    assert response.status_code == 404  # Ожидаем, что код 404 - это не найдено
    assert "detail" in response.json()


# def test_delete_project():
#     response = client.delete("/api/projects/Project_1")
#     assert response.status_code == 204  # Ожидаем, что код 204 - это успешное удаление


def test_delete_nonexistent_project():
    response = client.delete("/api/projects/non_existent_project")  # Имя проекта, которого нет
    assert response.status_code == 404  # Ожидаем, что код 404 - это не найдено
    assert "detail" in response.json()
    
################################################################TESTS FOR TASKS################################################################

# Тест для создания задачи
def test_create_task(setup_db_for_test_tasks):
    response = client.post(
        "/api/tasks/",
        json={
            "title": "Task_1",
            "description": "Complete the API",
            "status": "TODO",
            "project_id": 1,
            "complexity": "LOW",
            "assign_id": 1,
            "task_start_date": "2024-09-01T00:00:00",
            "task_end_date": "2024-09-15T00:00:00"
        },
    )
    assert response.status_code == 200  # Ожидаем, что задача была создана
    assert response.json()["task"]["title"] == "Task_1"

# Тест для получения списка всех задач
def test_get_all_tasks():
    response = client.get("/api/tasks/")
    assert response.status_code == 200  # Ожидаем успешный ответ
    assert isinstance(response.json(), list)  # Ожидаем, что ответ - это список

# Тест для получения задачи по id
def test_get_task_by_id():
    response = client.get("/api/tasks/1")
    assert response.status_code == 200  # Ожидаем успешный ответ
    assert response.json()["title"] == "Task_1"

# Негативный тест для получения несуществующей задачи
def test_get_nonexistent_task():
    response = client.get("/api/tasks/999")  # Предполагаем, что задача с id 999 не существует
    assert response.status_code == 404  # Ожидаем, что задача не найдена

# Тест для изменения параметров задачи
def test_update_task():
    response = client.put(
        "/api/tasks/1",
        json={
            "title": "NewImportantTask",
            "description": "Complete the API",
            "status": "TODO",
            "project_id": 1,
            "complexity": "LOW",
            "assign_id": 1,
            "task_start_date": "2024-09-01T00:00:00",
            "task_end_date": "2024-09-15T00:00:00",
        },
    )
    assert response.status_code == 200  # Ожидаем успешный ответ
    assert response.json()["task"]["title"] == "NewImportantTask"

# Негативный тест для изменения несуществующей задачи
def test_update_nonexistent_task():
    response = client.put(
        "/api/tasks/999",
        json={
            "title": "NewImportantTask",
            "description": "Complete the API",
            "status": "TODO",
            "project_id": 1,
            "complexity": "LOW",
            "assign_id": 1,
            "task_start_date": "2024-09-01T00:00:00",
            "task_end_date": "2024-09-15T00:00:00",
        },
    )
    assert response.status_code == 404  # Ожидаем, что задача не найдена

# Тест для удаления задачи
def test_delete_task():
    response = client.delete("/api/tasks/NewImportantTask")
    assert response.status_code == 200  # Ожидаем, что задача была удалена

# Негативный тест для удаления несуществующей задачи
def test_delete_nonexistent_task():
    response = client.delete("/api/tasks/999")  # Предполагаем, что задача с id 999 не существует
    assert response.status_code == 404  # Ожидаем, что задача не найдена

################################################################TESTS FOR COMMENTS################################################################

# # Негативный тест для создания комментария с некорректными данными
# def test_create_comment_invalid_data():
#     response = client.post(
#         "/api/comments",
#         json={
#             "task_id": 1,
#             "user_id": 13,
#             "comment": "",  # Пустой комментарий
#         },
#     )
#     assert response.status_code == 422  # Ожидаем ошибку валидации данных

# Тест для создания нового комментария
def test_create_comment(setup_db_for_test_comments):
    response = client.post(
        "/api/comments",
        json={
            "task_id": 1,
            "user_id": 1,
            "comment": "Some random comment about task",
        },
    )
    assert response.status_code == 201  # Ожидаем, что комментарий был создан
    assert response.json()["comment"] == "Some random comment about task"

# Тест для получения комментария по уникальному id
def test_get_comment_by_id():
    response = client.get("/api/comments/1")
    assert response.status_code == 200  # Ожидаем успешный ответ
    assert response.json()["id"] == 1  # Проверяем, что получен правильный комментарий

# Негативный тест для получения несуществующего комментария
def test_get_nonexistent_comment():
    response = client.get("/api/comments/999")  # Предполагаем, что комментарий с id 999 не существует
    assert response.status_code == 404  # Ожидаем, что комментарий не найден

# Тест для получения всех комментариев для задачи
def test_get_comments_for_task():
    response = client.get("/api/comments/task/1")
    assert response.status_code == 200  # Ожидаем успешный ответ
    assert isinstance(response.json(), list)  # Ожидаем, что ответ - это список

# Тест для изменения комментария
def test_update_comment():
    response = client.put(
        "/api/comments/1",
        json={
            "comment": "Updated comment about task"
        },
    )
    assert response.status_code == 200  # Ожидаем успешный ответ
    assert response.json()["comment"] == "Updated comment about task"

# Негативный тест для изменения несуществующего комментария
def test_update_nonexistent_comment():
    response = client.put(
        "/api/comments/999",
        json={
            "comment": "Updated comment about task"
        },
    )
    assert response.status_code == 404  # Ожидаем, что комментарий не найден

# Тест для удаления комментария
def test_delete_comment():
    response = client.delete("/api/comments/1")
    assert response.status_code == 204  # Ожидаем, что комментарий был удален

# Негативный тест для удаления несуществующего комментария
def test_delete_nonexistent_comment():
    response = client.delete("/api/comments/999")  # Предполагаем, что комментарий с id 999 не существует
    assert response.status_code == 404  # Ожидаем, что комментарий не найден

################################################################TESTS FOR PROJECT MEMEBERS################################################################

# Тест для добавления нового участника проекта
def test_add_project_member():
    response = client.post(
        "/api/project_members",
        json={
            "project_id": 1,
            "user_id": 4,
            "role": "LEAD",
        },
    )
    assert response.status_code == 201  # Ожидаем, что участник проекта был добавлен
    assert response.json()["role"] == "LEAD"

# Тест для получения всех участников проекта с определенным id
def test_get_project_members():
    response = client.get("/api/project_members/project/1")
    assert response.status_code == 200  # Ожидаем успешный ответ
    assert isinstance(response.json(), list)  # Ожидаем, что ответ - это список

# # Негативный тест для получения участников несуществующего проекта
# def test_get_nonexistent_project_members():
#     response = client.get("/api/project_members/project/999")  # Предполагаем, что проект с id 999 не существует
#     assert response.status_code == 404  # Ожидаем, что проект не найден

# Тест для изменения параметров участника проекта
def test_update_project_member():
    response = client.put(
        "/api/project_members/1/4",
        json={
            "project_id": 1,
            "user_id": 4,
            "role": "MANAGER",
        },
    )
    assert response.status_code == 200  # Ожидаем успешный ответ
    assert response.json()["role"] == "MANAGER"

# Негативный тест для изменения параметров несуществующего участника проекта
def test_update_nonexistent_project_member():
    response = client.put(
        "/api/project_members/999/4",
        json={
            "project_id": 1,
            "user_id": 4,
            "role": "MANAGER",
        },
    )
    assert response.status_code == 404  # Ожидаем, что участник не найден

# Тест для удаления участника проекта
def test_delete_project_member():
    response = client.delete("/api/project_members/1/4")
    assert response.status_code == 204  # Ожидаем, что участник проекта был удален

# Негативный тест для удаления несуществующего участника проекта
def test_delete_nonexistent_project_member():
    response = client.delete("/api/project_members/999/4")  # Предполагаем, что участник с id 999 не существует
    assert response.status_code == 404  # Ожидаем, что участник не найден

################################################################TESTS FOR TASK DESTRIBUTION################################################################

################################################################TESTS FOR TASK RANKING################################################################