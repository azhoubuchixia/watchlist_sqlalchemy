from fastapi.security import OAuth2PasswordRequestForm
from passlib.hash import bcrypt
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from backend.models.user import User
from backend.schemas.user import UserBase
from backend.config.db import SessionLocal
from backend.config.token import *


user_api=APIRouter(tags=['用户'])

def get_db():
  try:
    db = SessionLocal()
    yield db
  finally:
    db.close()

@user_api.post("/register", summary="注册")
async def user_register(user_form: UserBase, db: Session = Depends(get_db) ):
  user_dict = user_form.model_dump(exclude_unset=True)  #转换成字典类型
  userName=user_dict['userName']
  existing_user=db.query(User).filter(User.userName==userName).first()
  if existing_user :
    raise HTTPException(status_code=404, detail="用户已存在，请更换后重试！")
  
  # 创建新用户对象，加密密码
  new_user_data = user_dict.copy()
  plain_password = new_user_data.pop('userPassword')  # 假设密码字段名为 userPassword
  hashed_password = bcrypt.hash(plain_password)  # 使用 bcrypt 生成哈希密码
  new_user_data['userPassword'] = hashed_password

  new_user = User(**new_user_data)

  # 添加到数据库提交会话
  try:
    db.add(new_user)
    db.commit()
  except Exception as e:
    db.rollback()
    raise HTTPException(status_code=500, detail=str(e))
    
  userData = db.query(User).filter(User.userName == userName).first()

    # 返回增加成功后的信息
  return {
    "msg": "增加成功",
    "data": userData
  } 


@user_api.post("/login", summary="登录")
async def user_login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.userName == form_data.username).first()
    if user:
        if bcrypt.verify(form_data.password, user.userPassword):
            return JSONResponse(
               status_code=200,
               content={
                "msg": "登录成功",
                "access_token": create_access_token({"sub": user.userName}),
                "token_type": "bearer"}
              )
    else:
      raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
