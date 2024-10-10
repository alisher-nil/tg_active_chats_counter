from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.constants import (
    TG_FIRST_NAME_MAX_LENGTH,
    TG_LAST_NAME_MAX_LENGTH,
    TG_USERNAME_MAX_LENGTH,
)
from app.models import Users


class UserDataSchema(BaseModel):
    telegram_id: int = Field(..., alias="id")
    first_name: str | None = Field(None, max_length=TG_FIRST_NAME_MAX_LENGTH)
    last_name: str | None = Field(None, max_length=TG_LAST_NAME_MAX_LENGTH)
    username: str | None = Field(None, max_length=TG_USERNAME_MAX_LENGTH)


class CRUDUsers:
    async def get_user_by_telegram_id(id: int, session: AsyncSession):
        stmt = select(Users).where(Users.telegram_id == id)
        user_query = await session.execute(stmt)
        user = user_query.scalars().first()
        return user

    async def create(user_data, session: AsyncSession):
        user_data = UserDataSchema(**user_data)
        user = Users(**user_data.model_dump())
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user
