from src.articles.schemas import ArticleSchema
from src.articles.models import ArticleCreate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Select


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
