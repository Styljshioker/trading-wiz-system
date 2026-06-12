from pydantic_settings import BaseSettings
from typing import List, Optional
import os
from functools import lru_cache

class Settings(BaseSettings):
    # App Configuration
    app_name: str = "Trading Wiz System"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # API Configuration
    api_prefix: str = "/api/v1"
    secret_key: str = "your-secret-key-change-this"
    access_token_expire_minutes: int = 60 * 24 * 7  # 7 days
    algorithm: str = "HS256"
    
    # Database
    database_url: str = "sqlite:///./trading_wiz.db"
    
    # Trading APIs
    alpaca_api_key: Optional[str] = None
    alpaca_secret_key: Optional[str] = None
    alpaca_base_url: str = "https://paper-api.alpaca.markets"  # Paper trading by default
    
    # Market Data APIs  
    alpha_vantage_api_key: Optional[str] = None
    yahoo_finance_enabled: bool = True
    
    # AI/ML APIs
    openai_api_key: Optional[str] = None
    huggingface_token: Optional[str] = None
    
    # External APIs
    news_api_key: Optional[str] = None
    twitter_bearer_token: Optional[str] = None
    
    # Redis (for caching and real-time data)
    redis_url: str = "redis://localhost:6379"
    
    # CORS
    backend_cors_origins: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001", 
        "http://localhost:8080",
        "https://localhost:3000",
    ]
    
    class Config:
        env_file = ".env"
        case_sensitive = False

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
