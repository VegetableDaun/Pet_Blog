from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from sqlalchemy import Select

from src.users.schemas import UserSchema
from src.users.models import UserCreate, UserLogin
from src.auth.utils import get_password_hash, verify_password


async def add_user_db(Session: AsyncSession, user_data: UserCreate) -> UserSchema:
    user_db = UserSchema(
        username=user_data.username,
        email=user_data.email,
        password=get_password_hash(user_data.password),
    )

    Session.add(user_db)

    await Session.flush()
    await Session.commit()

    return user_db


async def authenticate_user(Session: AsyncSession, user_data: UserLogin) -> UserSchema:
    if user_data.username is not None:
        query = Select(UserSchema).where(UserSchema.username == user_data.username)
    else:
        query = Select(UserSchema).where(UserSchema.email == user_data.email)

    results = await Session.execute(query)
    user = results.scalar()

    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    elif not verify_password(
        plain_password=user_data.password, hashed_password=user.password
    ):
        raise HTTPException(status_code=401, detail="User not authorized")
    else:
        return user
