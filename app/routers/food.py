#!/usr/bin/env python
from fastapi import FastAPI, Response, status, HTTPException, APIRouter, Depends
from typing import Optional
from .. import schemas, utils, database,oauth,rules_book
from . import state
from fastapi.responses import ORJSONResponse
import orjson
from collections import Counter
from datetime import datetime
import datetime as dt
import copy
conn,cursor=database.run()
router = APIRouter(
        prefix='/food',
        tags=['Foods'])
#Post, General and others
@router.post("/",status_code=status.HTTP_201_CREATED)
def post_user_food(food_info: schemas.FoodBase,get_current_user: int = Depends(oauth.get_current_user)):
    f_result=dict()
    # if no state, get state
    #saving user id
    user_id=get_current_user.id
    if not food_info.general.state_id:
        #Get state id
        state_id=state.user_state_general(schemas.GeneralState(),get_current_user)
        state_id=orjson.loads(state_id.body)[0]['state_id']
        food_info.general.state_id=state_id
        print("got state_id from query/update")
    if food_info.general.servings_taken:
        #apply servings taken to all the data
        food_info=apply_servings_taken(food_info.dict(exclude_none=True),food_info.general.servings_taken)
    #get FoodBase  General as a dict
    general_info=food_info.general.dict(exclude_none=True)
    # add user_id to that dict
    general_info['user_id']=user_id
    # post it to user_food_general
    general_info=post_food_general(general_info)
    #get the newly created food_entry_id
    food_entry_id=general_info['food_entry_id']
    #use the food_entry_id to post to user_food_Xs tables
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
    #Post/update to general state
    print("input to general state:",general_info)
    state.user_state_general(schemas.GeneralState(**general_info),get_current_user)
    #post/update to state x
    print("input to state_x",f_result)
    state.user_state_x(schemas.StateX(**f_result),get_current_user)
    f_result['general']=general_info
    return f_result
def post_food_general(food_info: dict):
    query_str,in_tup=utils.query_strs('insert','user_food_general',obj=food_info)
    cursor.execute(query_str,in_tup)
    food_info=cursor.fetchone()
    #update general user state
    conn.commit()
    return food_info
def post_user_food_an_x(food_info: dict,tablename:str,food_entry_id: int):
    food_info['food_entry_id']=food_entry_id
    query_str,in_tup=utils.query_strs('insert',f'user_food_{tablename}',obj=food_info)
    cursor.execute(query_str,in_tup)
    food_info=cursor.fetchone()
    conn.commit()
    food_info.pop('food_entry_id')
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
        #######################################################
        #deep copy previous food_entry data
        previous_state=dict()
        previous_state['general']=copy.deepcopy(b_result['general'])
        for k,v in b_result.items():
            if v:
                if k != 'general':
                    previous_state[k]=copy.deepcopy(v)
        ######################################################
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
        # actual update command
        query_str,in_tup=utils.query_strs('update','user_food_general','food_entry_id',food_id,obj=general_info)
        print(query_str)
        print(in_tup)
        cursor.execute(query_str,in_tup)
        f_result['general']=cursor.fetchone()
        conn.commit()
        lss=food_info.keys()
        for x in lss:
            f_result[x]=update_user_food_an_x(food_info[x],x,food_id)
        #HERE we update state general and state x with sub op
        #######################################################################
        # actual state update
        #delete old states 
        #General state 1st
        print("delete input to general state:",state_input)
        state.user_state_general(schemas.GeneralState(**previous_state['general']),get_current_user,op_input='sub')
        #X states 2nd
        previous_state.pop('general')
        print("delete input to state_x",previous_state)
        state.user_state_x(schemas.StateX(**previous_state),get_current_user,op_input='sub')
        ########################################################################
        #HERE we update state general and state x with the NEW DATA sum op
        #######################################################################
        #actual state update
        # update general state
        gg=f_result.pop('general')
        print("UPDATED input to general state:",state_input)
        state.user_state_general(schemas.GeneralState(**gg),get_current_user)
        #update state Xs
        print("UPDATED input to state_x",previous_state)
        state.user_state_x(schemas.StateX(**f_result),get_current_user)
        f_result['general']=gg

        return f_result

    else:
        raise HTTPException(status_code=403, detail=f"no such food_entry_id")

def update_user_food_an_x(food_info: dict,tablename:str,food_entry_id: int):
    #need to 2 update statex, 1- sub op_input, second new update
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
            # delete from state general
            print("delete input to general state:",result)
            state.user_state_general(schemas.GeneralState(**result),get_current_user,op_input='sub')
            #need to update statex, sub op_input
            #1 fetch data from all
            b_result=dict()
            cursor.execute('''SELECT * FROM user_food_macros WHERE food_entry_id=%s''', (food_info.food_entry_id,))
            b_result['macros']=cursor.fetchone()
            #not sure if nesscary, but deleting food_entry_id from StateXs returned queries
            if b_result['macros']:
                b_result['macros'].pop('food_entry_id')
            cursor.execute('''SELECT * FROM user_food_minerals WHERE food_entry_id=%s''', (food_info.food_entry_id,))
            b_result['minerals']=cursor.fetchone()
            if b_result['minerals']:
                b_result['minerals'].pop('food_entry_id')
            cursor.execute('''SELECT * FROM user_food_vitamins WHERE food_entry_id=%s''', (food_info.food_entry_id,))
            b_result['vitamins']=cursor.fetchone()
            if b_result['vitamins']:
                b_result['vitamins'].pop('food_entry_id')
            cursor.execute('''SELECT * FROM user_food_traces WHERE food_entry_id=%s''', (food_info.food_entry_id,))
            b_result['traces']=cursor.fetchone()
            if b_result['traces']:
                b_result['traces'].pop('food_entry_id')
            # None values being taking out
            b_result={k:dict(v) for k,v in b_result.items() if v }
            # delete from stateXs
            print("delete input to state_x",b_result)
            state.user_state_x(schemas.StateX(**b_result),get_current_user,op_input='sub')
            # delete the food entry by deleting it from user_food_general parent table
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
    f_result=dict()
    cursor.execute('''SELECT * FROM user_food_general WHERE food_entry_id=%s''', (food_entry_id,))
    f_result['general']=cursor.fetchone()
    if 'general' in f_result.keys():
        if f_result['general']['user_id']!=int(get_current_user.id):
            raise HTTPException(status_code=403, detail=f"Forrbidden")

        lss=['macros','minerals','vitamins','traces']
        for x in lss:
            cursor.execute(f'''SELECT * FROM user_food_{x} WHERE food_entry_id=%s''', (food_entry_id,))
            f_result[x]=cursor.fetchone()
    else:
        raise HTTPException(status_code=403, detail=f"No such food entry")

    return ORJSONResponse(f_result)
def get_a_food_dict(food_entry_id: int,get_current_user: int = Depends(oauth.get_current_user)):
    f_result=dict()
    cursor.execute('''SELECT * FROM user_food_general WHERE food_entry_id=%s''', (food_entry_id,))
    f_result['general']=cursor.fetchone()
    if 'general' in f_result.keys():
        if f_result['general']['user_id']!=int(get_current_user.id):
            raise HTTPException(status_code=403, detail=f"Forrbidden")

        lss=['macros','minerals','vitamins','traces']
        for x in lss:
            cursor.execute(f'''SELECT * FROM user_food_{x} WHERE food_entry_id=%s''', (food_entry_id,))
            f_result[x]=cursor.fetchone()
    else:
        raise HTTPException(status_code=403, detail=f"No such food entry")
    for k,v in f_result.items():
        if v:
            f_result[k]=dict(v)

    return f_result

@router.get("/history",status_code=status.HTTP_201_CREATED)
def get_food_entries(get_current_user: int = Depends(oauth.get_current_user)):
    f_result=list()
    cursor.execute('''SELECT food_entry_id FROM user_food_general WHERE user_id=%s''', (get_current_user.id,))
    result=cursor.fetchall()
    if result:
        lss=[x['food_entry_id'] for x in result]
        for x in lss:
            f_result.append(get_a_food_dict(x,get_current_user))
        print(f_result)
        print(type(f_result))
    else:
        raise HTTPException(status_code=403, detail=f"No such food entries for the user")
    return ORJSONResponse(f_result)

@router.get("/date",status_code=status.HTTP_201_CREATED)
def get_food_entries(date: str,get_current_user: int = Depends(oauth.get_current_user)):
    f_result=list()
    date1=datetime.combine(datetime.fromisoformat(date),datetime.min.time())
    date2=datetime.combine(datetime.fromisoformat(date),datetime.max.time())
    cursor.execute('''SELECT food_entry_id FROM user_food_general WHERE user_id=%s AND created_at BETWEEN %s AND %s''', (get_current_user.id,date1,date2))
    result=cursor.fetchall()
    if result:
        lss=[x['food_entry_id'] for x in result]
        for x in lss:
            f_result.append(get_a_food_dict(x,get_current_user))
    else:
        raise HTTPException(status_code=403, detail=f"No such food entries for the user")
    return ORJSONResponse(f_result)
