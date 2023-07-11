# DBに登録するテーブルやカラムを設定するためのファイル
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, MetaData
from sqlalchemy.orm import relationship

from database import Base

metadata = MetaData()

# Userテーブルの定義
class User(Base):
    __tablename__ = "users"  # テーブルの名前"users"をSQLAlchemyに伝える

    user_id = Column(Integer, primary_key=True, autoincrement=True)  # 主キー
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    disabled = Column(Boolean, default=False)

    todos = relationship("Todo", back_populates="user")


# Todoテーブルの定義
class Todo(Base):
    __tablename__ = "todos"  

    id = Column(Integer, primary_key=True, index=True)  
    content = Column(String, index=True)
    deadline = Column(String, index=True)
    checked = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey('users.user_id'))

    user = relationship("User", back_populates="todos")
