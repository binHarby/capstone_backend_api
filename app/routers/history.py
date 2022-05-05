#!/usr/bin/env python
from fastapi import FastAPI, Response, status, HTTPException, APIRouter,Depends
from typing import List
from datetime import datetime
from .. import schemas, utils, database,oauth
conn,cursor = database.run()

router = APIRouter(
        prefix='/history',
        tags=['/history']
        )
# CRUD Food
@router.post("/food", status_code=status.HTTP_201_CREATED, response_model=List[schemas.PostFoodRes])
def get_food_history(user_food: schemas.PostFoodReq,get_current_user: int = Depends(oauth.get_current_user)):
    return user_food

@router.get("/food", status_code=status.HTTP_201_CREATED, response_model=List[schemas.GetFoodRes])

def get_food_history(user_food_history: schemas.GetFoodReq,get_current_user: int = Depends(oauth.get_current_user)):
    if not user_food_history.frm:
        # set user_food_history.frm to today
        user_food_history.frm=datetime.utcnow().date()
        # set user_food_history.from to beginning of the day at 00:00
        user_food_history.frm=datetime.combine(user_food_history.frm,datetime.min.time())
    if user_food_history.frm.date()>=user_food_history.too.date():
        cursor.execute('''SELECT * FROM user_food WHERE user_id=%s AND created_at>=%s AND created_at<=%s''',(get_current_user.id,user_food_history.frm,
            user_food_history.too))
        food_hist=cursor.fetchall()
        return food_hist

    else:
        raise HTTPException(status_code=418,detail=f"invalid date")

#@router.post("/food", status_code=status.HTTP_201_CREATED,response_model=schemas.PostFoodRes)
#def post_food(user_food_history: schemas.PostFoodReq,get_current_user: int = Depends(oauth.get_current_user)):

    
