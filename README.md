### Запуск
Запускаем базу данных в докере
```
docker-compose up
```
Можно убедиться, что база поднялась
```
docker exec -it task-trasker-db psql postgresql://postgres:1234@localhost:5432/
```

Запускаем приложение
```
uvicorn app.main:app --reload
```

### Using Swagger UI
Go to the http://localhost:8000/docs

### Requests

Создание пользователя
```
curl -X POST "http://127.0.0.1:8000/api/users/" -H "Content-Type: application/json" -d '{"username": "john_doe", "email": "john@example.com", "password": "password123"}'
```
Получить список всех пользователей
```
curl -X GET "http://127.0.0.1:8000/api/users/"
```
Получить пользователя по id
```
curl -X GET "http://127.0.0.1:8000/api/users/1"
```

Создать проект
```
curl -X POST "http://127.0.0.1:8000/api/projects/" -H "Content-Type: application/json" -d '{"title": "Project 1", "description": "My first project", "owner_id": 1}'
```
Список всех проектов
```
curl -X GET "http://127.0.0.1:8000/api/projects/"
```
Получить проект по id
```
curl -X GET "http://127.0.0.1:8000/api/projects/1"
```

Создать задачу
```
curl -X POST "http://127.0.0.1:8000/api/tasks/" -H "Content-Type: application/json" -d '{"title": "Task 1", "description": "Complete the API", "status": "TO_DO", "project_id": 1}'
```
Получить список всех задач
```
curl -X GET "http://127.0.0.1:8000/api/tasks/"
```
Получить задачу по id
```
curl -X GET "http://127.0.0.1:8000/api/tasks/1"
```