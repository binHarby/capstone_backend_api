#!/usr/bin/env python
from fastapi import FastAPI, Response, status, HTTPException, APIRouter, Depends
from typing import List
from .. import schemas, utils, database,oauth,rules_book
from . import state
from fastapi.responses import ORJSONResponse
import orjson
from collections import Counter
conn,cursor=database.run()
router = APIRouter(
        prefix='/food',
        tags=['Foods'])
#Post, General and others
@router.post("/",status_code=status.HTTP_201_CREATED)
def post_user_food(food_info: schemas.FoodBase,get_current_user: int = Depends(oauth.get_current_user)):
    f_result=dict()
    # if no state, get state
    user_id=get_current_user.id
    if not food_info.general.state_id:
        state_id=state.user_state_general(schemas.GeneralState(),get_current_user)
        state_id=orjson.loads(state_id.body)[0]['state_id']
        food_info.general.state_id=state_id
        print("got state_id from query/update")
    if food_info.general.servings_taken:
        food_info=apply_servings_taken(food_info.dict(exclude_none=True),food_info.general.servings_taken)
    general_info=food_info.general.dict(exclude_none=True)
    general_info['user_id']=user_id
    general_info=post_food_general(general_info)
    food_entry_id=general_info['food_entry_id']
    f_result['general']=general_info
    if food_info.macros:
        x_in=food_info.macros.dict(exclude_none=True)
        f_result['macros']=post_user_food_an_x(x_in,'macros',food_entry_id)
    if food_info.minerals:
        x_in=food_info.minerals.dict(exclude_none=True)
        f_result['minerals']=post_user_food_an_x(x_in,'minerals',food_entry_id)
    if food_info.vitamins:
        x_in=food_info.vitamins.dict(exclude_none=True)
        f_result['vitamins']=post_user_food_an_x(x_in,'vitamins',food_entry_id)
    if food_info.traces:
        x_in=food_info.traces.dict(exclude_none=True)
        f_result['traces']=post_user_food_an_x(x_in,'traces',food_entry_id)
    return f_result
def post_food_general(food_info: dict):
    query_str,in_tup=utils.query_strs('insert','user_food_general',obj=food_info)
    cursor.execute(query_str,in_tup)
    food_info=cursor.fetchone()
    return food_info
def post_user_food_an_x(food_info: dict,tablename:str,food_entry_id: int):
    food_info['food_entry_id']=food_entry_id
    query_str,in_tup=utils.query_strs('insert',f'user_food_{tablename}',obj=food_info)
    cursor.execute(query_str,in_tup)
    food_info=cursor.fetchone()
    
    return food_info
def apply_servings_taken(food_info: dict,servings: int):
    if 'general' in food_info.keys():
        food_info['general']['total_cals']=food_info['general']['total_cals']*servings
    lss=['macros','vitamins','traces','minerals']
    for x in lss:
        if x in food_info.keys():
            food_info[x]={k: servings*v for k,v in food_info[x].items() if v}

    return schemas.FoodBase(**food_info)

@router.put("/",status_code=status.HTTP_201_CREATED)
def update_user_food(food_info: schemas.FoodBase,get_current_user: int = Depends(oauth.get_current_user)):
    f_result=dict()
    # lookup food by food_entry_id
    #if food exists, continue, other wise raise error 403
    # exculde unset from food_info,update the ones set on the query result
    # update to each table with the final query
#Update
#Delete
#Get
