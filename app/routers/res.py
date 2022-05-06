#!/usr/bin/env python
from fastapi import FastAPI, Response, status, HTTPException, APIRouter, Depends
from typing import List
from .. import schemas, utils, database,oauth
conn,cursor=database.run()
router = APIRouter(
        prefix='/res',
        tags=['Restrictions'])
#@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schemas.PostRestReq)
@router.post("/res_rules", status_code=status.HTTP_201_CREATED)
def post_rest(new_rest: schemas.PostRestReq, get_current_user: int = Depends(oauth.get_current_user)):
    new_rest=new_rest.dict(exclude_none=True)
    cursor.execute('''SELECT * FROM res_rules WHERE name=%s LIMIT 1''',(new_rest['name'],))
    query=cursor.fetchone()
    if query:
        raise HTTPException(status_code=403, detail=f"restriction is already in DataBase") 
    # convert datetimes into strings
    new_rest['created_at']=str(new_rest['created_at'])
    new_rest['updated_at']=str(new_rest['updated_at'])
    # end conversion
    cols_ls=list(new_rest.keys())
    in_ls=list(new_rest.values())
    res_pop_flag=False
    if 'res_prop' in new_rest.keys():
        print("restrictions properties are given")
        cols_ls.pop()
        in_ls.pop()
        res_pop_flag=True

    cols_str='('+','.join(map(str,cols_ls))+')'
    in_str_ls=['%s' for _ in in_ls ]
    in_str='('+','.join(map(str,in_str_ls))+')'
    in_tup=tuple(in_ls)
    print(cols_str)
    print(in_str)
    print(in_tup)
    sql_str='''INSERT INTO res_rules '''+cols_str+" VALUES"+in_str+" RETURNING *"
    print(sql_str)
    cursor.execute(sql_str,in_tup)
    result=cursor.fetchone()
    conn.commit()
    if res_pop_flag:
        res_props=dict(new_rest['res_prop'])
        res_props['res_id']=result['id']
        prop_comp_ls=list(res_props.keys())
        prop_comp_vals=list(res_props.values())
        prop_comp_ls_str='('+','.join(map(str,prop_comp_ls))+')'
        vals_str_ls=['%s' for _ in prop_comp_vals ]
        prop_comp_vals_str='('+','.join(map(str,vals_str_ls))+')'
        in_tup=tuple(prop_comp_vals)
        ## Build query and insert into res_props
        sql_str='''INSERT INTO res_prop '''+prop_comp_ls_str+" VALUES"+prop_comp_vals_str+"RETURNING *"
        cursor.execute(sql_str,in_tup)
        res_props=cursor.fetchone()
        conn.commit()
        result['res_prop']=res_props

    return result

@router.delete("/res_rules", status_code=status.HTTP_201_CREATED)
def delete_rest(rest_info: schemas.DeleteRestReq, get_current_user: int = Depends(oauth.get_current_user)):
    rest_unq_col=''
    rest_unq_val=''
    if rest_info.id:
        rest_unq_col='id'
        rest_unq_val=str(rest_info.id)
        rest_info.id=None
    elif rest_info.name:
        rest_unq_col='name'
        rest_unq_val=str(rest_info.name)
    query_str,in_tup=utils.query_strs('delete','res_rules',rest_unq_col,rest_unq_val,rest_info)
    cursor.execute(query_str,in_tup)
    result=cursor.fetchone()
    conn.commit()

@router.put("/res_rules", status_code=status.HTTP_201_CREATED)

def update_rest(rest_info: schemas.UpdateRestReq, get_current_user: int = Depends(oauth.get_current_user)):
    rest_unq_col=''
    rest_unq_val=''
    if rest_info.id:
        rest_unq_col='id'
        rest_unq_val=str(rest_info.id)
        rest_info.id=None
    elif rest_info.name:
        rest_unq_col='name'
        rest_unq_val=str(rest_info.name)
    rest_info=rest_info.dict(exclude_none=True)
    res_prop=None
    if 'res_prop' in rest_info.keys():
        print("Updating res_prop")
        res_prop=rest_info.pop("res_prop")
    #print(rest_unq_col)
    #print(rest_unq_val)
    query_str,in_tup=utils.query_strs('update','res_rules',rest_unq_col,rest_unq_val,rest_info)
    cursor.execute(query_str,in_tup)
    result=cursor.fetchone()
    conn.commit()
    #print(query_str)
    #print(in_tup)
    if res_prop:
        nq_str,nin_tup=utils.query_strs('update','res_prop','res_id',result['id'],res_prop)
        cursor.execute(nq_str,nin_tup)
        nresult=cursor.fetchone()
        conn.commit()
        result['res_prop']=nresult

    return result

@router.get("/res_rules", status_code=status.HTTP_201_CREATED)

def get_rest(rest_info: schemas.GetRestReq, get_current_user: int = Depends(oauth.get_current_user)):
    query_str=''
    in_tup=tuple()
    if rest_info.alll:
        query_str,in_tup=utils.query_strs('get','res_rules',get_all=True)
    else:
        rest_unq_col=''
        rest_unq_val=''
        rest_info=rest_info.dict(exclude_none=True)
        if 'id' in rest_info.keys():
            rest_unq_col='id'
            rest_unq_val=str(rest_info['id'])
            rest_info['id']=None
        elif 'name' in rest_info.keys():
            rest_unq_col='name'
            rest_unq_val=str(rest_info['name'])
        query_str,in_tup=utils.query_strs('get','res_rules',rest_unq_col,rest_unq_val)
    print(query_str)
    print(in_tup)
    cursor.execute(query_str,in_tup)
    result=cursor.fetchall()
    conn.commit()
    return result
