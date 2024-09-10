from sqlalchemy import Column, Integer, String
from backend.config.db import Base, engine

class Movie(Base):
  __tablename__="movies"

  movieId = Column(Integer, primary_key=True, index=True)
  moviename = Column(String(255), nullable=False)
  year = Column(String(255), nullable=False)

Base.metadata.create_all(bind=engine)