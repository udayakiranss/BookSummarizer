from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    openai_api_key: Optional[str] = None
    db_url: str = 'sqlite:///./data/app.db'
    persistence_driver: str = 'sqlite'
    json_store: str = './data/store.json'
    host: str = '127.0.0.1'
    port: int = 8000
    
    # News API settings
    news_limit_default: int = 5
    news_limit_max: int = 10
    
    # OpenAI settings
    openai_model: str = 'gpt-3.5-turbo'
    openai_max_tokens: int = 500
    openai_temperature: float = 0.3
    
    # Development settings
    use_openai_stub: bool = False  # Set to False to use real OpenAI API
    stub_mode: bool = False # Enable stub mode for development
    
    class Config:
        env_file = '.env'

settings = Settings()