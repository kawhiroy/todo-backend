# DBのコマンドを投げるためのファイル

# パラメータの型を宣言し、関数での型チェックと補完をする
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


# Todoを更新(UPDATE)
def update_todo(db: Session, todo_id: int, new_todo: schemas.Todo):
    todo = get_todo(db, todo_id)  #   idで指定したtodoを抽出
    todo.content = new_todo.content  #   todo.contentを更新
    todo.deadline = new_todo.deadline
    todo.checked = new_todo.checked
    db.commit()


# Todoを削除(DELETE)
def delete_todo(db: Session, todo_id: int):
    todo = get_todo(db, todo_id)
    db.delete(todo)
    db.commit()
