from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "sqlite:///./app/database/database.db"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
