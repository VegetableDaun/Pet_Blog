from fastapi import APIRouter

from src.dependencies import SessionDep
from src.users.utils import add_user_db, check_user_db
from src.users.models import UserCreate, UserPublic, UserLogin
from src.users.schemas import UserSchema

router = APIRouter(
    tags=["Users 👤"],
)


@router.post("/signup", response_model=UserPublic)
async def sign_up(user_data: UserCreate, Session: SessionDep) -> UserSchema:
    try:
        user = await add_user_db(user_data=user_data, Session=Session)

        return user
    except Exception as e:
        raise e


@router.post("/signin", response_model=UserPublic)
async def sign_in(user_data: UserLogin, Session: SessionDep) -> UserSchema:
    try:
        user = await check_user_db(user_data=user_data, Session=Session)

        return user
    except Exception as e:
        raise e
