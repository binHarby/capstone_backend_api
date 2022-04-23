import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import settings

def run():
    global conn,cursor
    while True:
        try:
            # need to use envs vars
            conn = psycopg2.connect(host=settings.db_host,database=settings.db_name,user=settings.db_usr,password=settings.db_pass,cursor_factory=RealDictCursor)
            print(type(conn))
            cursor=conn.cursor()
            print("Database Connected!")
            return conn,cursor
        except Exception as error:
            print("DB connection failed")
            print("Error: ", error)
            time.sleep(3)
