#!/usr/bin/env python
from fastapi import FastAPI, Response, status, HTTPException, APIRouter, Depends
from typing import List
from .. import schemas, utils, database,oauth,rules_book
from . import res,user,state
from fastapi.responses import ORJSONResponse
import orjson
from collections import Counter
conn,cursor=database.run()
router = APIRouter(
        prefix='/activity',
        tags=['activities'])
#Post
# user_activities_general
@router.post("/", status_code=status.HTTP_201_CREATED)

def post_activity(activity_info: schemas.PostActivity, get_current_user: int = Depends(oauth.get_current_user)):
    result=dict()
    if not activity_info.state_id:
        obj=dict()
        obj['day']=activity_info.created_at
        state_id=state.user_state_general(schemas.GeneralState(**obj),get_current_user)
        activity_info.state_id=orjson.loads(state_id.body)[0]['state_id']
    activity_info=activity_info.dict(exclude_none=True)
    activity_info['user_id']=get_current_user.id
    query_str,in_tup=utils.query_strs('insert','user_activities_general',obj=activity_info)
    cursor.execute(query_str,in_tup)
    result=cursor.fetchone()
    conn.commit()
   #user_activities_general 
    return result
#Update
@router.put("/", status_code=status.HTTP_201_CREATED)

def put_activity(activity_info: schemas.UpdateActivity, get_current_user: int = Depends(oauth.get_current_user)):
    activity_info=activity_info.dict(exclude_none=True)
    activity_id=activity_info.pop('activity_id')
    query_str,in_tup=utils.query_strs('update','user_activities_general','activity_id',activity_id,obj=activity_info)
    cursor.execute(query_str,in_tup)
    result=cursor.fetchone()
    conn.commit()
    return result
#Delete
@router.delete("/", status_code=status.HTTP_201_CREATED)

def delete_activity(activity_id: int, get_current_user: int = Depends(oauth.get_current_user)):
    cursor.execute('''SELECT * FROM user_activities_general WHERE user_id=%s AND activity_id=%s''',(get_current_user.id,activity_id))
    result=cursor.fetchone()
    if result:
       cursor.execute('''DELETE FROM user_activities_general WHERE activity_id=%s RETURNING *''',(activity_id,)) 
       result=cursor.fetchone()
       conn.commit()

    else:
       raise HTTPException(status_code=403, detail=f"Forbbiden") 
    return activity_id


#Get
