#!/usr/bin/env python
from fastapi import FastAPI, Response, status, HTTPException, APIRouter, Depends
from typing import List
from .. import schemas, utils, database,oauth
from fastapi.responses import ORJSONResponse
conn,cursor=database.run()
router = APIRouter(
        prefix='/Exapi',
        tags=['External APIs'])

@router.post("/name", status_code=status.HTTP_201_CREATED)
def post_name(new_rest: schemas.ExapiNameReq, get_current_user: int = Depends(oauth.get_current_user)):
    rest_info=utils.nutrix_name(new_rest.name)
    return ORJSONResponse(rest_info)
@router.post("/upc", status_code=status.HTTP_201_CREATED)
def post_upc(new_rest: schemas.ExapiUPCReq, get_current_user: int = Depends(oauth.get_current_user)):
    rest_info=utils.nutrix_upc(new_rest.upc)
    return ORJSONResponse(rest_info)
