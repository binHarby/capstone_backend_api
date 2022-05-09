#!/usr/bin/env python
from fastapi import FastAPI, Response, status, HTTPException, APIRouter, Depends
from typing import List
from .. import schemas, utils, database,oauth
from . import res,user
from fastapi.responses import ORJSONResponse
import orjson
from collections import Counter
from datetime import datetime as dt
conn,cursor=database.run()
router = APIRouter(
        prefix='/state',
        tags=['User State'])
@router.post("/",status_code=status.HTTP_201_CREATED)
def user_state_general(general_state_info: schemas.GeneralState,get_current_user: int = Depends(oauth.get_current_user)):
    # Check if state of today exists
    today=general_state_info.day.date()
    cursor.execute('''SELECT * FROM user_state_general WHERE user_id=%s ORDER BY state_id DESC LIMIT 1''',(get_current_user.id,))
    result=cursor.fetchone()
    # Choose to post or put/patch
    if result['day']<today:
        post_user_state_general(general_state_info=general_state_info,get_current_user=get_current_user)
    else:
        general_state_info=general_state_info.dict(exclude_none=True)
        general_state_info['state_id']=result['state_id']
        update_user_state_general(general_state_info=general_state_info,get_current_user=get_current_user)
    return general_state_info
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
