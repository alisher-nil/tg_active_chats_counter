from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from 
from app.models import Users



class CRUDUsers:
    async def get_user_by_telegram_id(id: int, session: AsyncSession):
        stmt = select(Users).where(Users.telegram_id == id)
        user_query = await session.execute(stmt)
        user = user_query.scalars().first()
        return user

    async def create(user_data, session: AsyncSession):

        user = Users()
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user
