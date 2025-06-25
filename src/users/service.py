from fastapi import APIRouter, Response, Request
from fastapi.responses import RedirectResponse

from src.dependencies import SessionDep
from src.users.utils import add_user_db, authenticate_user
from src.users.models import UserCreate, UserLogin, UserPublic
from src.users.schemas import UserSchema
from src.auth.security import security

router = APIRouter(
    tags=["Users 👤"],
)


@router.post("/signup", response_class=RedirectResponse)
async def sign_up(user_data: UserCreate, Session: SessionDep, request: Request):
    try:
        user = await add_user_db(user_data=user_data, Session=Session)
        token = security.create_access_token(uid=str(user.id))

        redirect = RedirectResponse(
            url=request.url_for("get_articles", page_id=1), status_code=301
        )

        security.set_access_cookies(response=redirect, token=token, max_age=300)

        return redirect

    except Exception as e:
        raise e


@router.post("/signin", response_class=RedirectResponse)
async def sign_in(user_data: UserLogin, Session: SessionDep, request: Request):
    try:
        user = await authenticate_user(user_data=user_data, Session=Session)
        token = security.create_access_token(uid=str(user.id))

        redirect = RedirectResponse(
            url=request.url_for("get_articles", page_id=1), status_code=301
        )

        security.set_access_cookies(response=redirect, token=token, max_age=300)

        return redirect

    except Exception as e:
        raise e
