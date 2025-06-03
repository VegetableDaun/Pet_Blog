from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from src.articles.models import ArticleCreate, ArticlePublic
from src.articles.schemas import ArticleSchema
from src.dependencies import SessionDep
from src.articles.utils import get_list_articles, add_article_db
from fastapi.templating import Jinja2Templates

router = APIRouter()

# router.mount()
templates = Jinja2Templates(directory="templates")


@router.get("/blog/page/{page_id}", response_class=HTMLResponse)
async def get_articles(request: Request, Session: SessionDep, page_id: int = 1):
    articles = await get_list_articles(Session, page_id=page_id)

    return templates.TemplateResponse(
        request=request, name="blog.html", context={"articles": articles}
    )


@router.post("/blog", response_model=ArticlePublic)
async def add_article(
    Session: SessionDep, article_data: ArticleCreate
) -> ArticleSchema:
    try:
        article = await add_article_db(Session, article_data)

        return article
    except Exception as e:
        raise e
