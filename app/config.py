from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    api_id: str = Field(...)
    api_hash: str = Field(...)
    user_password: str | None = Field(None)
    user_phone: str = Field(...)
    database_url: str = Field("sqlite+aiosqlite:///./tg_counter.db")

    class Config:
        env_file = ".env"
        extra = "allow"


settings = Settings()
