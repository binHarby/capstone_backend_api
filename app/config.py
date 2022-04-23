import os
from pydantic import BaseSettings

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
    class Config:
        env_file = ".env"
settings = Settings()
