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

# генерируем рандомную дату
generate_random_date() {
    local start_date="$1"
    local end_date="$2"
    
    # Convert dates to seconds since epoch
    local start_seconds=$(date -d "$start_date" +%s)
    local end_seconds=$(date -d "$end_date" +%s)
    
    # Calculate the difference in seconds
    local diff_seconds=$((end_seconds - start_seconds))
    
    if [ $diff_seconds -lt 0 ]; then
        echo "Error: End date must be later than start date" >&2
        return 1
    fi
    
    # Generate a random number of seconds within the range
    local random_seconds=$((RANDOM % (diff_seconds + 1) + start_seconds))
    
    # Convert random seconds back to date format
    local random_date=$(date -d "@$random_seconds" +"%Y-%m-%dT00:00:00")
    
    echo "$random_date"
}

roles=("LEAD" "DEVELOPER" "TESTER" "MANAGER" "DELIVERY")
# генерируем 200 пользователей
for i in {1..200}; do
    user_name="User_$i"
    user_password="password12$i"
    user_email=$(generate_random_email)

    random_role=$(printf "%s\n" "${roles[@]}" | shuf -n 1)

    curl -X POST "http://$host:$port/api/users/" \
        -H "Content-Type: application/json" \
        -d "{\"username\": \"$user_name\", \
             \"email\": \"$user_email\", \
             \"password\": \"$user_password\", \
             \"role\": \"$random_role\"}"
done

status=("TODO" "IN_PROGRESS" "DONE")
# генерируем проекты
for i in {1..20}; do
    project_title="ProjectTitle_$i"
    description=$(generate_random_string "$length")
    owner_id=$(generate_random_number 200)

    # Выбор случайной строки
    random_status=$(printf "%s\n" "${status[@]}" | shuf -n 1)

    random_start_date=$(generate_random_date "2023-01-01" "2023-01-31")
    random_end_date=$(generate_random_date "2024-01-01" "2025-12-31")

    curl -X POST "http://$host:$port/api/projects/" \
        -H "Content-Type: application/json" \
        -d "{\"title\": \"$project_title\", \
             \"description\": \"$description\", \
             \"owner_id\": $owner_id, \
             \"status\": \"$random_status\", \
             \"project_start_date\": \"$random_start_date\", \
             \"project_end_date\": \"$random_end_date\"}"
done

status=("TODO" "IN_PROGRESS" "DONE")
complexity=("LOW" "MEDIUM" "HIGH")
# генерируем задачи
for i in {1..50}; do
    task_title="Task_$i"
    description=$(generate_random_string "$length")
    project_id=$(generate_random_number 20)
    assign_id=$(generate_random_number 200)

    # Выбор случайной строки
    random_status=$(printf "%s\n" "${status[@]}" | shuf -n 1)
    random_complexity=$(printf "%s\n" "${complexity[@]}" | shuf -n 1)

    random_start_date=$(generate_random_date "2023-02-01" "2023-10-31")
    random_end_date=$(generate_random_date "2023-12-01" "2025-12-31")

    curl -X POST "http://$host:$port/api/tasks/" \
        -H "Content-Type: application/json" \
        -d "{\"title\": \"$task_title\", \
             \"description\": \"$description\", \
             \"status\": \"$random_status\", \
             \"project_id\": $project_id, \
             \"complexity\": \"$random_complexity\", \
             \"assign_id\": $assign_id, \
             \"task_start_date\": \"$random_start_date\", \
             \"task_end_date\": \"$random_end_date\"}"
done

for i in {1..100}; do
    random_task_id=$(generate_random_number 50)
    random_user_id=$(generate_random_number 200)
    random_comment=$(generate_random_string 200)

    curl -X POST "http://$host:$port/api/comments" \
        -H "Content-Type: application/json" \
        -d "{\"task_id\": \"$random_task_id\", \
             \"user_id\": \"$random_user_id\", \
             \"comment\": \"$random_comment\"}"
done

for i in {1..20}; do
    random_project_id=$(generate_random_number 20)
    random_user_id=$(generate_random_number 200)
    random_role=$(printf "%s\n" "${roles[@]}" | shuf -n 1)

    curl -X POST "http://$host:$port/api/project_members" \
        -H "Content-Type: application/json" \
        -d "{\"project_id\": \"$random_project_id\", \
             \"user_id\": \"$random_user_id\", \
             \"role\": \"$random_role\"}"
done