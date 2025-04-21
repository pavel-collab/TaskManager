from datetime import datetime
from typing import Dict, List
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.task import Task
from app.utils.utils import Status, complexity_weight
from app.models.project import Project
from app.models.user import User
from app.models.project_members import ProjectMembers
from app.routes.auth import UserResponse, get_current_user

router = APIRouter()

# Схема для создания задачи


class TaskCreate(BaseModel):
    title: str
    description: str
    status: Status
    project_id: int
    complexity: str
    assign_id: int
    task_start_date: str
    task_end_date: str

# Функция для добавления новой задачи


@router.post('/tasks/')
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    # Проверяем, существует ли проект для этой задачи
    project = db.query(Project).filter(Project.id == task.project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail='Project not found')

    new_task = Task(title=task.title,
                    description=task.description,
                    status=task.status,
                    project_id=task.project_id,
                    complexity=task.complexity,
                    assign_id=task.assign_id,
                    task_start_date=task.task_start_date,
                    task_end_date=task.task_end_date)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return {'message': 'Task created', 'task': new_task}

# Функция для получения всех задач


@router.get('/tasks/')
def get_tasks(db: Session = Depends(get_db)):
    tasks = db.query(Task).all()
    return tasks

# TODO: изменить: получить задачу по названию
# Функция для получения конкретной задачи по id


@router.get('/tasks/{task_id}')
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail='Task not found')
    return task

# TODO: сделать так, чтобы можно было вносить частичные изменения
# Функция для обновления задачи


@router.put('/tasks/{task_id}')
def update_task(task_id: int, task_update: TaskCreate,
                db: Session = Depends(get_db)):
    """Update an existing task by ID.

    Args:
        task_id: The ID of the task to update
        task_update: The new task data
        db: Database session

    Returns:
        Updated task information

    Raises:
        HTTPException: If task not found or project not found

    """
    # Check if project exists
    project = db.query(Project).filter(
        Project.id == task_update.project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail='Project not found')

    # Find and update the task
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail='Task not found')

    # Update task fields
    task.title = task_update.title
    task.description = task_update.description
    task.status = task_update.status
    task.project_id = task_update.project_id

    db.commit()
    db.refresh(task)
    return {'message': 'Task updated', 'task': task}

# TODO: добавить каскадное удаление соответствующих сущностей
# Функция для удаления задачи


@router.delete('/tasks/{task_title}')
def delete_task(task_title: str, db: Session = Depends(get_db)):
    """Delete a task by ID.

    Args:
        task_id: The ID of the task to delete
        db: Database session

    Returns:
        Success message

    Raises:
        HTTPException: If task not found

    """
    task = db.query(Task).filter(Task.title == task_title).first()
    if not task:
        raise HTTPException(status_code=404, detail='Task not found')

    db.delete(task)
    db.commit()
    return {'message': 'Task deleted'}


@router.get('/auth/task-distribution')
def distribute_tasks(current_user: UserResponse = Depends(get_current_user),
                     db: Session = Depends(get_db)) -> Dict[int, List[int]]:
    users = db.query(User).all()
    tasks = db.query(Task).filter(Task.status == Status.TODO).all()

    # Загружаем все связи между пользователями и проектами
    project_members = db.query(ProjectMembers).all()
    project_user_map = {}  # project_id: set(user_id)
    for pm in project_members:
        project_user_map.setdefault(pm.project_id, set()).add(pm.user_id)

    # Подготовка информации о пользователях
    user_load = {
        user.id: {
            'rating': user.rating,
            'tasks': db.query(Task).filter(
                Task.assign_id == user.id,
                Task.status.in_([Status.IN_PROGRESS, Status.TODO])
            ).count(),
            'assigned_tasks': []
        }
        for user in users
    }

    # Сортировка задач по сложности (сложные первыми)
    tasks.sort(
        key=lambda t: complexity_weight.get(
            t.complexity,
            1),
        reverse=True)

    def assignment_score(user_id, task_difficulty):
        user = user_load[user_id]
        load_penalty = user['tasks']
        rating_bonus = user['rating']
        difficulty = complexity_weight.get(task_difficulty, 1)
        return rating_bonus / (1 + load_penalty * difficulty)

    for task in tasks:
        eligible_users = project_user_map.get(task.project_id, set())
        if not eligible_users:
            continue  # нет участников — задачу не назначаем

        best_user_id = max(
            eligible_users,
            key=lambda uid: assignment_score(uid, task.complexity)
        )

        user_load[best_user_id]['assigned_tasks'].append(task.id)
        user_load[best_user_id]['tasks'] += 1

    distribution_result = {
        user_id: info['assigned_tasks']
        for user_id, info in user_load.items()
        if info['assigned_tasks']
    }

    return distribution_result


@router.post('/auth/apply-distribution')
def apply_distribution(distribution: Dict[int, List[int]],
                       current_user: UserResponse = Depends(get_current_user),
                       db: Session = Depends(get_db)):
    try:
        for user_id, task_ids in distribution.items():
            # Обновляем assign_id у задач
            db.query(Task).filter(Task.id.in_(task_ids)).update(
                {Task.assign_id: user_id}, synchronize_session='fetch'
            )
        db.commit()
        return {'detail': 'Task assignment updated successfully.'}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500,
                            detail=f"Failed to update assignments: {str(e)}")


@router.get('/auth/ranked-tasks')
def get_ranked_tasks(db: Session = Depends(get_db),
                     current_user: UserResponse = Depends(get_current_user)) -> List[dict]:
    now = datetime.utcnow()

    tasks = db.query(Task).filter(Task.status.in_(
        [Status.TODO, Status.IN_PROGRESS])).all()

    def task_priority(task: Task):
        if task.task_start_date and task.task_start_date > now:
            return 0  # задача ещё не началась

        if not task.task_end_date:
            return 0.1  # минимальный приоритет, если нет дедлайна

        # Время до окончания в часах
        hours_left = (task.task_end_date - now).total_seconds() / 3600
        # защита от деления на ноль или прошлого
        hours_left = max(1, hours_left)

        difficulty = complexity_weight.get(task.complexity, 1)

        # Чем меньше времени и выше сложность — тем выше приоритет
        return round((difficulty / hours_left) * 100, 2)

    # чем выше score — тем выше в списке
    tasks.sort(key=task_priority, reverse=True)

    ranked_result = [
        {
            'id': task.id,
            'title': task.title,
            'start_date': task.task_start_date,
            'end_date': task.task_end_date,
            'difficulty': task.complexity,
            'status': task.status,
            'priority_score': task_priority(task)
        }
        for task in tasks
    ]

    return ranked_result
