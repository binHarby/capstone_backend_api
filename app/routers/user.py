#!/usr/bin/env python
from fastapi import FastAPI, Response, status, HTTPException, APIRouter, Depends
from typing import List
from .. import schemas, utils, database,oauth
from psycopg2 import sql
conn,cursor=database.run()

router = APIRouter(
        prefix='/user',
        tags=['User'])
@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schemas.UserRes)

def create_users(new_user: schemas.UserCreate):
    cursor.execute('''SELECT * FROM users WHERE email=%s LIMIT 1''',(new_user.email,))
    query=cursor.fetchone()
    if query:
        raise HTTPException(status_code=403, detail=f"account with email {new_user.email} already exists,try another email")

    if new_user.password == new_user.confpassword:
        new_user.password = utils.hash(new_user.password)
    else:
        raise HTTPException(status_code=418, detail=f"Input Passwords Mismatch")
    age = utils.get_age(new_user.birthday)
    bmi = utils.get_bmi(new_user.weight,new_user.height)
    tdee = utils.get_tdee(new_user.gender,new_user.weight,new_user.height,age,new_user.activity)
    tdee = tdee - new_user.cal_diff
    cursor.execute('''INSERT INTO users (gender,email,birthday,password,bloodtype,weight,height,age, bmi,cal_goal,cal_diff,tdee,cal_current,created_at,updated_at) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING *''',(new_user.gender,new_user.email,new_user.birthday,new_user.password,
        new_user.bloodtype,new_user.weight,new_user.height,age,bmi,tdee-new_user.cal_diff,new_user.cal_diff,tdee,0,new_user.created_at,new_user.updated_at))
    new_user=cursor.fetchone()
    conn.commit()
    return new_user

@router.get("/", status_code=status.HTTP_201_CREATED,response_model=List[schemas.UserRes])

def get_users(get_current_user: int = Depends(oauth.get_current_user)):
    
    cursor.execute('''SELECT * FROM users''')
    query=cursor.fetchall()
    if query:
        return query
    else:
        raise HTTPException(status_code=418, detail=f"no users exist")


@router.delete("/", status_code=204)

def delete_user(user_info: schemas.UserDelete,get_current_user: int = Depends(oauth.get_current_user)):
    # id 1 is admin
    if user_info.id == get_current_user.id or int(get_current_user.id)==1:
        cursor.execute('''DELETE FROM users WHERE id=%s RETURNING *''',(user_info.id,))
        auser=cursor.fetchone()
        conn.commit()
        if auser== None:
            raise HTTPException(status_code=404, detail="problem deleteing user")
        return Response(status_code=204)
    else:
        return {"notsure":"why"}



@router.put("/{id}", status_code=201)
@router.patch("/{id}", status_code=201)

def update_user(id: int , user_info: schemas.UserUpdate,get_current_user: int = Depends(oauth.get_current_user)):
    user_info=user_info.dict(exclude_none=True) 
    # Debugging Query building
    #print(user_info," type: ", type(user_info))
    #print("----keys and values---")
    #print(user_info.keys())
    #print(user_info.items())
    #print(','.join(user_info.keys()))
    #print(','.join(map(str,user_info.values())))
    #lss=[ (str(k),str(v)) for k,v in user_info.items() ]
    #print(lss)
    # Insert to DB here
    ## building the update string
    querystr='''UPDATE users SET '''
    tmpls=list()
    for k in user_info.keys():
        tmpls.append(f'{k}=%s ')
    querystr+=','.join(tmpls)+'WHERE id=%s RETURNING *'
    # convert all inputs to str for security 
    inputs_tup=list(map(str,user_info.values()))
    # add id 
    inputs_tup.append(str(id))
    inputs_tup=tuple(inputs_tup)
    print(querystr)
    print(inputs_tup)
    cursor.execute(querystr,inputs_tup)
    result=cursor.fetchone()
    conn.commit()
    if result== None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")

    return result
        


@router.get("/single", status_code=status.HTTP_201_CREATED,response_model=List[schemas.UserRes])

def get_user(get_current_user: int = Depends(oauth.get_current_user)):
    
    cursor.execute('''SELECT * FROM users WHERE id=%s''',(get_current_user.id,))
    query=cursor.fetchall()
    if query:
        return query
    else:
        raise HTTPException(status_code=418, detail=f"user doesn't exist any more?")
