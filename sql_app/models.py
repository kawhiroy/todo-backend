# DBに登録するテーブルやカラムを設定するためのファイル
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


# class User(Base):
#     __tablename__ = "users"

#     id = Column(Integer, primary_key=True, index=True)
#     email = Column(String, unique=True, index=True)
#     hashed_password = Column(String)
#     is_active = Column(Boolean, default=True)

#     tasks = relationship("Item", back_populates="owner")


# Todoテーブルの定義
class Todo(Base):
    __tablename__ = "tasks"  # テーブルの名前"tasks"をSQLAlchemyに伝える

    id = Column(Integer, primary_key=True, index=True)  # 主キー
    content = Column(String, index=True)
    deadline = Column(String, index=True)
