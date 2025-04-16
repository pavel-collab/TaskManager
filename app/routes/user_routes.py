from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.user import User
from pydantic import BaseModel
from passlib.context import CryptContext

# Создание маршрутизатора и шифрования паролей
router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Схема для валидации данных пользователя
class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    role: str

# Функция добавления нового пользователя
@router.post("/users/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = pwd_context.hash(user.password)
    db_user = User(username=user.username, 
                   email=user.email, 
                   hashed_password=hashed_password,
                   role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message": "User created", "user": db_user}

# Функция для получения всех пользователей
@router.get("/users/")
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

# Функция для получения конкретного пользователя по id
@router.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user