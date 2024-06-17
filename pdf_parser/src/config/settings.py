from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    base_url: Optional[str]
    api_key: Optional[str]
    ai_model_name: Optional[str]
    temperature: Optional[float]
    
    # model_config = SettingsConfigDict(env_file="", env_file_encoding='utf-8', extra="ignore")
    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
        extra = "ignore"
    
def get_settings(env_file_path) -> Settings:
    # return Settings.model_config(env_file = env_file_path)
    return Settings(_env_file=env_file_path)

# settings = get_settings()