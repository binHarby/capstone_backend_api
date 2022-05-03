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
    age: int
    bmi: int
    cal_goal: int
    cal_diff: int
    cal_current: int
    tdee: int
    created_at: datetime
    updated_at: datetime
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
# History Schemas
## Food
class GetFoodReq(BaseModel):
    id: Optional[int]
    frm: date
    too: date
class GetFoodRes(BaseModel):

class PostFoodReq(BaseModel):

class PostFoodRes(BaseModel):

class UpdateFoodReq(BaseModel):

class UpdateFoodRes(BaseModel):


class DeleteFoodReq(BaseModel):

class DeleteFoodRes(BaseModel):


## Activties

class GetActivitiesReq(BaseModel):
    id: Optional[int]
    frm: date
    too: date
class GetActivitiesRes(BaseModel):

class PostActivitiesReq(BaseModel):

class PostActivitiesRes(BaseModel):

class UpdateActivitiesReq(BaseModel):

class UpdateActivitiesRes(BaseModel):


class DeleteActivitiesReq(BaseModel):

class DeleteActivitiesRes(BaseModel):
## Meds

class GetMedsReq(BaseModel):
    id: Optional[int]
    frm: date
    too: date
class GetMedsRes(BaseModel):

class PostMedsReq(BaseModel):

class PostMedsRes(BaseModel):

class UpdateMedsReq(BaseModel):

class UpdateMedsRes(BaseModel):


class DeleteMedsReq(BaseModel):

class DeleteMedsRes(BaseModel):
