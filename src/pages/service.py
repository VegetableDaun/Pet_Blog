from fastapi import APIRouter, Request
from fastapi import Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from authx import RequestToken
from math import ceil

from src.dependencies import SessionDep
from src.articles.utils import (
    get_user_articles_db,
    count_user_articles_db,
)
from auth.security import security
from src.pages.templates import templates

router = APIRouter(
    tags=["Blog 🌐"],
)


@router.get("/register", response_class=HTMLResponse)
async def get_sign_up_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="register.html",
    )


@router.get("/login", response_class=HTMLResponse)
async def get_sign_in_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html",
    )


@router.get(
    "/post",
    response_class=HTMLResponse,
    dependencies=[Depends(security.access_token_required)],
)
async def get_post_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="create_post.html",
    )


@router.get(
    "/{user_id}/page/{page_id}",
    response_class=HTMLResponse,
    dependencies=[Depends(security.access_token_required)],
)
async def get_user_articles(
    request: Request,
    Session: SessionDep,
    user_id: int,
    page_id: int = 1,
    limit: int = 3,
):

    articles_count = await count_user_articles_db(Session=Session, user_id=user_id)
    total_pages = ceil(articles_count / limit)

    articles = await get_user_articles_db(Session, page_id=page_id, limit=limit)

    return templates.TemplateResponse(
        request=request,
        name="blog.html",
        context={"articles": articles, "total_pages": total_pages, "page": page_id},
    )


@router.get(
    "/page/{page_id}",
    response_class=HTMLResponse,
    dependencies=[Depends(security.access_token_required)],
)
async def get_articles(
    request: Request,
    Session: SessionDep,
    page_id: int = 1,
    limit: int = 3,
):

    articles_count = await count_user_articles_db(Session=Session)
    total_pages = ceil(articles_count / limit)

    articles = await get_user_articles_db(Session, page_id=page_id, limit=limit)

    return templates.TemplateResponse(
        request=request,
        name="blog.html",
        context={"articles": articles, "total_pages": total_pages, "page": page_id},
    )
