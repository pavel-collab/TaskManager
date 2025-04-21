import random
import string
from datetime import datetime

ROLES = ['LEAD', 'DEVELOPER', 'TESTER', 'MANAGER', 'DELIVERY']
STATUS = ['TODO', 'IN_PROGRESS', 'DONE']
COMPLEXITY = ['LOW', 'MEDIUM', 'HIGH']


def generate_random_string(length):
    """Генерирует случайную строку заданной длины."""
    if length <= 0:
        return ''

    characters = string.ascii_letters + string.digits  # Буквы и цифры
    random_string = ''.join(random.choice(characters) for _ in range(length))

    return random_string


def generate_random_email():
    """Генерирует случайный валидный email адрес."""

    # Генерация случайной локальной части email
    # Длина локальной части от 5 до 10 символов
    local_part_length = random.randint(5, 10)
    local_part = ''.join(
        random.choices(
            string.ascii_lowercase +
            string.digits,
            k=local_part_length))

    # Генерация домена
    domains = ['example.com', 'test.com', 'mail.com', 'domain.com']
    domain = random.choice(domains)

    # Формирование email адреса
    email = f"{local_part}@{domain}"

    return email


def choose_random_element(input_list):
    """Выбирает случайный элемент из списка."""
    if not input_list:  # Проверка на пустой список
        return None

    random_element = random.choice(input_list)
    return random_element


def generate_random_date(start_date, end_date):
    """Генерирует случайную дату в заданном диапазоне."""
    # Преобразование дат в формат timestamp
    start_timestamp = start_date.timestamp()
    end_timestamp = end_date.timestamp()

    # Генерация случайного timestamp в заданном диапазоне
    random_timestamp = random.uniform(start_timestamp, end_timestamp)

    # Преобразование timestamp обратно в дату
    random_date = datetime.fromtimestamp(random_timestamp)

    return random_date


def helper_fill_users(client, n_users=10):
    for i in range(n_users):
        response = client.post(
            '/api/users/',
            json={
                'username': f"User_{i}",
                'email': generate_random_email(),
                'password': generate_random_string(10),
                'role': choose_random_element(ROLES),
                'rating': random.randint(0, 100)
            }
        )
        assert response.status_code == 200


def helper_fill_projects(client, n_projects=10):
    start_date = datetime(2020, 1, 1)  # Начальная дата
    end_date = datetime(2023, 12, 31)  # Конечная дата

    for i in range(n_projects):
        response = client.post(
            '/api/projects/',
            json={
                'title': f"Project_{i}",
                'description': generate_random_string(50),
                'owner_id': random.randint(1, 10),
                'status': choose_random_element(STATUS),
                'project_start_date': str(generate_random_date(start_date, end_date)),
                'project_end_date': str(generate_random_date(start_date, end_date))
            }
        )
        assert response.status_code == 200


def helper_fill_tasks(client, n_tasks=10):
    start_date = datetime(2020, 1, 1)  # Начальная дата
    end_date = datetime(2023, 12, 31)  # Конечная дата

    for i in range(n_tasks):
        response = client.post(
            '/api/tasks/',
            json={
                'title': f"Task_{i}",
                'description': generate_random_string(50),
                'status': choose_random_element(STATUS),
                'project_id': random.randint(1, 10),
                'complexity': choose_random_element(COMPLEXITY),
                'assign_id': random.randint(1, 10),
                'task_start_date': str(generate_random_date(start_date, end_date)),
                'task_end_date': str(generate_random_date(start_date, end_date))
            }
        )
        assert response.status_code == 200

# def helper_fill_comments(client, n_comments=10):
#     for i in range(n_comments):
#         response = client.post(
#             "/api/comments/",
#             json={
#                 "task_id": random.randint(1, 10),
#                 "user_id": random.randint(1, 10),
#                 "comment": generate_random_string(100)
#             }
#         )
#         assert response.status_code == 200

# def helper_fill_project_members(client, n_project_members=10):
#     for i in range(n_project_members):
#         response = client.post(
#             "/api/project_members/",
#             json={
#                 "project_id": random.randint(1, 10),
#                 "user_id": random.randint(1, 10),
#                 "role": choose_random_element(ROLES)
#             }
#         )
#         assert response.status_code == 200
