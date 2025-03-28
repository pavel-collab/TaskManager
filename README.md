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

### Requests

