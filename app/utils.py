from passlib.context import CryptContext
from .config import settings
from datetime import date
from typing import Optional
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
        in_tup=tuple(unq_val)
        return query_str,in_tup
    elif method.lower()=='get':
        if get_all:
            query_str=f"SELECT * FROM {tablename}"
        else:
            query_str=f"SELECT * FROM {tablename} WHERE {unq_col}=%s "
            in_tup=(unq_val,)
        return query_str,in_tup
