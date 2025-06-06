from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse

from src.articles.models import ArticleCreate, ArticlePublic, ArticleUpdate
from src.articles.schemas import ArticleSchema
from src.dependencies import SessionDep
from src.articles.utils import (
    get_list_articles,
    add_article_db,
    delete_article_db,
    update_article_db,
    count_article_db,
)
from fastapi.templating import Jinja2Templates
from math import ceil

router = APIRouter(
    tags=["Articles 📰"],
)

# router.mount()
templates = Jinja2Templates(directory="templates")


@router.get("/blog/page/{page_id}", response_class=HTMLResponse)
async def get_articles(
    request: Request, Session: SessionDep, page_id: int = 1, limit: int = 3
):

    articles_count = await count_article_db(Session=Session)
    total_pages = ceil(articles_count / limit)

    articles = await get_list_articles(Session, page_id=page_id, limit=limit)

    return templates.TemplateResponse(
        request=request,
        name="blog.html",
        context={"articles": articles, "total_pages": total_pages, "page": page_id},
    )


@router.post("/article", response_model=ArticlePublic)
async def add_article(
    Session: SessionDep, article_data: ArticleCreate
) -> ArticleSchema:
    try:
        article = await add_article_db(Session, article_data)

        return article
    except Exception as e:
        raise e


@router.delete("/article")
async def delete_article(Session: SessionDep, article_id: int):

    try:
        await delete_article_db(Session=Session, article_id=article_id)

        return {"ok": True}
    except Exception as e:
        raise e


@router.patch("/article")
async def update_article(
    Session: SessionDep, article_id: int, new_article_data: ArticleUpdate
):
    try:
        article_db = await update_article_db(
            Session=Session, article_id=article_id, new_article_data=new_article_data
        )

        return article_db

    except Exception as e:
        raise e
