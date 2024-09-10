from pydantic import BaseModel
from typing import Union


class UserBase(BaseModel):
    userName: str
    userPassword: Union[str, None]

    class Config:
      from_attributes = True