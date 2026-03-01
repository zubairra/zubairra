from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Multi-Broker Trading Journal"
    database_url: str = "sqlite:///./trading_journal.db"
    jwt_secret: str = "change-me"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 720


settings = Settings()
