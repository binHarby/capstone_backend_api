#!/usr/bin/env python
from fastapi import FasAPI, Response, status, HTTPException, APIRouter
from typing import List
from datetime import datetime
from .. import schemas, utils, database
conn,cursor = database.run()

router = APIRouter(
        prefix='/history',
        tags=['/history']
        )
@router.get("/food", status_code=status.HTTP_201_CREATED)

def get_food_history(user_food_history: schemas.FoodHistory):
    if not user_food_history.frm:
        # set user_food_history.frm to today
        user_food_history.frm=datetime.utcnow().date()
        # set user_food_history.from to beginning of the day at 00:00
        user_food_history=datetime.combine(user_food_history.frm,datetime.min.time())
    if user_food_history.frm.date()>=user_food_history.too.date():
        cursor.execute('''SELECT * FROM history_food WHERE id=%s AND time>%s AND time<%s''',(get_current_user.id,user_food_history.frm,
            user_food_history.too))

    else:
        raise HTTPException(status_code=418,detail=f"invalid date")

