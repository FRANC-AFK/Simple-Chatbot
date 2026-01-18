import os
from dataclasses import dataclass

@dataclass
class Config:
    """Application configuration from environment variables."""
    
    # Flask
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", 5000))
    
    # AI
    HF_API_TOKEN: str = os.getenv("HF_API_TOKEN", "")
    USE_AI: bool = os.getenv("USE_AI", "True").lower() == "true"
    AI_MAX_TOKENS: int = int(os.getenv("AI_MAX_TOKENS", 64))
    AI_TIMEOUT: int = int(os.getenv("AI_TIMEOUT", 60))
    
    # Cache
    ENABLE_CACHE: bool = os.getenv("ENABLE_CACHE", "True").lower() == "true"
    CACHE_TTL: int = int(os.getenv("CACHE_TTL", 3600))
    CACHE_MAX_SIZE: int = int(os.getenv("CACHE_MAX_SIZE", 100))
    
    # Rate Limiting
    RATE_LIMIT_MAX_REQUESTS: int = int(os.getenv("RATE_LIMIT_MAX_REQUESTS", 10))
    RATE_LIMIT_WINDOW_SECONDS: int = int(os.getenv("RATE_LIMIT_WINDOW_SECONDS", 60))

config = Config()
