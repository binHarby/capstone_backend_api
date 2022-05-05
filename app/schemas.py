from pydantic import BaseModel, EmailStr
from datetime import datetime,date
from typing import Optional, List
from pydantic.types import conint
import datetime as dt
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
    created_at: datetime=dt.datetime.now(dt.timezone.utc)
    updated_at: datetime=dt.datetime.now(dt.timezone.utc)
class UserUpdate(BaseModel):
    #id: Optional[int] 
    email: Optional[EmailStr]
    password: Optional[str]
    gender: Optional[str]
    confpassword: Optional[str]
    birthday: Optional[str]
    bloodtype: Optional[str]
    weight: Optional[int]
    height: Optional[float]
    cal_diff: Optional[int]
    activity: Optional[int]
    updated_at: datetime=dt.datetime.now(dt.timezone.utc)

class UserLogin(UserBase):
    password: str
class UserDelete(BaseModel):
    id: int
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
class FoodResBase (BaseModel):
    food_name: str
    cals_per_serv: str
    servings: float
    total_cals: int
    fat: int
    protein: int
    created_at: datetime
    food_entry_id: int

class GetFoodReq(BaseModel):
    user_id: Optional[int]
    frm: date
    too: date
class GetFoodRes(FoodResBase):
    user_id: int

#class PostFoodReq(BaseModel):
#
#class PostFoodRes(BaseModel):
#
#class UpdateFoodReq(BaseModel):
#
#class UpdateFoodRes(BaseModel):
#
#
#class DeleteFoodReq(BaseModel):
#
#class DeleteFoodRes(BaseModel):


## Activties

class GetActivitiesReq(BaseModel):
    id: Optional[int]
    frm: date
    too: date
#class GetActivitiesRes(BaseModel):
#
#class PostActivitiesReq(BaseModel):
#
#class PostActivitiesRes(BaseModel):
#
#class UpdateActivitiesReq(BaseModel):
#
#class UpdateActivitiesRes(BaseModel):
#
#
#class DeleteActivitiesReq(BaseModel):
#
#class DeleteActivitiesRes(BaseModel):
## Meds

#class GetMedsReq(BaseModel):
#    id: Optional[int]
#    frm: date
#    too: date
#class GetMedsRes(BaseModel):
#
#class PostMedsReq(BaseModel):
#
#class PostMedsRes(BaseModel):
#
#class UpdateMedsReq(BaseModel):
#
#class UpdateMedsRes(BaseModel):
#
#
#class DeleteMedsReq(BaseModel):
#
#class DeleteMedsRes(BaseModel):
