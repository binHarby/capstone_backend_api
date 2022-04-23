from pydantic import BaseModel, EmailStr
from datetime import datetime,date
from typing import Optional, List
from pydantic.types import conint

class UserBase(BaseModel):
    email: EmailStr
class UserRes(UserBase):
    id: int
    password: str
    gender: str
    birthday: date 
    bloodtype: str
    weight: int
    height: float
    cal_diff: int
    age: int
    bmi: int
    main_cals: int
    cal_diff: int
    created_at: datetime
class UserCreate(UserBase):
    password: str
    gender:str
    confpassword: str
    birthday: str
    bloodtype: str
    weight: int
    height: float
    cal_diff: int=0
    activity: int
class UserLogin(UserBase):
    password: str
class Token(BaseModel):
    access_token: str
    token_type: str
class TokenData(BaseModel):
    id: Optional[str] = None
class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)

