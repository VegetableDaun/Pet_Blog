from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Select

from src.users.schemas import UserSchema
from src.users.models import UserCreate, UserLogin


async def add_user_db(Session: AsyncSession, user_data: UserCreate) -> UserSchema:
    user_db = UserSchema(
        username=user_data.username,
        email=user_data.email,
        password=user_data.password,
    )

    Session.add(user_db)

    await Session.flush()
    await Session.commit()

    return user_db


async def check_user_db(Session: AsyncSession, user_data: UserLogin) -> UserSchema:

    if user_data.username is not None:
        query = Select(UserSchema).where(
            UserSchema.username == user_data.username,
            UserSchema.password == user_data.password,
        )
    else:
        query = Select(UserSchema).where(
            UserSchema.email == user_data.email,
            UserSchema.password == user_data.password,
        )

    result = await Session.execute(query)

    return result.scalar()
