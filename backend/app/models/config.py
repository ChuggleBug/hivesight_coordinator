
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    broker_hostname: str
    broker_port: int
    cloud_hostname: str
    cloud_port: int
    
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings() # type: ignore
