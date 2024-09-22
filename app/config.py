from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    api_id: str = Field(...)
    api_hash: str = Field(...)
    user_password: str | None = Field(None)
    user_phone: str = Field(...)

    class Config:
        env_file = ".env"


settings = Settings()
