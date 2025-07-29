from fastapi import APIRouter, Depends
from src.auth.security import security
from authx import TokenPayload

from src.articles.models import ArticleCreate, ArticlePublic, ArticleUpdate
from src.articles.schemas import ArticleSchema
from src.dependencies import SessionDep
from src.articles.utils import (
    add_article_db,
    delete_article_db,
    update_article_db,
)

router = APIRouter(
    tags=["Articles 📰"],
)


@router.post(
    "/article",
    response_model=ArticlePublic,
)
async def add_article(
    Session: SessionDep,
    article_data: ArticleCreate,
    token: TokenPayload = Depends(security.access_token_required),
) -> ArticleSchema:
    # check_token(token=token, auth=security)

    try:

        article = await add_article_db(
            Session=Session, article_data=article_data, user_id=int(token.sub)
        )

        return article
    except Exception as e:
        raise e


@router.delete("/article", dependencies=[Depends(security.access_token_required)])
async def delete_article(Session: SessionDep, article_id: int):

    try:
        await delete_article_db(Session=Session, article_id=article_id)

        return {"ok": True}
    except Exception as e:
        raise e


@router.patch(
    "/article",
    response_model=ArticlePublic,
    dependencies=[Depends(security.access_token_required)],
)
async def update_article(
    Session: SessionDep, article_id: int, new_article_data: ArticleUpdate
):
    try:
        article_db = await update_article_db(
            Session=Session,
            article_id=article_id,
            new_article_data=new_article_data,
        )

        return article_db

    except Exception as e:
        raise e
