from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DIFY_API_URL: str = "https://api.dify.ai/v1"
    DIFY_LOGGER_ON: bool = True


settings = Settings()
