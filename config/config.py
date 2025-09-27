from pydantic import BaseSettings
class Settings(BaseSettings):
    openai_api_key: str
    db_url: str = 'sqlite:///./data/app.db'
    persistence_driver: str = 'sqlite'
    json_store: str = './data/store.json'
    host: str = '127.0.0.1'
    port: int = 8000
    class Config:
        env_file = '.env'
settings = Settings()