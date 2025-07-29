from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Select, func, desc
from fastapi import Depends, HTTPException

from src.articles.schemas import ArticleSchema
from src.articles.models import ArticleCreate, ArticleUpdate

from src.users.schemas import UserSchema


async def get_user_articles_db(
    Session: AsyncSession, username: str | None = None, limit=5, page_id=1
):
    if username is None:
        query = (
            Select(ArticleSchema)
            .offset((page_id - 1) * limit)
            .limit(limit)
            .order_by(desc(ArticleSchema.release_date))
        )
    else:
        query = (
            Select(ArticleSchema)
            .offset((page_id - 1) * limit)
            .limit(limit)
            .where(
                ArticleSchema.user_id
                == Select(UserSchema.id)
                .where(UserSchema.username == username)
                .scalar_subquery()
            )
            .order_by(desc(ArticleSchema.release_date))
        )

    results = await Session.execute(query)
    articles = results.scalars().all()

    return articles


async def add_article_db(
    Session: AsyncSession, article_data: ArticleCreate, user_id: int
) -> ArticleSchema:
    article = ArticleSchema(
        title=article_data.title,
        content=article_data.content,
        secret_info=article_data.secret_info,
        user_id=user_id,
    )

    Session.add(article)

    await Session.flush()
    await Session.commit()

    return article


async def delete_article_db(Session: AsyncSession, article_id: int):
    article_db = await Session.get(ArticleSchema, article_id)

    if not article_db:
        raise HTTPException(status_code=404, detail="Article not found")

    await Session.delete(article_db)

    await Session.flush()
    await Session.commit()


async def update_article_db(
    Session: AsyncSession,
    article_id: int,
    new_article_data: ArticleUpdate,
):
    article_db = await Session.get(ArticleSchema, article_id)

    if not article_db:
        raise HTTPException(status_code=404, detail="Article not found")

    article_data = new_article_data.model_dump(
        exclude_unset=True, exclude_none=True
    ).items()

    for key, value in article_data:
        setattr(article_db, key, value)

    await Session.flush()
    await Session.commit()

    return article_db


async def count_user_articles_db(Session: AsyncSession, username: str | None = None):
    if username is None:
        query = Select(func.count(ArticleSchema.id))
    else:
        query = Select(func.count(ArticleSchema.id)).where(
            ArticleSchema.user_id
            == Select(UserSchema.id)
            .where(UserSchema.username == username)
            .scalar_subquery()
        )

    results = await Session.execute(query)

    return results.scalar()
