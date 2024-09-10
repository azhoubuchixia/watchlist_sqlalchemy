from fastapi import FastAPI
from backend.api.movie import movie_api
from backend.api.user import user_api

app=FastAPI()
app.include_router(movie_api,prefix="/movie")
app.include_router(user_api,prefix="/user")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(
        "main:app",
        host='127.0.0.1',
        port=8083,
        log_level="debug",
        reload=True,
    )