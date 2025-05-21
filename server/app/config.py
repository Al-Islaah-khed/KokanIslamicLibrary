from pydantic_settings import BaseSettings
from functools import lru_cache

from dotenv import load_dotenv
import os
load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv('DATABASE_URL')
    JWT_ALGORITHM: str = os.getenv('JWT_ALGORITHM')
    SECRET_KEY : str = os.getenv('SECRET_KEY')
    ACCESS_TOKEN_EXPIRE_MINUTES : int = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
    CLIENT_BASE_URL : str = os.getenv("CLIENT_BASE_URL")
    GOOGLE_CLIENT_ID : str = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET : str = os.getenv("GOOGLE_CLIENT_SECRET")
    REDIRECT_URL : str = os.getenv("REDIRECT_URL")

@lru_cache()
def get_settings():
    return Settings()