#!/usr/bin/env python
from fastapi import FastAPI, Response, status, HTTPException, APIRouter, Depends
from typing import List
from .. import schemas, utils, database,oauth,rules_book
from . import res,user
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

#Get
