import pytest
from httpx import AsyncClient, HTTPStatusError, Cookies

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Delete
from tests.conftest import async_client


from src.articles.schemas import ArticleSchema
from src.users.schemas import UserSchema


@pytest.mark.usefixtures("prepare_db", "async_client", "test_session")
class TestArticleRoutes:
    @pytest.fixture
    def article_data(self) -> dict:
        return {
            "title": "Sample Title",
            "content": "Full article text goes here.",
        }

    @pytest.fixture
    def new_article_data(self) -> dict:
        return {
            "title": "Updated Title",
            "content": "Updated article text goes here.",
        }

    @pytest.fixture(scope="class")
    async def token(self, async_client: AsyncClient) -> Cookies:
        response = await async_client.post(
            url="/signup",
            json={"username": "test", "email": "test@test.com", "password": "test"},
        )

        return response.cookies

    async def test_add_article(
        self,
        async_client: AsyncClient,
        article_data: dict,
        token: Cookies,
    ):
        access_token_cookie = token.get("access_token_cookie")
        csrf_access_token = token.get("csrf_access_token")

        async_client.cookies.set("access_token_cookie", access_token_cookie)
        async_client.cookies.set("csrf_access_token", csrf_access_token)

        response = await async_client.post(
            "/article",
            json=article_data,
            headers={"X-CSRF-TOKEN": csrf_access_token},
        )

        assert response.status_code == 200

        json_data = response.json()

        assert json_data["title"] == article_data["title"]
        assert json_data["content"] == article_data["content"]

    async def test_update_article(
        self,
        async_client: AsyncClient,
        token: Cookies,
        new_article_data: dict,
    ):
        # First, create an article
        access_token_cookie = token.get("access_token_cookie")
        csrf_access_token = token.get("csrf_access_token")

        async_client.cookies.set("access_token_cookie", access_token_cookie)
        async_client.cookies.set("csrf_access_token", csrf_access_token)

        # Update it
        response = await async_client.patch(
            f"/article?article_id=1",
            json=new_article_data,
            headers={"X-CSRF-TOKEN": csrf_access_token},
        )

        assert response.status_code == 200
        updated = response.json()

        assert updated["title"] == new_article_data["title"]
        assert updated["content"] == new_article_data["content"]

    async def test_delete_article(self, async_client: AsyncClient, token: Cookies):
        # First, create an article
        access_token_cookie = token.get("access_token_cookie")
        csrf_access_token = token.get("csrf_access_token")

        async_client.cookies.set("access_token_cookie", access_token_cookie)
        async_client.cookies.set("csrf_access_token", csrf_access_token)

        # Then, delete it
        response = await async_client.delete(
            f"/article?article_id=1",
            headers={"X-CSRF-TOKEN": csrf_access_token},
        )
        assert response.status_code == 200
        assert response.json() == {"ok": True}

    async def test_update_article_invalid_id(
        self, async_client: AsyncClient, new_article_data: dict, token: Cookies
    ):

        with pytest.raises(HTTPStatusError) as ex:
            access_token_cookie = token.get("access_token_cookie")
            csrf_access_token = token.get("csrf_access_token")

            async_client.cookies.set("access_token_cookie", access_token_cookie)
            async_client.cookies.set("csrf_access_token", csrf_access_token)

            response = await async_client.patch(
                "/article?article_id=999999",
                json=new_article_data,
                headers={"X-CSRF-TOKEN": csrf_access_token},
            )

            response.raise_for_status()

        assert response.status_code == 404

    async def test_delete_article_invalid_id(
        self, async_client: AsyncClient, token: Cookies
    ):
        with pytest.raises(HTTPStatusError) as ex:
            access_token_cookie = token.get("access_token_cookie")
            csrf_access_token = token.get("csrf_access_token")

            async_client.cookies.set("access_token_cookie", access_token_cookie)
            async_client.cookies.set("csrf_access_token", csrf_access_token)

            response = await async_client.delete(
                "/article?article_id=999999",
                headers={"X-CSRF-TOKEN": csrf_access_token},
            )

            response.raise_for_status()

        assert response.status_code == 404

    async def test_add_article_unauthorized(
        self, article_data: dict, async_client: AsyncClient
    ):
        # Simulate unauthenticated client
        with pytest.raises(HTTPStatusError) as ex:
            response = await async_client.post("/article", json=article_data)

            response.raise_for_status()

        assert response.status_code == 401

    async def test_update_article_unauthorized(
        self, new_article_data: dict, async_client: AsyncClient
    ):
        # Simulate unauthenticated client
        with pytest.raises(HTTPStatusError) as ex:
            response = await async_client.patch(
                "/article?article_id=1", json=new_article_data
            )

            response.raise_for_status()

        assert response.status_code == 401

    async def test_delete_article_unauthorized(
        self, article_data: dict, async_client: AsyncClient
    ):
        # Simulate unauthenticated client
        with pytest.raises(HTTPStatusError) as ex:
            response = await async_client.delete("/article?article_id=1")

            response.raise_for_status()

        assert response.status_code == 401

    async def test_empty_db(self, test_session: AsyncSession):
        query = Delete(ArticleSchema).where(ArticleSchema.id >= 0)
        await test_session.execute(query)

        query = Delete(UserSchema).where(UserSchema.id >= 0)
        await test_session.execute(query)

        await test_session.commit()
