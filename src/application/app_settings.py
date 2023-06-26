from functools import lru_cache
from pydantic import BaseSettings

class AppSettings(BaseSettings):
    app_name: str = "ECG service"
    running_env: str = ""

    class Config:
        env_file = ".env"

@lru_cache()
def get_setting():
    return AppSettings()
