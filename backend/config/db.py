from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = (
    "mysql://root:123456@localhost/watchlist"
)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

# 创建数据库会话
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# 创建基类
Base = declarative_base()
