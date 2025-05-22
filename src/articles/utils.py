from src.articles.models import ArticleSchema
from src.articles.schemas import ArticleModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Select


async def get_list_articles(Session: AsyncSession, limit=10):
    query = Select(ArticleSchema).limit(limit)

    results = await Session.execute(query)
    articles = results.scalars().all()

    return articles


async def add_article_db(Session: AsyncSession, article_data: ArticleModel) -> ArticleSchema:
    article = ArticleSchema(
        title=article_data.title,
        author=article_data.author,
        content=article_data.content,
    )

    Session.add(article)

    await Session.flush()
    await Session.commit()

    return article
