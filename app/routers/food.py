#!/usr/bin/env python
from fastapi import FastAPI, Response, status, HTTPException, APIRouter, Depends
from typing import Optional
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
    conn.commit()
    return food_info
def post_user_food_an_x(food_info: dict,tablename:str,food_entry_id: int):
    food_info['food_entry_id']=food_entry_id
    query_str,in_tup=utils.query_strs('insert',f'user_food_{tablename}',obj=food_info)
    cursor.execute(query_str,in_tup)
    food_info=cursor.fetchone()
    conn.commit()
    return food_info
def apply_servings_taken(food_info: dict,servings: int,op:Optional[str]='post'):
    if 'general' in food_info.keys():
        food_info['general']['total_cals']=food_info['general']['total_cals']*servings
    lss=['macros','vitamins','traces','minerals']
    for x in lss:
        if x in food_info.keys():
            food_info[x]={k: servings*v for k,v in food_info[x].items() if v}
    if op=='post':
        res= schemas.FoodBase(**food_info)
    else:
        res= schemas.FoodUpdate(**food_info)
    return res

@router.put("/",status_code=status.HTTP_201_CREATED)
def update_user_food(food_info: schemas.FoodUpdate,get_current_user: int = Depends(oauth.get_current_user)):
    f_result=dict()
    un_flag=False
    # lookup food by food_entry_id
    cursor.execute('''SELECT * FROM user_food_general WHERE food_entry_id=%s''', (food_info.food_entry_id,))
    result=cursor.fetchone()
    conn.commit()
    #if food exists, continue, other wise raise error 403
    if result:
    # exculde unset from food_info,update the ones set on the query result
    # {old_data}.update(new_data)
    # update to each table with the final query
        if result['user_id']!=int(get_current_user.id):
            raise HTTPException(status_code=403, detail=f"Forbbiden")
        cursor.execute('''SELECT * FROM user_food_macros WHERE food_entry_id=%s''', (food_info.food_entry_id,))
        result1=cursor.fetchone()
        cursor.execute('''SELECT * FROM user_food_minerals WHERE food_entry_id=%s''', (food_info.food_entry_id,))
        result2=cursor.fetchone()
        cursor.execute('''SELECT * FROM user_food_vitamins WHERE food_entry_id=%s''', (food_info.food_entry_id,))
        result3=cursor.fetchone()
        
        cursor.execute('''SELECT * FROM user_food_traces WHERE food_entry_id=%s''', (food_info.food_entry_id,))
        result4=cursor.fetchone()
        b_result=dict()
        b_result['general']=result
        b_result['macros']=result1
        b_result['minerals']=result2
        b_result['vitamins']=result3
        b_result['traces']=result4
        # unapply servings taken    
        if b_result['general']['servings_taken']>1:
            b_result=unapply_taken(b_result)
        new_info=food_info.dict(exclude_unset=True)
        b_result.update(new_info)
        # convert back to FoodUpdate
        if b_result['general']['servings_taken']>1:
            food_info=apply_servings_taken(b_result,op='update')
        else:
            food_info=schemas.FoodUpdate(**b_result)
        #put to every table 
        lss=['general','macros','minerals','vitamins','traces']
        for x in lss:
            
        
        return food_info

    else:
        raise HTTPException(status_code=403, detail=f"no such food_entry_id")

def update_user_food_an_x(food_info: dict,tablename:str,food_entry_id: int):
    #NEEDS EDITING
    #CHANGE TO UPDATE
    food_info['food_entry_id']=food_entry_id
    query_str,in_tup=utils.query_strs('insert',f'user_food_{tablename}',obj=food_info)
    cursor.execute(query_str,in_tup)
    food_info=cursor.fetchone()
    conn.commit()
    return food_info
def unapply_taken(food_info: dict):
    servings_taken=food_info['servings_taken']
    if 'general' in food_info.keys():
        food_info['general']['total_cals']=food_info['general']['total_cals']/servings
    
    lss=['macros','vitamins','traces','minerals']
    for x in lss:
        if x in food_info.keys():
            food_info[x]={k: v/servings_taken for k,v in food_info[x].items() if v}

    return food_info

#Update
#Delete
#Get
