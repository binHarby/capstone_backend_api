import os
from pydantic import BaseSettings,HttpUrl

class Settings(BaseSettings):
    #importing settings from .env
    fast_api_host: str
    db_host: str
    db_usr: str
    db_name: str
    db_pass: str
    s_key: str
    fast_api_port: int
    pass_algo: str
    varify_pass_algo: str
    nutrix_name_endp: str
    nutrix_name_key1: str
    nutrix_name_key2: str
    nutrix_name_val1: str
    nutrix_name_val2: str
    nutrix_upc_endp: str
    nutrix_upc_key1: str
    nutrix_upc_key2: str
    nutrix_upc_val1: str
    nutrix_upc_val2: str

    class Config:
        env_file = ".env"
settings = Settings()
