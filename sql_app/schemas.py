# Pydanticモデルを設定するためのファイル
# 型定義している
from pydantic import BaseModel


# BaseBodelクラスの子クラスTodoBase
class TodoBase(BaseModel):
    content: str
    deadline: str


class TodoCreate(TodoBase):
    pass


class Todo(TodoBase):
    id: int
    # owner_id: int

    class Config:
        orm_mode = True


# class UserBase(BaseModel):
#     email: str


# class UserCreate(UserBase):
#     password: str


# class User(UserBase):
#     id: int
#     is_active: bool
#     todos: list[Todo] = []

#     class Config:
#         orm_mode = True
