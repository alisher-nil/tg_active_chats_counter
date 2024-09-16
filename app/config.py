from pydantic import BaseSettings


class Settings(BaseSettings):
    api_id: str
    api_hash: str
    user_password: str | None
    user_phone: str

    class Config:
        env_file = ".env"


settings = Settings()
