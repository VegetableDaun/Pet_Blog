from sqlalchemy.ext.asyncio import AsyncSession
from src.users.schemas import UserSchema
from src.users.models import UserCreate


async def add_user_db(Session: AsyncSession, user_data: UserCreate):
    user_db = UserSchema(
        username=user_data.username,
        email=user_data.email,
        password=user_data.password,
    )

    Session.add(user_db)

    await Session.flush()
    await Session.commit()

    return user_db
