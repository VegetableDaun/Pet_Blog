import pytest
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Select, func, Delete
from sqlalchemy.exc import DataError, IntegrityError, DBAPIError

from src.articles.schemas import ArticleSchema
from src.users.models import UserCreate
from src.users.utils import add_user_db
from src.users.schemas import UserSchema


@pytest.mark.usefixtures("prepare_db", "test_session")
class TestArticleSchema:

    @pytest.fixture(scope="class")
    async def test_user(
        self,
        test_session: AsyncSession,
    ):
        # Create user to assign articles to
        user = await add_user_db(
            Session=test_session,
            user_data=UserCreate(
                username="test",
                email="test@test.com",
                password="pass1234",
            ),
        )

        return user

    @pytest.mark.parametrize(
        "title, content, secret_info",
        [
            ("First Post", "This is the first article content", "secret1"),
            ("Second", "Another article goes here", None),
            ("Tips", "How to write better code.", "hidden tip"),
            ("Release Notes", "Version 1.0 released!", "internal"),
            ("Story", "Once upon a time...", None),
        ],
    )
    async def test_add_articles(
        self,
        test_session: AsyncSession,
        test_user: UserSchema,
        title: str,
        content: str,
        secret_info: str | None,
    ):

        article = ArticleSchema(
            title=title,
            content=content,
            secret_info=secret_info,
            user_id=test_user.id,
        )

        test_session.add(article)

        await test_session.commit()

        assert article.id is not None
        assert article.release_date is not None
        assert article.title == title
        assert article.content == content
        assert article.secret_info == secret_info

    async def test_get_articles(self, test_session: AsyncSession):
        query = Select(func.count(ArticleSchema.id))
        results = await test_session.execute(query)

        count = results.scalar()

        assert count == 5  # match with number of successful inserts above

    async def test_delete_articles(self, test_session: AsyncSession):
        query = Delete(ArticleSchema).where(ArticleSchema.id >= 0)

        await test_session.execute(query)
        await test_session.commit()

        # Check if articles were removed
        result = await test_session.execute(Select(func.count(ArticleSchema.id)))
        count = result.scalar()

        assert count == 0

    async def test_too_long_title(
        self, test_session: AsyncSession, test_user: UserSchema
    ):
        await test_session.refresh(test_user)

        article = ArticleSchema(
            title="x" * 81,
            content="Valid content",
            secret_info="Valid secret info",
            user_id=test_user.id,
        )

        with pytest.raises(DBAPIError) as ex_pytest:
            test_session.add(article)

            try:
                await test_session.commit()
            except DBAPIError as ex_db:
                await test_session.rollback()

                raise

    async def test_too_long_content(
        self, test_session: AsyncSession, test_user: UserSchema
    ):
        await test_session.refresh(test_user)

        article = ArticleSchema(
            title="Valid Title",
            content="x" * 281,
            secret_info="Valid secret info",
            user_id=test_user.id,
        )

        with pytest.raises(DBAPIError) as ex_pytest:
            test_session.add(article)

            try:
                await test_session.commit()
            except DBAPIError as ex_db:
                await test_session.rollback()

                raise

    async def test_too_long_secret_info(
        self, test_session: AsyncSession, test_user: UserSchema
    ):
        await test_session.refresh(test_user)

        article = ArticleSchema(
            title="Valid Title",
            content="Valid content",
            secret_info="x" * 81,
            user_id=test_user.id,
        )

        with pytest.raises(DBAPIError) as ex_pytest:
            test_session.add(article)

            try:
                await test_session.commit()
            except DBAPIError as ex_db:
                await test_session.rollback()

                raise

    async def test_nullable_secret_info(
        self, test_session: AsyncSession, test_user: UserSchema
    ):
        await test_session.refresh(test_user)

        article = ArticleSchema(
            title="Test Article",
            content="Some content",
            secret_info=None,
            user_id=test_user.id,
        )

        test_session.add(article)
        await test_session.commit()

        assert article.id is not None
        assert article.release_date is not None
        assert article.title == "Test Article"
        assert article.content == "Some content"
        assert article.secret_info == None

        await test_session.delete(article)
        await test_session.commit()

    async def test_empty_db(self, test_session: AsyncSession, test_user: UserSchema):
        await test_session.delete(test_user)

        await test_session.flush()
