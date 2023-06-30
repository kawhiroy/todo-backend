# DBのコマンドを投げるためのファイル

# パラメータの型を宣言し、関数での型チェックと補完をする
from fastapi import HTTPException
from sqlalchemy.orm import Session

import models, schemas


# 単一のTodoを取得(READ)
def get_todo(db: Session, todo_id: int):
    return db.query(models.Todo).filter(models.Todo.id == todo_id).first()


# Todo一覧を取得(READ)
def get_todos(db: Session, limit: int = 100):
    return db.query(models.Todo).limit(limit).all()


# Todoを作成(CREATE)
def create_todo(db: Session, todo: schemas.TodoCreate):
    db_todo = models.Todo(**todo.dict())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


def update_todo(db: Session, todo_id: int, new_todo: schemas.TodoUpdate):
    db_todo = get_todo(db, todo_id)  # 存在しない場合にはget_todo関数内で例外が投げられる
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    db_todo.content = new_todo.content
    db_todo.deadline = new_todo.deadline
    db_todo.checked = new_todo.checked
    db.commit()
    db.refresh(db_todo)
    return db_todo


# Todoを削除(DELETE)
def delete_todo(db: Session, todo_id: int):
    db_todo = get_todo(db, todo_id)
    db.delete(db_todo)
    db.commit()
