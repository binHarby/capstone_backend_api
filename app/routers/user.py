#!/usr/bin/env python
from fastapi import FastAPI, Response, status, HTTPException, APIRouter
from typing import List
from .. import schemas, utils, database

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
        raise HTTPException(status_code=418, details=f"Input Passwords Mismatch")
    age = utils.get_age(new_user.birthday)
    bmi = utils.get_bmi(new_user.weight,new_user.height)
    tdee = utils.get_tdee(new_user.gender,new_user.weight,new_user.height,age,new_user.activity)
    tdee = tdee - new_user.cal_diff
    cursor.execute('''INSERT INTO users (gender,email,birthday,password,bloodtype,weight,height,age, bmi,cal_goal,cal_diff,tdee,cal_current) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING *''',(new_user.gender,new_user.email,new_user.birthday,new_user.password,
        new_user.bloodtype,new_user.weight,new_user.height,age,bmi,tdee-new_user.cal_diff,new_user.cal_diff,tdee,0))
    new_user=cursor.fetchone()
    conn.commit()
    return new_user
    
