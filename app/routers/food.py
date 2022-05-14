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
    food_info={k:v for k,v in food_info.items() if v}
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
    b_result=dict()
    
    # lookup food by food_entry_id
    cursor.execute('''SELECT * FROM user_food_general WHERE food_entry_id=%s''', (food_info.food_entry_id,))
    b_result['general']=dict(cursor.fetchone())
    #if food exists, continue, other wise raise error 403
    if 'general' in b_result.keys():
    # exculde unset from food_info,update the ones set on the query result
    # {old_data}.update(new_data)
    # update to each table with the final query
        if b_result['general']['user_id']!=int(get_current_user.id):
            raise HTTPException(status_code=403, detail=f"Forbbiden")
        cursor.execute('''SELECT * FROM user_food_macros WHERE food_entry_id=%s''', (food_info.food_entry_id,))
        b_result['macros']=cursor.fetchone()
        cursor.execute('''SELECT * FROM user_food_minerals WHERE food_entry_id=%s''', (food_info.food_entry_id,))
        b_result['minerals']=cursor.fetchone()
        cursor.execute('''SELECT * FROM user_food_vitamins WHERE food_entry_id=%s''', (food_info.food_entry_id,))
        b_result['vitamins']=cursor.fetchone()
        
        cursor.execute('''SELECT * FROM user_food_traces WHERE food_entry_id=%s''', (food_info.food_entry_id,))
        b_result['traces']=cursor.fetchone()
        b_result={k:dict(v) for k,v in b_result.items() if v }
        # unapply servings taken    
        if b_result['general']['servings_taken']>1:
            b_result=unapply_taken(b_result)
        new_info=food_info.dict(exclude_unset=True)
        print("b_result Before\n",b_result)
        print("inputed updates\n",new_info)
        #b_result.update(new_info)
        for k,v in new_info.items():
            if k!='food_entry_id':
                if k in b_result.keys():
                    b_result[k].update(v)
                else:
                    #raising an error if new tables are being edited
                    raise HTTPException(status_code=403, detail=f"Delete and make a new entry")

        b_result={k:dict(v) for k,v in b_result.items() if v}
        #adding food_enty_id to b_result
        b_result['food_entry_id']=new_info['food_entry_id']
        print("b_result after\n",b_result)
        # convert back to FoodUpdate
        if b_result['general']['servings_taken']>1:
            food_info=apply_servings_taken(b_result,b_result['general']['servings_taken'],op='update')
        else:
            food_info=schemas.FoodUpdate(**b_result)
        #put to every table 
        food_info=food_info.dict(exclude_none=True)
        food_id=food_info.pop('food_entry_id')
        general_info=food_info.pop('general')
        query_str,in_tup=utils.query_strs('update','user_food_general','food_entry_id',food_id,obj=general_info)
        print(query_str)
        print(in_tup)
        cursor.execute(query_str,in_tup)
        f_result['general']=cursor.fetchone()
        conn.commit()
        lss=food_info.keys()
        for x in lss:
            f_result[x]=update_user_food_an_x(food_info[x],x,food_id)

        return f_result

    else:
        raise HTTPException(status_code=403, detail=f"no such food_entry_id")

def update_user_food_an_x(food_info: dict,tablename:str,food_entry_id: int):
    #NEEDS EDITING
    #CHANGE TO UPDATE
    query_str,in_tup=utils.query_strs('update',f'user_food_{tablename}','food_entry_id',food_entry_id,obj=food_info)
    print(query_str)
    print(in_tup)
    cursor.execute(query_str,in_tup)
    food_info=cursor.fetchone()
    conn.commit()
    return food_info
def unapply_taken(food_info: dict):
    servings_taken=food_info['general']['servings_taken']
    food_info={k:v for k,v in food_info.items() if v}
    lss=list(food_info.keys())
    if 'general' in food_info.keys():
        food_info['general']['total_cals']=food_info['general']['total_cals']/servings_taken
        lss.remove('general')
    
    for x in lss:
        if x in food_info.keys():
            food_id=food_info[x].pop('food_entry_id')
            food_info[x]={k: v/servings_taken for k,v in food_info[x].items() if v}
            food_info[x]['food_entry_id']=food_id

    return food_info


#Delete
@router.delete("/",status_code=status.HTTP_201_CREATED)
def delete_food_entry(food_entry_id: int,get_current_user: int = Depends(oauth.get_current_user)):
    cursor.execute('''SELECT * FROM user_food_general WHERE food_entry_id=%s''', (food_entry_id,))
    result=cursor.fetchone()
    if result:
        if result['user_id']==int(get_current_user.id):
            # delete
            cursor.execute('''DELETE FROM user_food_general WHERE food_entry_id=%s RETURNING *''',(food_entry_id,))
            result=cursor.fetchone()
            conn.commit()
        else: 
            raise HTTPException(status_code=403, detail=f"Can't delete other users food entry")
    else:
        raise HTTPException(status_code=403, detail=f"No such food entry")
    return result


#Get
@router.get("/",status_code=status.HTTP_201_CREATED)
def get_a_food_entry(food_entry_id: int,get_current_user: int = Depends(oauth.get_current_user)):
    return food_entry_id
