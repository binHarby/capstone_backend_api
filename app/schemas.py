from pydantic import BaseModel, EmailStr
from datetime import datetime,date
from typing import Optional, List
from pydantic.types import conint
from pydantic import validator
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
    food_entry_id: int
    food_name: str
    cals_per_serv: float 
    servings: float
    total_cals: int
    fat: int
    protein: int
    created_at: datetime
class FoodReqBase(BaseModel):
    food_name: str
    cals_per_serv: float
    servings: float
    total_cals: int
    fat: int
    carbs: int
    protein: int
    created_at: datetime=dt.datetime.now(dt.timezone.utc)

class GetFoodRes(FoodResBase):
    user_id: int
class GetFoodReq(BaseModel):
    frm: date
    too: date

class PostFoodRes(FoodResBase):
    user_id: int
class PostFoodReq(FoodReqBase):
    user_id: Optional[int]

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
#-----------------------------------
## Restrictions
class RestPropReq(BaseModel):
    comp_1: Optional[str]
    comp_2: Optional[str]
    comp_3: Optional[str]
    comp_4: Optional[str]
    comp_5: Optional[str]
    comp_6: Optional[str]
    comp_7: Optional[str]
    comp_8: Optional[str]
    comp_9: Optional[str]
    comp_10: Optional[str]
class PostRestReq(BaseModel):
    name: str
    no_rules: int
    traces: bool
    minerals: bool
    vitamins: bool
    macros: bool
    description: str
    created_at: datetime=dt.datetime.now(dt.timezone.utc)
    updated_at: datetime=dt.datetime.now(dt.timezone.utc)
    res_prop: Optional[RestPropReq]
class DeleteRestReq(BaseModel):
    id: Optional[int]
    name: Optional[str]
    @validator('name',always=True)
    def check_name_or_id(cls,name,values):
        if not values.get('id') and not name:
            raise ValueError('Either name or id is required')
        return name
class UpdateRestReq(BaseModel):
    id: Optional[int]
    name: Optional[str]
    no_rules: Optional[int]
    traces: Optional[bool]
    minerals: Optional[bool]
    vitamins: Optional[bool]
    macros: Optional[bool]
    description: Optional[str]
    res_prop: Optional[RestPropReq]
    updated_at: datetime=dt.datetime.now(dt.timezone.utc)
    @validator('name',always=True)
    def check_name_or_id(cls,name,values):
        if not values.get('id') and not name:
            raise ValueError('Either name or id is required')
        return name
class GetRestReq(BaseModel):
    name: Optional[str]
    id: Optional[int]
    alll: Optional[bool]
    @validator('alll',always=True)
    def check_name_or_alll(cls,alll,values):
        if alll and values.get('id'):
            raise ValueError('Either alll xor [name/id] is required')
        if  values.get('name') and alll:
            raise ValueError('Either alll xor [name/id] is required')
        if  not values.get('name') and not alll and not values.get('id'):
            raise ValueError('Either alll xor [name/id] is required')

        return alll
