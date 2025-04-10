from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_URL: str = "https://api.dify.ai/v1"
    APP_KEY: str = ""


settings = Settings()
