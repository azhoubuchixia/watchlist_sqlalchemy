from pydantic import BaseModel
from typing import Union


class MovieBase(BaseModel):
  moviename:Union[str,None]
  year:Union[str,None]

  class Config:
    from_attributes = True