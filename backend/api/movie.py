from typing import List
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from backend.models.movie import Movie
from backend.config.db import SessionLocal
from backend.schemas.movie import MovieBase
from backend.config.token import get_current_user

movie_api = APIRouter(tags=['电影'],dependencies=[Depends(get_current_user)])

def get_db():
  try:
    db = SessionLocal()
    yield db
  finally:
    db.close()

@movie_api.get("/check_movie", summary="查看电影", response_model=List[MovieBase])
async def check_movies(db: Session = Depends(get_db)):
    movies = db.query(Movie).all()
    if not movies:
        raise HTTPException(status_code=400, detail="未找到！")

    movie_data = [MovieBase.model_dump(MovieBase.model_validate(mov)) for mov in movies]

    # 返回 JSON 响应
    return JSONResponse(
        status_code=200,
        content={"msg": "查询成功", "data": movie_data}
    )

@movie_api.post("/add_movie", summary="增加")
async def add_movie(movie_form: MovieBase, db: Session = Depends(get_db)):
    # 转成字典类型
    movie_dict = movie_form.model_dump(exclude_unset=True)
    movie_name = movie_dict['moviename']
    existing_movie = db.query(Movie).filter(Movie.moviename == movie_name).first()
    if existing_movie:
        raise HTTPException(status_code=404, detail="名字已存在，请更换后重试")

    new_movie_data = movie_form.model_dump(exclude_unset=True)
    new_movie = Movie(**new_movie_data)

    try:
        db.add(new_movie)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    movies_data = db.query(Movie).filter(Movie.moviename == movie_name).first()
    return {
        "msg": "增加成功",
        "data": movies_data
    }