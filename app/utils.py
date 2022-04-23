from passlib.context import CryptContext
from .config import settings
from datetime import date
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

