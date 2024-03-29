from passlib.context import CryptContext
from .config import settings
from datetime import date
from typing import Optional
import orjson
import requests
import os
import io
from pprint import pprint
from PIL import Image
import httpx
import urllib

pwd_context=CryptContext(schemes=[settings.pass_algo],deprecated="auto")
def hash(password: str):
    return pwd_context.hash(password)
def verify(txt_pass,hashed_pass):
    return pwd_context.verify(txt_pass,hashed_pass)
def get_bmi(weight,height):
    # height should be in meters, weight should be in kg (from app)
    return int(weight//(height*height))
def get_age(birthday):
    year,month,day=birthday.split('-')
    print(f"Day: {day}, Month: {month}, Year: {year}")
    today=date.today()
    age=(today.year - int(year)) - ((today.month, today.day) < (int(month), int(day)))
    return age

def get_bmr(gender,weight,height,age):
    # height should be in meters, weight should be in kg (from app)
    # age should be calculated before this
    # converting height to cm by *100
    if gender == 'male':
        bmr = 66 + (13.7*weight) +(5*height*100)-(6.8 *age)
    else: 

        bmr = 655 + (9.6*weight) +(1.8*height*100)-(4.7 *age)
    return bmr
def get_tdee(gender,weight,height,age,activity):
    bmr = get_bmr(gender,weight,height,age)
    if(activity==0):
        tdee = bmr*1.2
    elif(activity==1):
        tdee = bmr*1.375
    elif(activity==2):
        tdee = bmr*1.55
    elif(activity==3):
        tdee = bmr*1.725
    elif(activity>=4):
        tdee = bmr*1.9
    return int(tdee)
def query_strs(method: str, tablename: str,unq_col: Optional[str]=None,unq_val: Optional[str]=None, obj: Optional[dict]=None,get_all: Optional[bool]=False):
    # PASS ONLY ONE LVL DICTs
    query_str=''
    in_tup=tuple()
    if method.lower()=='insert':
        # INSERT INTO tablename (col, ...) VALUES (%s, ...) RETURNING *, input=tuple
        query_str=f'INSERT INTO {tablename} '
        cols_str='('+','.join(map(str,list(obj.keys())))+')'
        in_spf_ls=[ '%s' for _ in obj.keys()]
        in_spf_str=' VALUES'+'('+','.join(in_spf_ls)+') RETURNING *'
        in_tup=tuple(obj.values())
        query_str+=cols_str+in_spf_str
        return query_str,in_tup
    elif method.lower()=='update':
        # UPDATE tablename SET {col1}=%s ... WHERE unq=%s RETURNING *, input=tuple
        query_str=f'UPDATE {tablename} SET '
        tmpls=list()
        for key in obj.keys():
            tmpls.append(f'{key}=%s ')
        query_str+=','.join(tmpls)+f'WHERE {unq_col}=%s RETURNING *'
        # processing input tuple
        if f'{unq_col}' in obj.keys() and f'{unq_col}'=='id':
            obj.pop(f'{unq_col}')
        in_tup=list(obj.values())
        in_tup.append(unq_val)
        in_tup=tuple(in_tup)
        return query_str,in_tup
    elif method.lower()=='delete':
        query_str=f'DELETE FROM {tablename} WHERE {unq_col}=%s RETURNING *'
        in_tup=(unq_val,)
        return query_str,in_tup
    elif method.lower()=='get':
        if get_all:
            query_str=f"SELECT * FROM {tablename} "
        else:
            query_str=f"SELECT * FROM {tablename} WHERE {unq_col}=%s "
            in_tup=(unq_val,)
        return query_str,in_tup

## UPC processing of nutrix
def upc_lookup_table(key: str):
    '''
['old_api_id', 'item_id', 'item_name', 'leg_loc_id', 'brand_id', 'brand_name', 'item_description', 'updated_at', 'nf_ingredient_statement', 'nf_water_grams', 'nf_calories', 'nf_calories_from_fat', 'nf_total_fat', 'nf_saturated_fat', 'nf_trans_fatty_acid', 'nf_polyunsaturated_fat', 'nf_monounsaturated_fat', 'nf_cholesterol', 'nf_sodium', 'nf_total_carbohydrate', 'nf_dietary_fiber', 'nf_sugars', 'nf_protein', 'nf_vitamin_a_dv', 'nf_vitamin_c_dv', 'nf_calcium_dv', 'nf_iron_dv', 'nf_refuse_pct', 'nf_servings_per_container', 'nf_serving_size_qty', 'nf_serving_size_unit', 'nf_serving_weight_grams', 'allergen_contains_milk', 'allergen_contains_eggs', 'allergen_contains_fish', 'allergen_contains_shellfish', 'allergen_contains_tree_nuts', 'allergen_contains_peanuts', 'allergen_contains_wheat', 'allergen_contains_soybeans', 'allergen_contains_gluten', 'usda_fields']
    '''
    ans=''
    if key=='item_name':
        ans='food_name'
    elif key=='nf_sugars':
        ans ='sugar'
    elif key == 'nf_protein':
        ans = 'protein'
    elif key == 'nf_vitamin_c_dv':
        ans = 'c'
    elif key == 'nf_vitamin_a_dv':
        ans = 'a'
    elif key == 'nf_calcium_dv':
        ans ='calcium'
    elif key == 'nf_iron_dv':
        ans = 'iron'
    elif key == 'nf_polyunsaturated_fat':
        ans ='polyunsaturated'
    elif key == 'nf_monounsaturated_fat':
        ans = 'monounsaturated'
    elif key == 'nf_cholesterol':
        ans= 'cholesterol'
    elif key == 'nf_sodium':
        ans = 'sodium'
    elif key == 'nf_total_carbohydrate':
        ans ='carb'
    elif key == 'nf_dietary_fiber':
        ans = 'fiber'
    elif key=='brand_name':
        ans='brand_name'
    elif key == 'nf_ingredient_statement':
        ans='ingredients'
    elif key == 'nf_calories':
        ans='total_cals'
    elif key == 'nf_total_fat':
        ans='fat'
    elif key == 'nf_saturated_fat':
        ans='saturated'
    elif key == 'nf_trans_fatty_acid':
        ans ='trans'
    #elif key == 'nf_servings_per_container':
    #    ans ='servings'
    elif key == 'nf_serving_size_qty':
        ans= 'servings'
    elif key == 'nf_serving_size_unit':
        ans = 'serving_size_unit'
    #elif key == 'nf_serving_weight_grams':
    #    ans = 'serving_weight'
    return ans
def process_upc(obj: dict):
    # Skip errors, in utils raise http 404
    if 'status_code' in obj.keys():
        print("Not in Database")
        return {'error': f"{obj['status_code']}"}
    else:
        print("Food in DB")
        obj={ k:v for k,v in obj.items() if v }
        new_obj=dict()
        for k,v in obj.items():
            newk=upc_lookup_table(str(k))
            if newk !='':
                new_obj[newk]=v
        return new_obj
def process_mama(obj):
    obj=obj['top_results'][0]
    lu_table={
"calcium":"calcium",
"saturatedFat": "saturated",
"monounsaturatedFat": "monounsaturated",
"sodium": "sodium",
"totalFat": "fat",
#"cholesterol": "cho",
"iron": "iron",
"polyunsaturatedFat": "polyunsaturated",
"totalCarbs": "carb",
"protein": "protein",
"potassium": "potassium", 
"vitaminA": "a",
"vitaminC": "c",
"calories": "total_cals",
"sugars": "sugar",
"name": "food_name",
"brand":"brand_name"}
    newobj=obj['nutrition'] 
    multiple=obj['servingSizes'][0]['servingWeight']
    unit_def=obj['servingSizes'][0]['unit']

    tmpobj=dict()
    score=0
    measures=list()
    for k,v in newobj.items():
        if k in lu_table.keys():
            newv=round(v*1000*multiple)
            if lu_table[k] =='total_cals':
                tmpobj[lu_table[k]]=v*multiple 
            elif newv !=0:
                tmpobj[lu_table[k]]=newv
    newobj=dict()
    if 'name' in obj.keys():
        tmpobj['food_name']=obj.pop('name')
    if 'brand' in obj.keys():
        tmpobj['brand_name']=obj['brand']
    if 'score' in obj.keys():
        newobj['score']=obj.pop('score')
    if 'servingSizes' in obj.keys():  
        obj.pop('servingSizes')
        newobj['serving_size_unit']=unit_def
       # 
       # newobj['measures']=obj.pop('servingSizes')
       # newobj['measures']
       # for x in newobj['measures']:
       #     for k,v in x.items():
       #         if k == 'servingWeight':
       #             x[k]=round(v*1000)
    obj=format_x(tmpobj)
    obj['meta']=newobj
    return obj
def nutrix_upc(upc_code):
    url=settings.nutrix_upc_endp
    querystring = {"upc":str(upc_code)}
    headers = {
            settings.nutrix_upc_key1: settings.nutrix_upc_val1 ,
            settings.nutrix_upc_key2: settings.nutrix_upc_val2
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    #parsed json response
    par=orjson.loads(response.text)

    #return json response as json object / dict
    return process_upc(par)
def check_float(val: str):
    try:
        float(val)
        return True
    except:
        return False

## dish name processing of nutrix
## Returns:
# carb: int
# fat: int
# fiber: int
# food_name: int
# is_raw: bool
# measures: list of dicts of different measures
#       -"measure":"cup|oz etc"
#       -"qty": int number of default qty
#       -"serving_weight": int, weight in grams
# photo: dict 
#   -"highres": url to HD photo
#   -"thumb": url to thumbnail
#potassium: int
#protein: int
#serving_weight: int seems to be always in g
#etc..
def name_lookup_table(key: str):
    '''
    '''
    ans=''
    if key=='food_name':
        ans='food_name'
    elif key=='nf_potassium':
        ans = 'potassium'
    #elif key == 'metadata':
    #    ans='is_raw'
    elif key == 'alt_measures':
        ans = 'measures'
    elif key == 'photo':
        ans = 'photo'
    elif key=='nf_sugars':
        ans ='sugar'
    elif key == 'nf_protein':
        ans = 'protein'
    elif key == 'nf_vitamin_c_dv':
        ans = 'c'
    elif key == 'nf_vitamin_a_dv':
        ans = 'a'
    elif key == 'nf_calcium_dv':
        ans ='calcium'
    elif key == 'nf_iron_dv':
        ans = 'iron'
    elif key == 'nf_polyunsaturated_fat':
        ans ='polyunsaturated'
    elif key == 'nf_monounsaturated_fat':
        ans = 'monounsaturated'
    elif key == 'nf_cholesterol':
        ans= 'cholesterol'
    elif key == 'nf_sodium':
        ans = 'sodium'
    elif key == 'nf_total_carbohydrate':
        ans ='carb'
    elif key == 'nf_dietary_fiber':
        ans = 'fiber'
    elif key=='brand_name':
        ans='brand_name'
    elif key == 'nf_ingredient_statement':
        ans='ingredients'
    elif key == 'nf_calories':
        ans='total_cals'
    elif key == 'nf_total_fat':
        ans='fat'
    elif key == 'nf_saturated_fat':
        ans='saturated'
    elif key == 'nf_trans_fatty_acid':
        ans ='trans'
    elif key == 'serving_qty':
        ans ='servings'
    elif key == 'serving_unit':
        ans = 'serving_size_unit'
    elif key == 'serving_weight_grams':
        ans = 'serving_weight'
    return ans
def process_name_api(obj: dict):
    if 'message' in obj.keys():
        print("Not in Database")
        return {'error': '404',"message": f"{obj['message']}"}
    else:
        print("Food in DB")
        obj=dict(obj['foods'][0])
        # clear Nulls
        obj={k:v for k,v in obj.items() if v}
        for k,v in obj.items():
            if v:
                if v is float or check_float(v):
                    obj[k]=int(v)
                else:
                    obj[k]=v
        new_obj=dict()
        for k,v in obj.items():
            newk=name_lookup_table(str(k))
            if newk !='':
                new_obj[newk]=v
        #new_obj['is_raw']=new_obj['is_raw']['is_raw_food']
        # removing null values in measures
        mea=new_obj['measures'] # a list of dicts
        for idx,obj in enumerate(mea):
            new_dict=dict()
            for k,v in obj.items():
                if v:
                    if v is float or check_float(v):
                        new_dict[k]=int(v)
                    else:
                        new_dict[k]=v
            mea[idx]=new_dict
        new_obj['measures']=mea

        return new_obj


def nutrix_name(name):
    url=settings.nutrix_name_endp
    food_name=name
    querystring = {"query":food_name}
    headers = {
        settings.nutrix_name_key1: settings.nutrix_name_val1,
        settings.nutrix_name_key2: settings.nutrix_name_val2
        }
    
    response = requests.request("POST", url, headers=headers, json=querystring)
    #parsed json response
    
    par=orjson.loads(response.text)
    par=process_name_api(par)
    return par

class FoodAI:
    def __init__(self):
        self.user_key = '6d44fe497a4a4733bb0b86014d64ee42'
        #self.endpoint = os.environ.get("ENDPOINT", "https://api3.azumio.com/")
        self.endpoint = "https://api-2445582032290.production.gw.apicast.io/"

    def connect(self):
        self.client = httpx.Client(http2=False)

    def recognize(self, image, persistent=True):
        headers = {
            "Content-Type": "image/jpeg",
            "Accept-Encoding": "gzip"
        }

        if persistent:
            pp=os.path.join(self.endpoint, "v1/foodrecognition/full") + "?user_key=" +urllib.parse.quote(self.user_key)
            print(pp)
            foods = self.client.post(pp + "&top=1", content=image, headers=headers)
        else:
            foods = httpx.post(os.path.join(self.endpoint, "v1/foodrecognition/full") + "?user_key=" +
                               urllib.parse.quote(self.user_key) + "&top=1", content=image, headers=headers)

        j = foods.json()
        pprint(j)
        if "is_food" not in j:
            raise BaseException("Failed request", j)

        return j

    def ping(self):
        pong = self.client.get(self.endpoint)
        print(pong.text[:100])

def format_x(obj):
    macros=['carb', 'sugar', 'fructose', 'lactose', 'protein', 'amino', 'fat', 'unsaturated', 'monounsaturated', 'polyunsaturated', 'saturated', 'fiber', 'trans']
    vitamins=['b', 'b_1', 'b_2', 'b_3', 'b_8', 'b_5', 'b_6', 'b_7', 'b_12', 'choline', 'a', 'c', 'd', 'd_2', 'd_3', 'k_1', 'k_2', 'k_3', 'k', 'e']
    traces=['boron', 'copper', 'selenium', 'maganese', 'fluorine', 'chromium', 'cobalt', 'iodine']
    minerals=['calcium', 'phosphorus', 'magnesium', 'sodium', 'potassium', 'iron', 'zinc']
    general=['food_name','servings','servings_taken','total_cals','cal_per_serv','brand_name','ingredients','serving_size_unit','score']
    result=dict()
    result['general'],result['macros'],result['vitamins']=dict(),dict(),dict()
    result['traces'],result['minerals']=dict(),dict()
    for k,v in obj.items():
        if k in macros:
            result['macros'][k]=v
        elif k in vitamins:
            result['vitamins'][k]=v
        elif k in traces:
            result['traces'][k]=v
        elif k in macros:
            result['minerals'][k]=v
        elif k in general:
            result['general'][k]=v
    result={k:v for k,v in result.items() if v}
    return result

