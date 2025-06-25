from fastapi import APIRouter, Response, Depends, HTTPException

from src.dependencies import SessionDep
from src.users.utils import add_user_db, authenticate_user
from src.users.models import UserCreate, UserLogin, UserPublic
from src.users.schemas import UserSchema
from src.auth.security import security

router = APIRouter(
    tags=["Users 👤"],
)


@router.post(
    "/signup",
    response_model=UserPublic,
)
async def sign_up(
    user_data: UserCreate, Session: SessionDep, response: Response
) -> UserSchema:
    try:
        user = await add_user_db(user_data=user_data, Session=Session)
        token = security.create_access_token(uid=str(user.id))
        security.set_access_cookies(
            response=response,
            token=token,
        )
        # response.set_cookie(key=security.config.JWT_ACCESS_COOKIE_NAME, value=token)

        return user

    except Exception as e:
        raise e


@router.post(
    "/signin",
    response_model=UserPublic,
)
async def sign_in(
    user_data: UserLogin, Session: SessionDep, response: Response
) -> UserSchema:
    try:
        user = await authenticate_user(user_data=user_data, Session=Session)

        token = security.create_access_token(uid=str(user.id))
        security.set_access_cookies(
            response=response,
            token=token,
        )
        # response.set_cookie(key=security.config.JWT_ACCESS_COOKIE_NAME, value=token)

        return user

    except Exception as e:
        raise e
