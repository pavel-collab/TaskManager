from fastapi import FastAPI, HTTPException
from app.db import Base, engine
from app.routes import task_routes
from app.routes import project_routes
from app.routes import user_routes
from app.routes.user_routes import verify_password
from datetime import datetime, timedelta
import jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

SECRET_KEY = "your_secret_key"  #! Испортировать из переменных окружения
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Функция для создания токена
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# ОAUTH2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(task_routes.router, prefix="/api", tags=["tasks"])
app.include_router(user_routes.router, prefix="/api", tags=["users"])
app.include_router(project_routes.router, prefix="/api", tags=["projects"])

@app.get("/")
def read_root():
    return {"message": "Welcome to task manager API"}

# Регистрация пользователя
@app.post("/register")
def register(username: str, email: str, password: str):
    db: Session = SessionLocal()
    hashed_password = hash_password(password)
    new_user = User(username=username, email=email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"msg": "User registered successfully"}

# Авторизация и получение токена
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    db: Session = SessionLocal()
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}