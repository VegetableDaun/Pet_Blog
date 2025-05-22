from typing import Annotated, Generator
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from src.database import session_maker


async def get_session():
    async with session_maker() as Session:
        yield Session


SessionDep = Annotated[AsyncSession, Depends(get_session)]
