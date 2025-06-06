from src.articles.schemas import ArticleSchema
from src.articles.models import ArticleCreate, ArticleUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Select
from fastapi import Depends, HTTPException

async def get_list_articles(Session: AsyncSession, limit=5, page_id=1):
    query = Select(ArticleSchema).offset((page_id - 1) * limit).limit(limit)

    results = await Session.execute(query)
    articles = results.scalars().all()

    return articles


async def add_article_db(
    Session: AsyncSession, article_data: ArticleCreate
) -> ArticleSchema:
    article = ArticleSchema(
        title=article_data.title,
        author=article_data.author,
        content=article_data.content,
        secret_info=article_data.secret_info,
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

async def update_article_db(Session: AsyncSession, article_id: int, new_article_data: ArticleUpdate):
    article_db = await Session.get(ArticleSchema, article_id)

    if not article_db:
        raise HTTPException(status_code=404, detail="Article not found")

    article_data = new_article_data.model_dump(exclude_unset=True, exclude_none=True).items()

    for key, value in article_data:
        setattr(article_db, key, value)

    await Session.flush()
    await Session.commit()

    return article_db
