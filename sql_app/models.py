# DBに登録するテーブルやカラムを設定するためのファイル
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship

from database import Base

# Userテーブルの定義
class User(Base):
    __tablename__ = "users"  # テーブルの名前"users"をSQLAlchemyに伝える

    id = Column(Integer, primary_key=True, index=True)  # 主キー
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    todos = relationship("Todo", back_populates="owner")


# Todoテーブルの定義
class Todo(Base):
    __tablename__ = "todos"  

    id = Column(Integer, primary_key=True, index=True)  
    content = Column(String, index=True)
    deadline = Column(String, index=True)
    checked = Column(Boolean, index=True, default=False)

    user_id = Column(Integer, ForeignKey('users.id'))
    owner = relationship("User", back_populates="todos")
