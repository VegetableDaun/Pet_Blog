from fastapi import APIRouter
from typing import List, Dict, Union

from src.articles.schemas import ArticleModel
from src.dependencies import SessionDep
from src.articles.utils import get_list_articles, add_article_db

router = APIRouter()


@router.get('/blog')
async def get_articles(Session: SessionDep) -> List[ArticleModel]:
    articles = await get_list_articles(Session)

    return articles


@router.post('/blog')
async def add_article(Session: SessionDep, article_data: ArticleModel) -> Dict[str, bool]:
    try:
        article = await add_article_db(Session, article_data)

        return {
            'success': True,
        }
    except Exception as e:
        raise e
