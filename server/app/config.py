from pydantic_settings import BaseSettings
from functools import lru_cache
class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_ALGORITHM: str
    SECRET_KEY : str
    ACCESS_TOKEN_EXPIRE_MINUTES : str

    class Config:
        env_file = "../.env"

@lru_cache()
def get_settings():
    return Settings()