#!/bin/bash

host="127.0.0.1"
port="8000"

length=30

# Функция для генерации случайной строки заданной длины
generate_random_string() {
    local length=$1
    # Генерация строки и возврат её
    tr -dc 'A-Za-z0-9' < /dev/urandom | head -c "$length"
}

# Функция для генерации случайного email-адреса
generate_random_email() {
    local username_length=8  # Длина имени пользователя
    local domain="example.com"  # Доменное имя

    # Генерируем случайное имя пользователя
    local username=$(generate_random_string "$username_length")

    # Формируем email-адрес
    echo "$username@$domain"
}

generate_random_number() {
    local max_value=$1
    # Генерация случайного числа
    echo $((RANDOM % $max_value + 1))
}

# генерируем 200 пользователей
for i in {1..200}; do
    user_name="User_$i"
    user_password="password12$i"
    user_email=$(generate_random_email)

    curl -X POST "http://$host:$port/api/users/" \
        -H "Content-Type: application/json" \
        -d "{\"username\": \"$user_name\", \"email\": \"$user_email\", \"password\": \"$user_password\"}"
done

# генерируем проекты
for i in {1..20}; do
    project_title="ProjectTitle_$i"
    description=$(generate_random_string "$length")
    owner_id=$(generate_random_number 200)

    curl -X POST "http://$host:$port/api/projects/" \
        -H "Content-Type: application/json" \
        -d "{\"title\": \"$project_title\", \"description\": \"$description\", \"owner_id\": $owner_id}"
done

status=("TODO" "IN_PROGRESS" "DONE")
# генерируем задачи
for i in {1..50}; do
    task_title="Task_$i"
    description=$(generate_random_string "$length")
    project_id=$(generate_random_number 20)

    # Выбор случайной строки
    random_status=$(printf "%s\n" "${status[@]}" | shuf -n 1)

    curl -X POST "http://$host:$port/api/tasks/" \
        -H "Content-Type: application/json" \
        -d "{\"title\": \"$task_title\", \"description\": \"$description\", \"status\": \"$random_status\", \"project_id\": $project_id}"
done