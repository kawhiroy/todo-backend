# DBに登録するテーブルやカラムを設定するためのファイル
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from database import Base


# Todoテーブルの定義
class Todo(Base):
    __tablename__ = "todos"  # テーブルの名前"tasks"をSQLAlchemyに伝える

    id = Column(Integer, primary_key=True, index=True)  # 主キー
    content = Column(String, index=True)
    deadline = Column(String, index=True)
    checked = Column(Boolean, index=True, default=False)
