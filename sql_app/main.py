# URLと対応する処理をするためのファイル
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


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
