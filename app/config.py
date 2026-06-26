"""应用配置管理"""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """应用配置"""
    # 基础配置
    app_name: str = "HouseKeep-AI"
    debug: bool = True
    host: str = "0.0.0.0"
    port: int = 8000

    # 数据库
    database_url: str = "postgresql://housekeep:housekeep123@localhost:5432/housekeep_ai"

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # AI API
    openai_api_key: str = ""
    openai_model: str = "gpt-4"
    claude_api_key: str = ""
    claude_model: str = "claude-3-opus-20240229"

    # JWT
    secret_key: str = "change-me"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 10080

    # Elasticsearch
    es_host: str = "http://localhost:9200"

    # 业务配置
    default_lead_price: float = 80.0

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
