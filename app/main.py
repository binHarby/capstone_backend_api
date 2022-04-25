#!/usr/bin/env python
from fastapi import FastAPI,Response,status,HTTPException 
from typing import List
from . import schemas, utils, database
from .routers import user,login,history
from datetime import date,datetime

conn,cursor=database.run()
app = FastAPI()

@app.get('/')

async def root():
    return {"message": "Hello Capstone!"}
app.include_router(user.router)
app.include_router(login.router)
app.include_router(history.router)
