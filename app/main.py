#!/usr/bin/env python
from fastapi import FastAPI,Response,status,HTTPException 
from typing import List
from . import schemas, utils, database
from .routers import user
from datetime import date,datetime

conn,cursor=database.run()
app = FastAPI()

@app.get('/')

async def root():
    return {"message": "Hello Capstone!"}
app.include_router(user.router)
