### Запуск
Запускаем базу данных в докере
```
docker-compose up -d
```
Можно убедиться, что база поднялась
```
docker exec -it task-trasker-db psql postgresql://postgres:1234@localhost:5432/
```

Запускаем приложение
```
uvicorn main:app --reload
```

Используем скрипт, чтобы заполнить базу данными для демонстрации.
```
./scripts/fill_db.py
```

### Using Swagger UI
Go to the http://localhost:8000/docs

### Requests


#### Работа с пользователями

Создание пользователя
```
curl -X POST "http://127.0.0.1:8000/api/users/" \
    -H "Content-Type: application/json" \
    -d "{\"username\": \"john_doe\", \
         \"email\": \"john@example.com\", \
         \"password\": \"password123\", \
         \"role\": \"DEVELOPER\"}"
```
Получить список всех пользователей
```
curl -X GET "http://127.0.0.1:8000/api/users/"
```
Получить пользователя по id
```
curl -X GET "http://127.0.0.1:8000/api/users/1"
```
Изменить данные пользователя
```
curl -X PUT "http://localhost:8000/api/users/1" \
      -H "Content-Type: application/json" \
      -d "{\"username\": \"john_doe\", \
           \"email\": \"john@example.com\", \
           \"password\": \"password123\", \
           \"role\": \"DEVELOPER\"}"
```
Удаление пользователя
```
curl -X DELETE "http://localhost:8000/api/users/john_doe" 
```

#### Работа с проектами

Создать проект
```
curl -X POST "http://127.0.0.1:8000/api/projects/" \
    -H "Content-Type: application/json" \
    -d "{\"title\": \"Project 1\", \
         \"description\": \"My first project\", \
         \"owner_id\": 3, \
         \"status\": \"TODO\", \
         \"project_start_date\": \"2024-09-01T00:00:00\", \
         \"project_end_date\": \"2024-09-30T00:00:00\"}"
```
Список всех проектов
```
curl -X GET "http://127.0.0.1:8000/api/projects/"
```
Получить проект по id
```
curl -X GET "http://127.0.0.1:8000/api/projects/1"
```
Обновление данных проекта
```
curl -X PUT "http://localhost:8000/api/projects/1" \
    -H "Content-Type: application/json" \
    -d "{\"title\": \"Project new\", \
         \"description\": \"My first project\", \
         \"owner_id\": 3, \
         \"status\": \"TODO\", \
         \"project_start_date\": \"2024-09-01T00:00:00\", \
         \"project_end_date\": \"2024-09-30T00:00:00\"}"
```
Удаление проекта
```
curl -X DELETE "http://localhost:8000/api/projects/ProjectTitle_1"
```

#### Работа с задачами

Создать задачу
```
curl -X POST "http://127.0.0.1:8000/api/tasks/" \
    -H "Content-Type: application/json" \
    -d "{\"title\": \"Task 1\", \
         \"description\": \"Complete the API\", \
         \"status\": \"TODO\", \
         \"project_id\": 1, \
         \"complexity\": \"LOW\", \
         \"assign_id\": 1, \
         \"task_start_date\": \"2024-09-01T00:00:00\", \
         \"task_end_date\": \"2024-09-15T00:00:00\"}"
```
Получить список всех задач
```
curl -X GET "http://127.0.0.1:8000/api/tasks/"
```
Получить задачу по id
```
curl -X GET "http://127.0.0.1:8000/api/tasks/1"
```
Изменить параметры задачи
```
curl -X PUT "http://localhost:8000/api/tasks/1" \
     -H "Content-Type: application/json" \
     -d "{\"title\": \"NewImportantTask\", \
         \"description\": \"Complete the API\", \
         \"status\": \"TODO\", \
         \"project_id\": 1, \
         \"complexity\": \"LOW\", \
         \"assign_id\": 1, \
         \"task_start_date\": \"2024-09-01T00:00:00\", \
         \"task_end_date\": \"2024-09-15T00:00:00\"}"
```
Удалить задачу
```
curl -X DELETE "http://localhost:8000/api/tasks/NewImportantTask"
```

#### Работа с комментариями

Создать новую запись
```
curl -X POST "http://localhost:8000/api/comments" \
        -H "Content-Type: application/json" \
        -d "{\"task_id\": 1, \
             \"user_id\": 13, \
             \"comment\": \"Some random comment about task\"}"
```
Получить комментарий по уникальному id
```
curl -X GET http://localhost:8000/api/comments/3
```
Получить все комментарии для задачи
```
curl -X GET http://localhost:8000/api/comments/task/1
```
Изменить комментарий
```
curl -X POST "http://localhost:8000/api/comments/1" \
        -H "Content-Type: application/json" \
        -d "{\"task_id\": \"1", \
             \"user_id\": \"13", \
             \"comment\": \"Some random comment about task"}"
```
Удалить комментарий
```
curl -X DELETE http://localhost:8000/comments/1
```

#### Работа с членами проекта

Добавление нового участника проекта
```
curl -X POST "http://localhost:8000/api/project_members" \
        -H "Content-Type: application/json" \
        -d "{\"project_id\": 1, \
             \"user_id\": 4, \
             \"role\": \"LEAD\"}"
```
Получить всех участников проекта с определенным id
```
curl -X GET "http://localhost:8000/api/project_members/project/1"
```
Изменить параметры некоторого пользователя
```
curl -X PUT "http://localhost:8000/api/project_members/1/4" \
        -H "Content-Type: application/json" \
        -d "{\"project_id\": 1, \
             \"user_id\": 4, \
             \"role\": \"MANAGER\"}"
```
Удаление
```
curl -X DELETE http://localhost:8000/api/project_members/1/4
```