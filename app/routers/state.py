#!/usr/bin/env python
from fastapi import FastAPI, Response, status, HTTPException, APIRouter, Depends
from typing import List,Optional
from .. import schemas, utils, database,oauth
from . import res,user
from fastapi.responses import ORJSONResponse
import orjson
from collections import Counter,deque
from datetime import datetime as dt
conn,cursor=database.run()
router = APIRouter(
        prefix='/state',
        tags=['User State'])
@router.put("/",status_code=status.HTTP_201_CREATED)
@router.post("/",status_code=status.HTTP_201_CREATED)
def user_state_general(general_state_info: schemas.GeneralState,get_current_user: int = Depends(oauth.get_current_user)
        ,op_input: Optional[str]='sum'):
    # Check if state of today exists
    today=general_state_info.day.date()
    cursor.execute('''SELECT * FROM user_state_general WHERE user_id=%s ORDER BY state_id DESC LIMIT 1''',(get_current_user.id,))
    result=cursor.fetchone()
    # Choose to post or put/patch
    if result:
        if result['day']<today:
            result=post_user_state_general(general_state_info=general_state_info,get_current_user=get_current_user)
        else:
            general_state_info=general_state_info.dict(exclude_none=True)
            general_state_info['state_id']=result['state_id']
            if op_input=='sub':
                general_state_info['total_cals']=result['total_cals']-general_state_info['total_cals']
            else:
                general_state_info['total_cals']=result['total_cals']+general_state_info['total_cals']
            result=update_user_state_general(general_state_info=general_state_info,get_current_user=get_current_user)
    else:
        result=post_user_state_general(general_state_info=general_state_info,get_current_user=get_current_user)
    return ORJSONResponse(result)
def post_user_state_general(general_state_info: schemas.GeneralState,get_current_user: int = Depends(oauth.get_current_user)):
    query_str,in_tup='',tuple()
    general_state_info=general_state_info.dict(exclude_none=True) 
    general_state_info['user_id']=get_current_user.id
    query_str,in_tup=utils.query_strs('insert','user_state_general',obj=general_state_info)
    cursor.execute(query_str,in_tup)
    result=cursor.fetchall()
    conn.commit()
    return result

def update_user_state_general(general_state_info: dict,get_current_user: int = Depends(oauth.get_current_user)):
    query_str,in_tup='',tuple()
    state_id=general_state_info.pop('state_id')
    general_state_info.pop('day')
    query_str,in_tup=utils.query_strs('update','user_state_general','state_id',state_id,obj=general_state_info)
    cursor.execute(query_str,in_tup)
    result=cursor.fetchall()
    conn.commit()
    return result
@router.put("/x",status_code=status.HTTP_201_CREATED)
@router.post("/x",status_code=status.HTTP_201_CREATED)
def user_state_x(x_state_info: schemas.StateX, get_current_user: int = Depends(oauth.get_current_user),op_input: Optional[str]='sum'):
    # Check if state of today exists
    today=x_state_info.day
    new_ugs={"day": today}
    result=user_state_general(general_state_info=schemas.GeneralState(**new_ugs),get_current_user=get_current_user)
    result=orjson.loads(result.body)[0]
    f_result=dict()
    f_result['general']=result.copy()
    if x_state_info.macros:
        f_result['macros']=user_state_an_x(result['state_id'],x_state_info,'macros',op=op_input)
    
    if x_state_info.minerals:
        f_result['minerals']=user_state_an_x(result['state_id'],x_state_info,'minerals',op=op_input)
    
    if x_state_info.vitamins:
        f_result['vitamins']=user_state_an_x(result['state_id'],x_state_info,'vitamins',op=op_input)
    
    if x_state_info.minerals:
        f_result['traces']=user_state_an_x(result['state_id'],x_state_info,'traces',op=op_input)


    return f_result

def user_state_an_x(state_id: int,x_state_info: schemas.StateX,tablename: str,op: str):
    
    cursor.execute(f'''SELECT * FROM user_state_{tablename} WHERE state_id=%s ORDER BY state_id DESC LIMIT 1''',(state_id,))
    result=cursor.fetchone()
    query_str_in_tup='',tuple()
    x_info=eval(f'x_state_info.{tablename}.dict(exclude_none=True)')
    if result:
        if result['state_id']!=state_id:
            x_info['state_id']=state_id
            query_str,in_tup=utils.query_strs('insert',f'user_state_{tablename}',obj=x_info)
            cursor.execute(query_str,in_tup)
            result = cursor.fetchall()
            conn.commit()
        else:
            # Add old and new
            # then update
            result.pop('state_id')
            ## exclude Null values from result
            result={k:v for k,v in result.items() if v}
            old_macros=Counter(result)
            new_macros=Counter(x_info)
            if op=='sum':
                sum_macros=dict(old_macros+new_macros)
            else:
                #consume = deque(maxlen=0).extend
                #consume(old_macros.pop(key, None) for key in new_macros) 
                #sum_macros=old_macros
                #sum_macros=dict(set(old_macros.items()) - set(new_macros.items()))
                sum_macros=subtract_dicts(old_macros,new_macros)
            if bool(sum_macros):
                query_str,in_tup=utils.query_strs('update',f'user_state_{tablename}','state_id',state_id,obj=sum_macros)
                cursor.execute(query_str,in_tup)
                result=cursor.fetchone()
                conn.commit()

    else:
        print("No Post in Macros")
        #Post given macros
        # Posting macros_state_info to user_state_macros
        x_info['state_id']=state_id
        query_str,in_tup=utils.query_strs('insert',f'user_state_{tablename}',obj=x_info)
        cursor.execute(query_str,in_tup)
        result = cursor.fetchone()
        conn.commit()
    result={k:v for k,v in result.items() if v}
    return result

def subtract_dicts(old: dict,new: dict):
    # figure out a way to subtract between two dicts, of different keys
    result=dict()
    for k,v in new.items():
        if k in old.keys():
            result[k]=old[k]-v

    return result


@router.post("/reset",status_code=status.HTTP_201_CREATED)
def state_reset(get_current_user: int = Depends(oauth.get_current_user)):
    state_id=user_state_general(schemas.GeneralState(**dict()),get_current_user)
    state_id=orjson.loads(state_id.body)[0]['state_id']
    cursor.execute('''DELETE FROM user_state_general WHERE state_id=%s''',(state_id,))
    return dict()

@router.get("/get", status_code=status.HTTP_201_CREATED)
def state_get(get_current_user: int = Depends(oauth.get_current_user)):
    result=dict()
    state_id=user_state_general(schemas.GeneralState(**dict()),get_current_user)
    state_id=orjson.loads(state_id.body)[0]['state_id']
    cursor.execute('''SELECT * FROM user_state_general WHERE state_id=%s''',(state_id,))
    result["general"]=cursor.fetchone()
    cursor.execute('''SELECT * FROM user_state_macros WHERE state_id=%s''',(state_id,))
    result["macros"]=cursor.fetchone()
    cursor.execute('''SELECT * FROM user_state_minerals WHERE state_id=%s''',(state_id,))
    result["minerals"]=cursor.fetchone()
    cursor.execute('''SELECT * FROM user_state_vitamins WHERE state_id=%s''',(state_id,))
    result["vitamins"]=cursor.fetchone()
    cursor.execute('''SELECT * FROM user_state_traces WHERE state_id=%s''',(state_id,))
    result["traces"]=cursor.fetchone()
    return result

