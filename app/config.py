import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APPTEK_API_TOKEN: str = os.getenv("APPTEK_API_TOKEN", "")

settings = Settings()
