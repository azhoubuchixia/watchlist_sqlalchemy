from sqlalchemy import Column, Integer, String
from backend.config.db import Base, engine

class User(Base):
  __tablename__="users"

  userId = Column(Integer, primary_key=True)
  userName = Column(String(255), nullable=False, doc="用户姓名")
  userPassword = Column(String(255), nullable=False, doc="密码")

Base.metadata.create_all(bind=engine)