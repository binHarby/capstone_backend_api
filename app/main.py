#!/usr/bin/env python
from fastapi import FastAPI,Response,status,HTTPException 
from typing import List
from . import schemas, utils, database
from .routers import user,login,res,exapi,goal,ai,state,food,med,recommendation,activity
from datetime import date,datetime
from fastapi.middleware.cors import CORSMiddleware



conn,cursor=database.run()
app = FastAPI()
# change allow_origins to allow certain domians and not others
# NOTE: we are not talking to any website, but native apps, so you can keep origins empty 
# Allowing all CORS connections 
app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
        )

@app.get('/')

async def root():
    return {"message": "Hello Capstone!"}
app.include_router(user.router)
app.include_router(login.router)
app.include_router(res.router)
app.include_router(exapi.router)
app.include_router(goal.router)
app.include_router(ai.router)
app.include_router(state.router)
app.include_router(food.router)
app.include_router(recommendation.router)
app.include_router(med.router)
app.include_router(activity.router)
