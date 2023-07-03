# Pydanticモデルを設定するためのファイル
# 型定義している
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer

# OAuth2PasswordBearerクラスのインスタンス作成時に引数tokenUrlを渡す
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None

class UserInDB(User):
    hashed_password: str


class TodoBase(BaseModel):
    content: str
    deadline: str
    checked: bool


class TodoUpdate(BaseModel):
    content: str
    deadline: str
    checked: bool


class TodoCreate(TodoBase):
    pass


class Todo(TodoBase):
    id: int

    class Config:
        orm_mode = True
