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
        prefix='/goal',
        tags=['User Goals'])

@router.post("/",status_code=status.HTTP_201_CREATED) 
def post_general_goals(general_info: schemas.PostGeneralGoal, get_current_user: int = Depends(oauth.get_current_user)):
    cursor.execute('''SELECT * FROM users WHERE id=%s''',(get_current_user.id,))
    query=cursor.fetchone()
    query_str=''
    in_tup=tuple()
    if not query:
        raise HTTPException(status_code=403, detail=f"User Not In Database")
    else:
        cursor.execute('''SELECT * FROM user_goal_general WHERE user_id=%s''',(get_current_user.id,))
        qu2=cursor.fetchone()
        if qu2:
            raise HTTPException(status_code=403, detail=f"General Goals for this user have been posted!")

        general_info=general_info.dict(exclude_none=True)
        general_info['user_id']=get_current_user.id
        # calculate tdee, bmi and cal_goal
        tdee=utils.get_tdee(query['gender'],general_info['weight'],query['height'],query['age'],general_info['activity_lvl'])
        bmi=utils.get_bmi(general_info['weight'],query['height'])
        cal_goal=tdee-general_info['cal_diff']
        if 'cal_goal' in general_info.keys():
            cal_goal=general_info['cal_goal']
        # add them to insert query
        general_info['tdee']=tdee
        general_info['bmi']=bmi
        general_info['cal_goal']=cal_goal
        query_str,in_tup=utils.query_strs('insert','user_goal_general',obj=general_info)
        print(query_str)
        print(in_tup)
        cursor.execute(query_str,in_tup)
        general_info=cursor.fetchall()
        conn.commit()
        return ORJSONResponse(general_info[0])

@router.put("/",status_code=status.HTTP_201_CREATED) 
def update_general_goals(general_info: schemas.UpdateGeneralGoal, get_current_user: int = Depends(oauth.get_current_user)):
    cursor.execute('''SELECT * FROM users WHERE id=%s''',(get_current_user.id,))
    query=cursor.fetchone()
    query_str=''
    in_tup=tuple()
    if not query:
        raise HTTPException(status_code=403, detail=f"User Not In Database")
    else:
        cursor.execute('''SELECT * FROM user_goal_general WHERE user_id=%s''',(get_current_user.id,))
        qu2=cursor.fetchone()
        if not qu2:
            raise HTTPException(status_code=403, detail=f"No General Goals entry for this user")

        general_info=general_info.dict(exclude_none=True)
        if 'activity_lvl' not in general_info.keys():
            general_info['activity_lvl']=qu2['activity_lvl']
        if 'cal_diff' not in general_info.keys():
            general_info['cal_diff']=qu2['cal_diff']
        if 'control_lvl' not in general_info.keys():
            general_info['control_lvl']=qu2['control_lvl']
        # calculate tdee, bmi and cal_goal
        tdee=utils.get_tdee(query['gender'],general_info['weight'],query['height'],query['age'],general_info['activity_lvl'])
        bmi=utils.get_bmi(general_info['weight'],query['height'])
        cal_goal=tdee-general_info['cal_diff']
        if 'cal_goal' in general_info.keys():
            cal_goal=general_info['cal_goal']
        # add them to insert query
        general_info['tdee']=tdee
        general_info['bmi']=bmi
        general_info['cal_goal']=cal_goal
        query_str,in_tup=utils.query_strs('update','user_goal_general','user_id',get_current_user.id,obj=general_info)
        print(query_str)
        print(in_tup)
        cursor.execute(query_str,in_tup)
        general_info=cursor.fetchall()
        conn.commit()
        return ORJSONResponse(general_info[0])

@router.get("/",status_code=status.HTTP_201_CREATED) 
def get_general_goals(get_current_user: int = Depends(oauth.get_current_user)):
    cursor.execute('''SELECT * FROM user_goal_general WHERE user_id=%s''',(get_current_user.id,))
    result=cursor.fetchone()
    if result:
        return dict(result)
    else:
        raise HTTPException(status_code=403, detail=f"No General Goals entry for this user")

    


@router.post("/x",status_code=status.HTTP_201_CREATED) 
def post_x_goals(get_current_user: int = Depends(oauth.get_current_user)):
    # Post to respective tables
    final_results=set_goal(get_current_user=get_current_user)
    query_str,in_tup='',tuple()
    if 'macros' in final_results.keys():
        final_results['macros']['user_id']=get_current_user.id
        query_str,in_tup=utils.query_strs('insert','user_goal_macros',obj=final_results['macros'])
    else:
        objj={"user_id":get_current_user.id}
        query_str,in_tup=utils.query_strs('insert','user_goal_macros',obj=objj)
    try:
        cursor.execute(query_str,in_tup)
        final_results['macros']=cursor.fetchone()
        conn.commit()
    except Exception:
        conn.rollback()
        raise HTTPException(status_code=403, detail=f"X Goals entries have been posted for this user")

        
    if 'minerals' in final_results.keys():
        final_results['minerals']['user_id']=get_current_user.id
        query_str,in_tup=utils.query_strs('insert','user_goal_minerals',obj=final_results['minerals'])
    else:
        objj={"user_id":get_current_user.id}
        query_str,in_tup=utils.query_strs('insert','user_goal_minerals',obj=objj)
    try:
        cursor.execute(query_str,in_tup)
        final_results['minerals']=cursor.fetchone()
        conn.commit()
    except Exception:
        conn.rollback()
        raise HTTPException(status_code=403, detail=f"X Goals entries have been posted for this user")
    if 'vitamins' in final_results.keys():
        final_results['vitamins']['user_id']=get_current_user.id
        query_str,in_tup=utils.query_strs('insert','user_goal_vitamins',obj=final_results['vitamins'])
    else:
        objj={"user_id":get_current_user.id}
        query_str,in_tup=utils.query_strs('insert','user_goal_vitamins',obj=objj)
    try:
        cursor.execute(query_str,in_tup)
        final_results['vitamins']=cursor.fetchone()
        conn.commit()
    except Exception:
        conn.rollback()
        raise HTTPException(status_code=403, detail=f"X Goals entries have been posted for this user")

    if 'traces' in final_results.keys():
        final_results['traces']['user_id']=get_current_user.id
        query_str,in_tup=utils.query_strs('insert','user_goal_traces',obj=final_results['traces'])
    else:
        objj={"user_id":get_current_user.id}
        query_str,in_tup=utils.query_strs('insert','user_goal_traces',obj=objj)
    try:
        cursor.execute(query_str,in_tup)
        final_results['traces']=cursor.fetchone()
        conn.commit()
    except Exception:
        conn.rollback()
        raise HTTPException(status_code=403, detail=f"X Goals entries have been posted for this user")
    final_results = {k:v for k,v in final_results.items() if v}
    return final_results

def set_goal(get_current_user: int = Depends(oauth.get_current_user)):
    obj={"alll": True}
    rest_info=schemas.GetUserRestReq(**obj)
    user_res=res.get_user_rest(rest_info,get_current_user=get_current_user)
    user_res=orjson.loads(user_res.body)
    user_res_ruleid=dict()
    for i in user_res:
        i.pop('user_res_id')
        i.pop('user_id')
    # name of res and details
    user_res=get_res_details(user_res)
    # user general details
    user_info=user.get_user(get_current_user=get_current_user)
    user_general=get_general_goals(get_current_user=get_current_user)
    user_info=orjson.loads(user_info.body)
    user_general=user_general
    # pass to method, get results for each restriction
    results=list()
    for i in user_res:
        res_name=i['details']['name'].replace(' ','_')
        rule_no=str(i['rule'])
        method_name=res_name+'_'+rule_no
        print(method_name)
        result=eval(f'rules_book.{method_name}')(user_info,user_general,i)
        results.append(result)
    # sum results, get the final goals
    vitamins=Counter(dict())
    traces=Counter(dict())
    minerals=Counter(dict())
    macros=Counter(dict())
    for i in results:
        if i['macros']:
            macros+=Counter(i['macros'])
        if i['traces']:
            traces+=Counter(i['traces'])
        if i['vitamins']:
            vitamins+=Counter(i['vitamins'])
        if i['minerals']:
            minerals+=Counter(i['minerals'])
    macros=dict(macros)
    minerals=dict(minerals)
    traces=dict(traces)
    vitamins=dict(vitamins)
    final_result=dict()
    if macros:
        final_result['macros']=macros
    if vitamins:
        final_result['vitamins']=vitamins
    if minerals:
        final_result['minerals']=minerals
    if traces:
        final_result['traces']=traces

    return final_result

def get_res_details(res_ls: list):
    query_str='''SELECT * FROM res_rules LEFT JOIN res_prop ON res_rules.id=res_prop.res_id WHERE id=%s'''
    for i in res_ls:
        cursor.execute(query_str,(i['res_id'],))
        no_nulls=cursor.fetchone()
        no_nulls={k:v for k,v in no_nulls.items() if v}
        i['details']=no_nulls
        conn.commit()
    return res_ls 

@router.put("/x",status_code=status.HTTP_201_CREATED) 
def update_x_goals(get_current_user: int = Depends(oauth.get_current_user)):
    # Update to respective tables
    final_results=set_goal(get_current_user=get_current_user)
    query_str,in_tup='',tuple()
    if 'macros' in final_results.keys():
        query_str,in_tup=utils.query_strs('update','user_goal_macros','user_id',get_current_user.id,obj=final_results['macros'])
        try:
            cursor.execute(query_str,in_tup)
            final_results['macros']=cursor.fetchone()
            conn.commit()
        except Exception:
            conn.rollback()
            raise HTTPException(status_code=403, detail=f"Error Updating X")

        
    if 'minerals' in final_results.keys():
        final_results['minerals']['user_id']=get_current_user.id
        query_str,in_tup=utils.query_strs('update','user_goal_minerals','user_id',get_current_user.id,obj=final_results['minerals'])
        try:
            cursor.execute(query_str,in_tup)
            final_results['minerals']=cursor.fetchone()
            conn.commit()
        except Exception:
            conn.rollback()
            raise HTTPException(status_code=403, detail=f"Error Updating X")
    if 'vitamins' in final_results.keys():
        final_results['vitamins']['user_id']=get_current_user.id
        query_str,in_tup=utils.query_strs('update','user_goal_vitamins','user_id',get_current_user.id,obj=final_results['vitamins'])
        try:
            cursor.execute(query_str,in_tup)
            final_results['vitamins']=cursor.fetchone()
            conn.commit()
        except Exception:
            conn.rollback()
            raise HTTPException(status_code=403, detail=f"Error Updating X")

    if 'traces' in final_results.keys():
        final_results['traces']['user_id']=get_current_user.id
        query_str,in_tup=utils.query_strs('update','user_goal_traces','user_id',get_current_user.id,obj=final_results['traces'])
        try:
            cursor.execute(query_str,in_tup)
            final_results['traces']=cursor.fetchone()
            conn.commit()
        except Exception:
            conn.rollback()
            raise HTTPException(status_code=403, detail=f"Error Updating X")
    return ORJSONResponse(final_results) 


@router.get("/x",status_code=status.HTTP_201_CREATED) 
def get_x_goals(get_current_user: int = Depends(oauth.get_current_user)):
    result=dict()
    cursor.execute('''SELECT * FROM user_goal_macros WHERE user_id=%s''',(get_current_user.id,))
    result['macros']=cursor.fetchone()
    if result['macros']:
        result['macros'].pop('user_id')
        result['macros']={k:v for k,v in result['macros'].items() if v}
    if not bool(result['macros']):
        result['macros']=None
    cursor.execute('''SELECT * FROM user_goal_minerals WHERE user_id=%s''',(get_current_user.id,))
    result['minerals']=cursor.fetchone()
    if result['minerals']:
        result['minerals'].pop('user_id')
        result['minerals']={k:v for k,v in result['minerals'].items() if v}
    if not bool(result['minerals']):
        result['minerals']=None
    cursor.execute('''SELECT * FROM user_goal_vitamins WHERE user_id=%s''',(get_current_user.id,))
    result['vitamins']=cursor.fetchone()
    if result['vitamins']:
        result['vitamins'].pop('user_id')
        result['vitamins']={k:v for k,v in result['vitamins'].items() if v}
    if not bool(result['vitamins']):
        result['vitamins']=None
    cursor.execute('''SELECT * FROM user_goal_traces WHERE user_id=%s''',(get_current_user.id,))
    result['traces']=cursor.fetchone()
    if result['traces']:
        result['traces'].pop('user_id')
        result['traces']={k:v for k,v in result['traces'].items() if v}
    if not bool(result['traces']):
        result['traces']=None

    result = {k:v for k,v in result.items() if v}
    return dict(result)
