from fastapi import APIRouter, Request, Response
from fastapi.responses import HTMLResponse
from typing import List, Dict, Union

from src.articles.schemas import ArticleModel
from src.dependencies import SessionDep
from src.articles.utils import get_list_articles, add_article_db
from fastapi.templating import Jinja2Templates

router = APIRouter()

# router.mount()
templates = Jinja2Templates(directory="templates")


@router.get("/blog", response_class=HTMLResponse)
async def get_articles(request: Request, Session: SessionDep):
    articles = await get_list_articles(Session)

    # return articles

    return templates.TemplateResponse(
        request=request, name="blog.html", context={"articles": articles}
    )


@router.post("/blog")
async def add_article(
    Session: SessionDep, article_data: ArticleModel
) -> Dict[str, bool]:
    try:
        article = await add_article_db(Session, article_data)

        return {
            "success": True,
        }
    except Exception as e:
        raise e
