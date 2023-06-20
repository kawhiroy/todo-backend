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

    class Config:
        orm_mode = True
