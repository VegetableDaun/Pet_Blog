import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from sqlalchemy.sql.functions import user

from src.articles.schemas import ArticleSchema
from tests.conftest import test_session
from src.articles.models import ArticleCreate, ArticleUpdate
from src.articles.utils import (
    get_user_articles_db,
    add_article_db,
    delete_article_db,
    update_article_db,
    count_user_articles_db,
)
from src.users.utils import add_user_db
from src.users.models import UserCreate
from src.users.schemas import UserSchema

from sqlalchemy import Delete
from typing import List, Dict, Tuple


@pytest.mark.usefixtures("prepare_db", "test_session")
class TestArticleDB:
    count_articles_db = 0

    @pytest.fixture(
        # username: str, email: str, password: str, articles: List[Dict]
        params=[
            (
                "alice",
                "alice@example.com",
                "alicePwd2024",
                [
                    {
                        "title": "Alice's Adventures",
                        "content": "An article about Alice's journey.",
                        "secret_info": None,
                    },
                    {
                        "title": "Tea Time",
                        "content": "Thoughts on tea and wonderland.",
                        "secret_info": "Secret location",
                    },
                    {
                        "title": "Rabbit Hole",
                        "content": "What happens when you follow the white rabbit?",
                        "secret_info": None,
                    },
                ],
            ),
            (
                "bob_smith",
                "bob.smith@example.org",
                "bobSecure!",
                [
                    {
                        "title": "Bob's Blog",
                        "content": "First post on Bob's personal blog.",
                        "secret_info": None,
                    },
                    {
                        "title": "Coding Tips",
                        "content": "Best practices for writing clean code.",
                        "secret_info": None,
                    },
                    {
                        "title": "Secret Debugging Tricks",
                        "content": "Little-known Python debugging methods.",
                        "secret_info": "Private cheatsheet",
                    },
                ],
            ),
        ],
    )
    def test_data(self, request):
        username: str
        email: str
        password: str
        articles: List[Dict]

        username, email, password, articles = request.param

        return username, email, password, articles

    async def test_add_user_and_articles(
        self, test_session: AsyncSession, test_data: Tuple
    ):
        username: str
        email: str
        password: str
        articles: List[Dict[str, str]]

        username, email, password, articles = test_data

        user = await add_user_db(
            user_data=UserCreate(
                username=username,
                email=email,
                password=password,
            ),
            Session=test_session,
        )

        for article in articles:
            article_db = await add_article_db(
                Session=test_session,
                article_data=ArticleCreate(**article),
                user_id=user.id,
            )

            assert article_db is not None
            assert article_db.id is not None
            assert article_db.user_id is not None
            assert article_db.release_date is not None
            assert article_db.title == article["title"]
            assert article_db.content == article["content"]
            assert article_db.secret_info is article["secret_info"]

    async def test_get_articles_by_username(
        self, test_session: AsyncSession, test_data: Tuple
    ):
        username: str
        email: str
        password: str
        articles: List[Dict[str, str]]

        username, email, password, articles = test_data

        result = await get_user_articles_db(Session=test_session, username=username)

        assert isinstance(result, list)
        assert len(result) == len(articles)

    @pytest.mark.parametrize(
        "limit, page_id, expected",
        [(5, 1, 5), (6, 1, 6), (7, 1, 6), (5, 2, 1)],
    )
    async def test_get_articles_no_username(
        self, test_session: AsyncSession, limit: int, page_id: int, expected: int
    ):
        result = await get_user_articles_db(
            Session=test_session, limit=limit, page_id=page_id
        )

        assert isinstance(result, list)
        assert len(result) == expected

    async def test_count_user_articles_db_by_username(
        self, test_session: AsyncSession, test_data: Tuple
    ):
        username: str
        email: str
        password: str
        articles: List[Dict[str, str]]

        username, email, password, articles = test_data

        count_article = await count_user_articles_db(
            Session=test_session, username=username
        )

        assert isinstance(count_article, int)
        assert count_article == len(articles)

    async def test_count_user_articles_db_all(self, test_session: AsyncSession):
        count_article = await count_user_articles_db(Session=test_session)

        assert isinstance(count_article, int)
        assert count_article == 6

    async def test_update_article(self, test_session: AsyncSession):

        all_articles = await get_user_articles_db(Session=test_session)
        article_to_update = all_articles[0]

        update_data = ArticleUpdate(title="Updated Title", content="Updated content")
        updated = await update_article_db(
            Session=test_session,
            article_id=article_to_update.id,
            new_article_data=update_data,
        )

        assert updated.title == "Updated Title"
        assert updated.content == "Updated content"

    async def test_update_nonexistent_article(self, test_session: AsyncSession):
        with pytest.raises(HTTPException, match="Article not found") as exc:
            await update_article_db(
                Session=test_session,
                article_id=9999,
                new_article_data=ArticleUpdate(title="Doesn't exist"),
            )

        assert exc.value.status_code == 404

    async def test_delete_article(self, test_session: AsyncSession):
        all_articles = await get_user_articles_db(Session=test_session)
        article_to_delete = all_articles[0]

        await delete_article_db(Session=test_session, article_id=article_to_delete.id)

        remaining = await get_user_articles_db(Session=test_session)

        assert all(a.id != article_to_delete.id for a in remaining)

    async def test_delete_nonexistent_article(self, test_session: AsyncSession):
        with pytest.raises(HTTPException, match="Article not found") as exc:
            await delete_article_db(Session=test_session, article_id=9999)

        assert exc.value.status_code == 404

    async def test_delete_users(
        self,
        test_session: AsyncSession,
    ):
        query = Delete(ArticleSchema).where(ArticleSchema.id >= 0)
        await test_session.execute(query)

        query = Delete(UserSchema).where(UserSchema.id >= 0)
        await test_session.execute(query)

        await test_session.commit()

        assert True
