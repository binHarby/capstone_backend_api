#!/usr/bin/env python
from fastapi import FastAPI, Response, status, HTTPException, APIRouter, Depends
from typing import List,Optional
from .. import schemas, utils, database,oauth,rules_book
from . import res,user,state
from fastapi.responses import ORJSONResponse
import orjson
from collections import Counter
conn,cursor=database.run()
router = APIRouter(
        prefix='/med',
        tags=['Medications'])
#Post
@router.post("/", status_code=status.HTTP_201_CREATED)
def post_med(med_info: schemas.PostMed,get_current_user: int = Depends(oauth.get_current_user)):
    result=dict()
    if not med_info.res_id:
        # query res by name FROM res_rules, get id
        cursor.execute('''SELECT * FROM res_rules WHERE name=%s''',(med_info.res_name,))
        result=cursor.fetchone()
        if result:
            med_info.res_id=result['id']
        else:
            raise HTTPException(status_code=403, detail=f"No such restriction")
    
    cursor.execute('''SELECT * FROM user_meds_general WHERE med_name=%s AND user_id=%s''',(med_info.med_name,get_current_user.id))
    result=cursor.fetchone()
    if result:
        raise HTTPException(status_code=403, detail=f"medication already posted")

    # now, post to user_meds_general
    med_info=med_info.dict(exclude_none=True)
    med_info['user_id']=get_current_user.id
    query_str,in_tup=utils.query_strs('insert','user_meds_general',obj=med_info)
    print("",query_str,"\n",in_tup)
    cursor.execute(query_str,in_tup)
    result=cursor.fetchone()
    conn.commit()
    return result
#Update

@router.put("/", status_code=status.HTTP_201_CREATED)
def update_med(med_info: schemas.UpdateMed,get_current_user: int = Depends(oauth.get_current_user)):
    cursor.execute('''SELECT * FROM user_meds_general WHERE med_id=%s AND user_id=%s''',(med_info.med_id,get_current_user.id))
    med_info=med_info.dict(exclude_none=True)
    med_id=med_info.pop('med_id')
    med_info['user_id']=get_current_user.id
    query_str,in_tup=utils.query_strs('update','user_meds_general','med_id',med_id,obj=med_info)
    print("",query_str,"\n",in_tup)
    cursor.execute(query_str,in_tup)
    result=cursor.fetchone()
    conn.commit()
    return result
#Delete
@router.delete("/", status_code=status.HTTP_201_CREATED)
def delete_med(med_id: int,get_current_user: int = Depends(oauth.get_current_user)):
    cursor.execute('''SELECT * FROM user_meds_general WHERE med_id=%s AND user_id=%s''',(med_id,get_current_user.id))
    result=cursor.fetchone()
    if result:
        cursor.execute('''DELETE FROM user_meds_general WHERE med_id=%s RETURNING *''',(med_id,))
        result=cursor.fetchone()
        conn.commit()
    else:
        raise HTTPException(status_code=403, detail=f"Forbbiden")
    return result


#Get
@router.get("/", status_code=status.HTTP_201_CREATED)
def get_med(med_id: int,get_current_user: int = Depends(oauth.get_current_user)):
    cursor.execute('''SELECT * FROM user_meds_general WHERE med_id=%s AND user_id=%s''',(med_id,get_current_user.id))
    result=cursor.fetchone()
    if not result:
        raise HTTPException(status_code=403, detail=f"Forbbiden")
    return result
@router.get("/record", status_code=status.HTTP_201_CREATED)
def get_all_med(get_current_user: int = Depends(oauth.get_current_user)):
    cursor.execute('''SELECT * FROM user_meds_general WHERE user_id=%s''',(get_current_user.id,))
    result=cursor.fetchall()
    if not result:
        raise HTTPException(status_code=403, detail=f"Forbbiden")
    return result
#user_meds_delta

#Post
@router.post("/daily", status_code=status.HTTP_201_CREATED)
def post_daily_med(med_info: schemas.PostDailyMed,get_current_user: int = Depends(oauth.get_current_user)):
    if not med_info.state_id:
        obj=dict()
        result=state.user_state_general(schemas.GeneralState(**obj),get_current_user)
        med_info.state_id=orjson.loads(result.body)[0]['state_id']
    cursor.execute('''SELECT * FROM user_meds_delta WHERE state_id=%s AND med_id=%s''',(med_info.state_id,med_info.med_id))
    result=cursor.fetchone()
    if result:
        raise HTTPException(status_code=403, detail=f"Med Delta already Posted, try update")

    med_info=med_info.dict(exclude_none=True)
    query_str,in_tup=utils.query_strs('insert','user_meds_delta',obj=med_info)
    print(query_str)
    print(in_tup)
    cursor.execute(query_str,in_tup)
    result=cursor.fetchone()
    conn.commit()
    return result

@router.put("/daily", status_code=status.HTTP_201_CREATED)
def update_daily_med(med_info: schemas.UpdateDailyMed,get_current_user: int = Depends(oauth.get_current_user)):
    if not med_info.state_id:
        obj=dict()
        result=state.user_state_general(schemas.GeneralState(**obj),get_current_user)
        med_info.state_id=orjson.loads(result.body)[0]['state_id']
    
    cursor.execute('''SELECT * FROM user_meds_delta WHERE state_id=%s AND med_id=%s''',(med_info.state_id,med_info.med_id))
    result=cursor.fetchone()
    if not result:
        raise HTTPException(status_code=403, detail=f"Med Delta Not Posted")
    med_info=med_info.dict(exclude_none=True)
    state_id=med_info.pop('state_id')
    med_id=med_info.pop('med_id')
    query_str='''UPDATE user_meds_delta SET '''
    tmpls=list()
    for key in med_info.keys():
        tmpls.append(f'{key}=%s ')
    query_str+=','.join(tmpls)+'WHERE state_id=%s AND med_id=%s RETURNING *'
    in_tup=list(med_info.values())
    in_tup.append(state_id)
    in_tup.append(med_id)
    in_tup=tuple(in_tup)
    print(query_str)
    print(in_tup)
    cursor.execute(query_str,in_tup)
    result=cursor.fetchone()
    conn.commit()
    return result
#delete user med_delta
@router.delete("/daily", status_code=status.HTTP_201_CREATED)
def delete_daily_med(med_id: int,state_id: Optional[int],get_current_user: int = Depends(oauth.get_current_user)):
    if not state_id:
        obj=dict()
        result=state.user_state_general(schemas.GeneralState(**obj),get_current_user)
        state_id=orjson.loads(result.body)[0]['state_id']
    cursor.execute('''SELECT * FROM user_meds_delta WHERE state_id=%s AND med_id=%s''',(state_id,med_id))
    result=cursor.fetchone()
    if not result:
        raise HTTPException(status_code=403, detail=f"Med Delta Not Posted")
    cursor.execute('''DELETE FROM user_meds_delta WHERE state_id=%s AND med_id=%s RETURNING *''',(state_id,med_id))
    result=cursor.fetchone()
    return result


@router.get("/daily", status_code=status.HTTP_201_CREATED)
def get_daily_med(med_id: int,state_id: Optional[int],get_current_user: int = Depends(oauth.get_current_user)):
    if not state_id:
        obj=dict()
        result=state.user_state_general(schemas.GeneralState(**obj),get_current_user)
        state_id=orjson.loads(result.body)[0]['state_id']
    cursor.execute('''SELECT * FROM user_meds_delta WHERE state_id=%s AND med_id=%s''',(state_id,med_id))
    result=cursor.fetchone()
    if not result:
        raise HTTPException(status_code=403, detail=f"Med Delta Not Posted")
