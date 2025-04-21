from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.user import User
from pydantic import BaseModel
from passlib.context import CryptContext

# Создание маршрутизатора и шифрования паролей
router = APIRouter()
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

# Схема для валидации данных пользователя


class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    role: str
    rating: int

# TODO: сделать множество классов для обновления пользовательской
# информации, либо сделать поля необязательными


class UserUpdate(BaseModel):
    username: str = None
    email: str = None

# Функция добавления нового пользователя


@router.post('/users/')
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = pwd_context.hash(user.password)
    db_user = User(username=user.username,
                   email=user.email,
                   hashed_password=hashed_password,
                   role=user.role,
                   rating=user.rating)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {'message': 'User created', 'user': db_user}

# Функция для получения всех пользователей


@router.get('/users/')
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

# TODO: тут можно сделать запрос конкретного польщователя через агргументы запроса
# Функция для получения конкретного пользователя по id
@router.get('/users/{user_id}')
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    return user

# Функция для обновления информации о пользователе
@router.put('/users/{user_id}')
def update_user(user_id: int, user_update: UserUpdate,
                db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail='User not found')

    # Обновляем только те поля, которые были предоставлены
    user_data = user_update.dict(exclude_unset=True)
    for key, value in user_data.items():
        if value is not None:
            setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)
    return {'message': 'User updated', 'user': db_user}

# TODO: добавить каскадное удаление соответствующих сущностей
# Функция для удаления пользователя
@router.delete('/users/{username}')
def delete_user(username: str, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == username).first()
    if not db_user:
        raise HTTPException(status_code=404, detail='User not found')

    db.delete(db_user)
    db.commit()
    return {'message': 'User deleted'}

def get_user(username):
    db = next(get_db())
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return None
    return user