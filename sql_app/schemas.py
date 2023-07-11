# Pydanticモデルを設定するためのファイル
# 型定義している
from pydantic import BaseModel

# Todoリスト
class TodoBase(BaseModel):
    content: str
    deadline: str
    checked: bool

class TodoUpdate(TodoBase):
    pass

class TodoCreate(TodoBase):
    pass

class TodoCreateResponce(TodoBase):
    id: int

class Todo(TodoBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True


# ユーザー
class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str

class User(UserBase):
    user_id: int

    class Config:
        orm_mode = True

class UserAll(UserBase):
    hashed_password: str
    user_id: int

    class Config:
        orm_mode = True
