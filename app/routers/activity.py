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
        prefix='/activity',
        tags=['activities'])
@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schemas.UserRes)

def post_activity(get_current_user: dict):
    return get_current_user
