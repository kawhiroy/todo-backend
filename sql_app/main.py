# URLと対応する処理をするためのファイル
from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException,status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from passlib.context import CryptContext
from database import SessionLocal, engine
import crud, models, schemas

models.Base.metadata.create_all(bind=engine)

SECRET_KEY = "a576669c5ce71fc0c5b11c2f091259f3645a32b85916a0b3041b6ffc56e6aed7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# あとでちゃんとしたDBとつなぐよ
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    },
}

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class User(BaseModel):
    username: str
    disabled: bool | None = None

class UserInDB(User):
    hashed_password: str

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2PasswordBearerクラスのインスタンス作成時に引数tokenUrlを渡す
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()

# 許可するオリジン一覧
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ハッシュを生成
def get_password_hash(password):
    return pwd_context.hash(password)

# ハッシュを検証
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# DBから該当のUser情報取得
def get_user(db: Session, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

# ユーザ認証
def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

# 新しいアクセストークンを生成
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
    
# 受信したトークンを検証して現在のユーザーを返す
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user



@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/user/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user

@app.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return [{"item_id": "Foo", "owner": current_user.username}]

# ユーザーの登録
@app.post("/users/", response_model=schemas.UserCreate)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# ユーザーの取得
@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users



@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# Todoの一覧表示
@app.get("/todos/", response_model=list[schemas.Todo])
def read_todos(limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_todos(db, limit=limit)


# Todoの追加
@app.post("/todos/", response_model=schemas.Todo)
def add_todo(todo: schemas.TodoCreate, db: Session = Depends(get_db)):
    return crud.create_todo(db, todo)


# Todoの編集
@app.put("/todos/{todo_id}", response_model=schemas.Todo)
async def edit_todo(
    todo_id: int, new_todo: schemas.TodoUpdate, db: Session = Depends(get_db)
):
    return crud.update_todo(db, todo_id, new_todo)


# Todoの削除
@app.delete("/todos/{todo_id}")
async def remove_todo(todo_id: int, db: Session = Depends(get_db)):
    return crud.delete_todo(db, todo_id)
