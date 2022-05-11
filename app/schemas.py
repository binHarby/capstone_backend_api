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
    height: float
    age: int
    created_at: datetime
    updated_at: datetime
class UserCreate(UserBase):
    password: str
    gender:str
    confpassword: str
    birthday: str
    bloodtype: str
    height: float
    created_at: datetime=dt.datetime.now(dt.timezone.utc)
    updated_at: datetime=dt.datetime.now(dt.timezone.utc)
class UserUpdate(BaseModel):
    email: Optional[EmailStr]
    password: Optional[str]
    gender: Optional[str]
    confpassword: Optional[str]
    birthday: Optional[str]
    bloodtype: Optional[str]
    height: Optional[float]
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
class PostUserRestReq(BaseModel):
    # Need to account for a bulk insert at sign in
    res_id: int
    rule: int
class DeleteUserRestReq(BaseModel):
    user_res_id: int
class UpdateUserRestReq(BaseModel):
    user_res_id: int
    rule: int

class GetUserRestReq(BaseModel):
    user_res_id: Optional[int]
    alll: Optional[bool]
    @validator('alll',always=True)
    def check_name_or_alll(cls,alll,values):
        if alll and values.get('user_res_id'):
            raise ValueError('Either alll xor res_id is required')
        if  not values.get('user_res_id') and not alll:
            raise ValueError('Either alll xor res_id is required')

        return alll

## External APIs schemas
# Names
class ExapiNameReq(BaseModel):
    name: str
# UPC
class ExapiUPCReq(BaseModel):
    upc: str
# common models between State and Goal route
class MacrosBase(BaseModel):
    carb: Optional[int]
    sugar: Optional[int]
    fructose: Optional[int]
    lactose: Optional[int]
    protein: Optional[int]
    amino: Optional[int]
    fat: Optional[int]
    unsaturated: Optional[int]
    monounsaturated: Optional[int]
    polyunsaturated: Optional[int]
    saturated: Optional[int]
    fiber: Optional[int]
    trans: Optional[int]
class VitaminsBase(BaseModel):
    b: Optional[int]
    b_1: Optional[int]
    b_2: Optional[int]
    b_3: Optional[int]
    b_8: Optional[int]
    b_5: Optional[int]
    b_6: Optional[int]
    b_7: Optional[int]
    b_12: Optional[int]
    choline: Optional[int]
    a: Optional[int]
    c: Optional[int]
    d: Optional[int]
    d_2: Optional[int]
    d_3: Optional[int]
    k_1: Optional[int]
    k_2: Optional[int]
    k_3: Optional[int]
    k: Optional[int]
    e: Optional[int]
class TracesBase(BaseModel):
    boron: Optional[int]
    copper: Optional[int]
    selenium: Optional[int]
    maganese: Optional[int]
    fluorine: Optional[int]
    chromium: Optional[int]
    cobalt: Optional[int]
    iodine: Optional[int]
class MineralsBase(BaseModel):
    calcium: Optional[int]
    phosphorus: Optional[int]
    magnesium: Optional[int]
    sodium: Optional[int]
    potassium: Optional[int]
    iron: Optional[int]
    zinc: Optional[int]
class PostGeneralGoal(BaseModel):
    weight: int
    activity_lvl: int
    cal_diff: int =0
    cal_goal: Optional[int]
    control_lvl: Optional[str]='normal'
class UpdateGeneralGoal(BaseModel):
    weight: int
    activity_lvl: Optional[int]
    cal_diff: Optional[int]
    cal_goal: Optional[int]
    control_lvl: Optional[str]
class GeneralState(BaseModel):
    day: datetime=dt.datetime.now(dt.timezone.utc) 
    calories_consumed: Optional[int]=0
class MedsBase(BaseModel):
    updated_at: datetime=dt.datetime.now(dt.timezone.utc) 
    doses_taken: Optional[int]=0
    med_id: int
class StateX(BaseModel):
    day: datetime=dt.datetime.now(dt.timezone.utc) 
    macros: Optional[MacrosBase]
    traces: Optional[TracesBase]
    vitamins: Optional[VitaminsBase]
    minerals: Optional[MineralsBase]
    meds: Optional[MedsBase]
class GeneralFoodBase(BaseModel):
    food_name: str
    servings: float
    total_cals: int
    cals_per_serv: Optional[float]
    brand_name: Optional[str]
    ingredients: Optional[str]
    serving_size_unit: Optional[str]
    created_at: datetime=dt.datetime.now(dt.timezone.utc) 
    state_id: Optional[int]
class PostFood(BaseModel):
    general: GeneralFoodBase
    macros: Optional[MacrosBase]
    vitamins: Optional[VitaminsBase]
    minerals: Optional[MineralsBase]
    traces: Optional[TracesBase]
