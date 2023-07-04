# DBに登録するテーブルやカラムを設定するためのファイル
from sqlalchemy import Column, DateTime, Integer, String, Boolean
from sqlalchemy.orm import relationship

from database import Base

# Userテーブルの定義
class User(Base):
    __tablename__ = "users"  # テーブルの名前"users"をSQLAlchemyに伝える

    id = Column(Integer, primary_key=True, index=True)  # 主キー
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


# Todoテーブルの定義
class Todo(Base):
    __tablename__ = "todos"  

    id = Column(Integer, primary_key=True, index=True)  
    content = Column(String, index=True)
    deadline = Column(String, index=True)
    checked = Column(Boolean, index=True, default=False)
