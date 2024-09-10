
from datetime import datetime, timedelta, timezone
from typing import Optional
from fastapi import Depends, HTTPException,status
import jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from backend.config.db import SessionLocal
from backend.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# 创建访问令牌（token）
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    # 令牌的主体
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    # 将过期时间添加到 to_encode 字典
    to_encode.update(dict(exp=expire))
    # 对 to_encode 字典进行编码，生成 JWT 字符串
    encoded_jwt = jwt.encode(
        to_encode, SECRET_KEY, ALGORITHM
    )
    return encoded_jwt

class CredentialsException(Exception):
    """自定义异常，用于处理凭证相关的错误。"""
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail
        super().__init__(f"Status Code: {status_code}, Detail: {detail}")

# 依赖项，从请求中获取当前有效的令牌
# 所有用户
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        if not username:
            raise CredentialsException(status_code=401, detail="Credentials are missing")
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    db = SessionLocal()
    try:
        user = db.query(User).filter(User.userName == username).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
    finally:
        db.close()
    return user
