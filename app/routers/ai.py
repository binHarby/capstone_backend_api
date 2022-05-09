#!/usr/bin/env python
from fastapi import FastAPI, Response, status, HTTPException, APIRouter, Depends
from typing import List
from .. import schemas, utils, database,oauth
from fastapi.responses import ORJSONResponse
conn,cursor=database.run()
router = APIRouter(
        prefix='/ai',
        tags=['AI Modules'])
@router.post("/analyize_diabetes", status_code=status.HTTP_201_CREATED)
def analyize_diabetes(get_current_user: int = Depends(oauth.get_current_user)):
    return get_current_user

