#!/usr/bin/env python
import shutil
from fastapi import FastAPI, Response, status, HTTPException, APIRouter, Depends, UploadFile, File,Request
from typing import List
from .. import schemas, utils, database,oauth
from fastapi.responses import ORJSONResponse
import ast
import requests
## Image api libs
import os
import io
from pprint import pprint 
from PIL import Image
import httpx
import urllib
from tempfile import NamedTemporaryFile
import datetime as dt
from . import state,goal,res
import orjson
from collections import Counter
conn,cursor=database.run()
router = APIRouter(
        prefix='/Exapi',
        tags=['External APIs'])

@router.post("/name", status_code=status.HTTP_201_CREATED)
def post_name(new_rest: schemas.ExapiNameReq, get_current_user: int = Depends(oauth.get_current_user)):
    rest_info=utils.nutrix_name(new_rest.name)
    if 'error' not in rest_info.keys():
        #rest_info.pop('is_raw')
        serv_weight=rest_info.pop('serving_weight')
        photo=rest_info.pop('photo')
        measures=rest_info.pop('measures')
        hashMap=rest_info.pop("hash_map",None)
        calDiff=rest_info.pop("cals_diff",None)
        new_m=list()
        for x in measures:
            newdict=dict()
            for k,v in x.items():
                if k == 'measure':
                    print(k,v)
                    newdict['unit']=v
                elif k == 'serving_weight':
                    newdict['servingWeight']=v
            if newdict:
                new_m.append(newdict)
        measures=new_m
        rest_info=utils.format_x(rest_info)
        rest_info['meta']=dict()
        rest_info['meta']["def_w"]=serv_weight
        rest_info['meta']['photo']=photo
        rest_info['meta']['measures']=measures
        rest_info["hash_map"]=hashMap
        rest_info["cals_diff"]=calDiff

    rest_info['recom']=recommendation(rest_info,get_current_user)
    rest_info.pop("hash_map",None)
    rest_info.pop("cals_diff",None)
    return ORJSONResponse(rest_info)
@router.post("/upc", status_code=status.HTTP_201_CREATED)
def post_upc(new_rest: schemas.ExapiUPCReq, get_current_user: int = Depends(oauth.get_current_user)):
    rest_info=utils.nutrix_upc(new_rest.upc)
    if 'error' not in rest_info:
        rest_info=utils.format_x(rest_info)
        rest_info['recom']=recommendation(rest_info,get_current_user)
        rest_info.pop("hash_map",None)
        rest_info.pop("cals_diff",None)

    return ORJSONResponse(rest_info)

@router.post("/image", status_code=status.HTTP_201_CREATED)
async def post_image(request: Request,file: UploadFile=File(...),get_current_user: int = Depends(oauth.get_current_user)):
    url = 'https://api-2445582032290.production.gw.apicast.io/v1/foodrecognition?user_key=6d44fe497a4a4733bb0b86014d64ee42'
    contents = await file.read()
    file_copy = NamedTemporaryFile('wb', delete=False)
    f,newstream,outfile,resp = None,None,None,None
    foodai=utils.FoodAI()
    foodai.connect()

    try:
        # The 'with' block ensures that the file closes and data are stored
        with file_copy as f:
            f.write(contents);
        
        # Here, upload the file to your S3 service
        # You can reopen the file as many times as desired. 
        img=open(file_copy.name, 'rb')
        img=io.BytesIO(img.read())
        img=Image.open(img).resize((544,544))
        outfile=io.BytesIO()
        img.save(outfile,"jpeg",quality=100)
        resp=foodai.recognize(outfile.getvalue())
        pprint(resp)

    finally:
        if f is not None:
            f.close() # Remember to close any file instances before removing the temp file
        if newstream is not None: 
            newstream.close()
        if outfile is not None:
            outfile.close()
        os.unlink(file_copy.name)  # unlink (remove) the file from the system's Temp folder
        if resp['is_food']:
            resp=utils.process_mama(resp)
        else:
            resp={'error':'cant recoginize food'}
        resp['recom']=recommendation(resp,get_current_user)
    return resp
def recommendation(obj:dict, get_current_user: int = Depends(oauth.get_current_user)):
    #obj is the food
    lvlValues={"normal":1,"controlled":0.8,"uncontrolled": 0.65}
    hashMap=obj["hash_map"]
    calDiff=obj["cals_diff"]
    obj.pop("hash_map",None)
    obj.pop("cals_diff",None)


    #obj2 is user state
    obj2=dict()
    obj2['general']=state.user_state_general(schemas.GeneralState(),get_current_user)
    obj2['general']=orjson.loads(obj2['general'].body)[0]
    tempObj=dict()
    tempObj['macros'],tempObj['minerals'],tempObj['vitamins'],tempObj['traces']=dict(),dict(),dict(),dict()
    tempObj=state.user_state_x(schemas.StateX(**tempObj),get_current_user)
    print(f"\n\n\ntempObj from state x: {tempObj}\n\n\n")
    if 'macros' in tempObj.keys():
        obj2['macros']=tempObj['macros']
    if 'vitamins' in tempObj.keys():
        obj2['vitamins']=tempObj['vitamins']

    if 'minerals' in tempObj.keys():
        obj2['minerals']=tempObj['minerals']
    if 'traces' in tempObj.keys():
        obj2['traces']=tempObj['traces']
    ## adjusting for hashmap and calDiff
    # if hashmap not null, get level, compare it to the levelsValues
    #then change carb, and calories
    if hashMap:
        #new carb
        tmp=obj2["macros"]["carb"]
        obj2["macros"]["carb"]=obj2["macros"]["carb"]*lvlValues[hashMap["diabetes"]]
        carbDiff=tmp-obj2["macros"]["carb"]
        #new calories
        #NOTE:each carb gram is 4 calories
        carbCalDiff=carbDiff*4
        obj2["general"]["total_cals"]=obj2["general"]["total_cals"]-carbCalDiff
        #new sodium 

        obj2["minerals"]["sodium"]=obj2["minerals"]["sodium"]*lvlValues[hashMap["blood_preasure"]]
    if calDiff:
        # add cals burned to carbs and sodium 
        # sodium has no cals, keep in mind
        #TODO: make sure hashmap and caldiff stay in recommendation input but not in final output
        #TODO2: set new values for sodium and cals based od calDiff
        
        calInGrams=calDiff/4
        tmp=obj2["macros"]["carb"]
        obj2["macros"]["carb"]=obj2["macros"]["carb"]+(calInGrams*0.5)
        #new calories
        #NOTE:each carb gram is 4 calories
        carbCalDiff=calDiff*0.5
        obj2["general"]["total_cals"]=obj2["general"]["total_cals"]+carbCalDiff

        obj2["minerals"]["sodium"]=obj2["minerals"]["sodium"]+(calInGrams*0.5)
    print(f"obj: {obj}")
    print(f"obj2: {obj2}")
    #obj3 is user goals
    obj3=goal.get_x_goals(get_current_user)
    obj3['general']=goal.get_general_goals(get_current_user)

    print()
    print()
    print()
    print(f"obj3 (Goals):\n{obj3}")
    tempObj,macros,vitamins,traces,minerals,general=dict(),Counter(dict()),Counter(dict()),Counter(dict()),Counter(dict()),Counter(dict())
    for k,v in obj.items():
        if k == 'macros':
            macros+=Counter(v)
        if k=='vitamins':
            vitamins+=Counter(v)
        if k=='minerals':
            traces+=Counter(v)
        if k=='traces':
            minerals+=Counter(v)

    for k,v in obj2.items():
        if k == 'macros':
            macros+=Counter(v)
        if k=='vitamins':
            vitamins+=Counter(v)
        if k=='minerals':
            traces+=Counter(v)
        if k=='traces':
            minerals+=Counter(v)
    tempObj['general']={"total_cals":obj['general']['total_cals']+obj2['general']['total_cals']}
    tempObj['macros']=dict(macros)
    tempObj['vitamins']=dict(vitamins)
    tempObj['minerals']=dict(minerals)
    tempObj['traces']=dict(traces)

    print()
    print()
    #obj+obj2(state+food) current standing
    print(f"obj+obj2:\n {tempObj}")


    
    

    # (obj3 -(obj+obj2)) (goals -(state+food)):  standing after eating
    obj3['general']={"total_cals": obj3['general']['cal_goal']}
    tempObj=subtract_dicts(obj3,tempObj)

    print()
    print()
    #obj+obj2(state+food) current standing
    print(f"goals-(state+food)\n {tempObj}\n\n")

    
    # POST SUB 1: check if a componant is exceeded 
    groupsToComps=list()
    listOfComps=list()
    for k,v in tempObj.items():
        for k2,v2 in v.items():
            if v2<0:
                dd={"group":k,"comp":k2,"overBy":-1*v2}
                listOfComps.append(k2)
                groupsToComps.append(dd)

    print()
    print()
    print()
    print(f"brief {groupsToComps}")

    # POST SUB 2: loop through all the user illnesses, see if one them matches with the exceeded componant
    restReqDict={ "alll": True }
    user_rest_list=res.get_user_rest(schemas.GetUserRestReq(**restReqDict),get_current_user)
    user_rest_list=orjson.loads(user_rest_list.body)

    res_id_list=list()
    for obj in user_rest_list:
        for k,v in obj.items():
            if k == "res_id":
                res_id_list.append({"id":v})
    print(f"\n\n\nUser Restrictions Ids: \n {res_id_list}\n\n\n")

    res_list = res.get_rest(schemas.GetRestReq(**restReqDict),get_current_user)
    res_list = orjson.loads(res_list.body)
    selected_ress=list()
    for idd in res_id_list:
        for k,v in idd.items():
            for ress in res_list:
                if ress['id']==v:
                    selected_ress.append(ress)
    #brief listOfComps
    # brief detaild groupsToComps
    # Report selected_ress
    recom=dict()
    recom['brief']= listOfComps
    recom['detail']= groupsToComps
    recom['report']=selected_ress
    return recom
            


    # get all user
    # recommendation is an object that has 3 sections
    # brief, detailed brief, report stack 
    # brief: related diseases names
    # brief detailed: brief + food componants
    # report : brief detailed + structure and more words
def subtract_dicts(old: dict,new: dict):
    # figure out a way to subtract between two dicts, of different ke    ys
    result=dict()
    for k,v in new.items():
        if k in old.keys():
            if type(old[k]) is dict:
                result[k]=subtract_dicts(old[k],v)
            else:
                result[k]=old[k]-v

    return result
