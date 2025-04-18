### Архитектура базы

![Архитектура базы](/images/relationships.real.large.png)

### Запуск
Поднимаем приложение в докере с помощью docker-compose
```
docker-compose up --build -d
```

Используем скрипт, чтобы заполнить базу данными для демонстрации.
```
./scripts/fill_db.py
```

### Using Swagger UI
Go to the http://localhost:8080/docs

### Requests

#### Работа с пользователями

Создание пользователя
```
curl -X POST "http://127.0.0.1:8080/api/users/" \
    -H "Content-Type: application/json" \
    -d "{\"username\": \"john_doe\", \
         \"email\": \"john@example.com\", \
         \"password\": \"password123\", \
         \"role\": \"DEVELOPER\", \
         \"rating\": 20}"
```
Получить список всех пользователей
```
curl -X GET "http://127.0.0.1:8080/api/users/"
```
Получить пользователя по id
```
curl -X GET "http://127.0.0.1:8080/api/users/1"
```
Изменить данные пользователя
```
curl -X PUT "http://localhost:8080/api/users/1" \
      -H "Content-Type: application/json" \
      -d "{\"username\": \"john_doe\", \
           \"email\": \"john@example.com\", \
           \"password\": \"password123\", \
           \"role\": \"DEVELOPER\"}"
```
Удаление пользователя
```
curl -X DELETE "http://localhost:8080/api/users/john_doe" 
```

#### Работа с проектами

Создать проект
```
curl -X POST "http://127.0.0.1:8080/api/projects/" \
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
curl -X GET "http://127.0.0.1:8080/api/projects/"
```
Получить проект по id
```
curl -X GET "http://127.0.0.1:8080/api/projects/1"
```
Обновление данных проекта
```
curl -X PUT "http://localhost:8080/api/projects/1" \
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
curl -X DELETE "http://localhost:8080/api/projects/ProjectTitle_1"
```

#### Работа с задачами

Создать задачу
```
curl -X POST "http://127.0.0.1:8080/api/tasks/" \
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
curl -X GET "http://127.0.0.1:8080/api/tasks/"
```
Получить задачу по id
```
curl -X GET "http://127.0.0.1:8080/api/tasks/1"
```
Изменить параметры задачи
```
curl -X PUT "http://localhost:8080/api/tasks/1" \
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
curl -X DELETE "http://localhost:8080/api/tasks/NewImportantTask"
```

#### Работа с комментариями

Создать новую запись
```
curl -X POST "http://localhost:8080/api/comments" \
        -H "Content-Type: application/json" \
        -d "{\"task_id\": 1, \
             \"user_id\": 13, \
             \"comment\": \"Some random comment about task\"}"
```
Получить комментарий по уникальному id
```
curl -X GET http://localhost:8080/api/comments/3
```
Получить все комментарии для задачи
```
curl -X GET http://localhost:8080/api/comments/task/1
```
Изменить комментарий
```
curl -X POST "http://localhost:8080/api/comments/1" \
        -H "Content-Type: application/json" \
        -d "{\"task_id\": \"1", \
             \"user_id\": \"13", \
             \"comment\": \"Some random comment about task"}"
```
Удалить комментарий
```
curl -X DELETE http://localhost:8080/comments/1
```

#### Работа с членами проекта

Добавление нового участника проекта
```
curl -X POST "http://localhost:8080/api/project_members" \
        -H "Content-Type: application/json" \
        -d "{\"project_id\": 1, \
             \"user_id\": 4, \
             \"role\": \"LEAD\"}"
```
Получить всех участников проекта с определенным id
```
curl -X GET "http://localhost:8080/api/project_members/project/1"
```
Изменить параметры некоторого пользователя
```
curl -X PUT "http://localhost:8080/api/project_members/1/4" \
        -H "Content-Type: application/json" \
        -d "{\"project_id\": 1, \
             \"user_id\": 4, \
             \"role\": \"MANAGER\"}"
```
Удаление
```
curl -X DELETE http://localhost:8080/api/project_members/1/4
```

### Бизнес-задачи

Наша программа будет решать следующие бизнес-задачи

#### Оптимизация распределения задач

Алгоритм, который автоматически распределяет задачи между пользователями на основе их текущей загрузки и навыков.
Получаем наиболее оптимальное распределение открытых задач между пользователями. При этом мы учитываем рейтинг пользователя, сложность задачи,
количество задач, которыми занимается пользователь в данный момент и принадлежность пользователя к проекту, с которым связана задача.
```
curl -X GET "http://localhost:8080/api/task-distribution"
```

Результат работы алгоритма мы получаем в виде json соответствия: каждому ключу - идентификатору пользователя соответствуют идентификаторы задач, которые
стоит ему назначить. Далее мы можем это сделать отдельным запросом.
```
curl -X POST http://localhost:8080/api/apply-distribution \
    -H "Content-Type: application/json" \
    -d "{\"10\":[32,43,49], \
         \"24\":[5], \
         \"44\":[13], \
         \"74\":[38], \
         \"103\":[48], \
         \"115\":[29], \
         \"127\":[25], \
         \"186\":[42]}"
```

#### Система приоритетов задач

Алгоритм устанавливаем приоритеты для задач, учитывая сроки выполнения и сложность задачи.
```
curl -X GET "http://localhost:8080/api/ranked-tasks"
```
Аналогичный алгоритм для проектов
```
curl -X GET "http://localhost:8080/api/ranked-projects"
```

#### For developers

Python code formating. We're using pyformat 
```
pyformat -i -r -a --remove-all-unused-imports --remove-unused-variables ./
```
and check code quality via pylint
```
pylint ./ > pylint_report.txt
```