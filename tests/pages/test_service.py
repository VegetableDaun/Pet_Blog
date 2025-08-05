from itertools import count

import pytest
from httpx import AsyncClient, Cookies
from typing import List, Dict, Tuple

from src.articles.schemas import ArticleSchema
from src.users.schemas import UserSchema
from sqlalchemy import Delete, True_
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.usefixtures("prepare_db", "async_client")
class TestPages:
    @pytest.fixture(scope="class")
    async def token(self, async_client: AsyncClient) -> Cookies:
        response = await async_client.post(
            url="/signup",
            json={"username": "test", "email": "test@test.com", "password": "test"},
        )

        return response.cookies

    async def test_register_page(self, async_client: AsyncClient):
        response = await async_client.get("/register")

        assert response.status_code == 200
        assert "Sign Up" in response.text

    async def test_login_page(self, async_client: AsyncClient):
        response = await async_client.get("/login")
        assert response.status_code == 200
        assert "Log In" in response.text

    async def test_post_page_unauthorized(self, async_client: AsyncClient):
        response = await async_client.get("/post")

        assert (
            response.status_code == 401
        )  # Assuming your auth middleware blocks unauthenticated access

    async def test_post_page_authorized(
        self, async_client: AsyncClient, token: Cookies
    ):
        # simulate authorized user by mocking the dependency or providing token

        access_token_cookie = token.get("access_token_cookie")
        csrf_access_token = token.get("csrf_access_token")

        async_client.cookies.set("access_token_cookie", access_token_cookie)
        async_client.cookies.set("csrf_access_token", csrf_access_token)

        response = await async_client.get(
            "/post", headers={"X-CSRF-TOKEN": csrf_access_token}
        )

        assert response.status_code == 200
        assert "Create a New Post" in response.text


@pytest.mark.usefixtures("prepare_db", "async_client", "test_session")
class TestBlogPage:
    # TODO Add test with two users
    @pytest.fixture(scope="class")
    def articles_data(self) -> List[Dict]:
        articles = [
            {
                "title": "Alice Adventures",
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
            {
                "title": "Chery Smile",
                "content": "Reflections on cryptic grins and strange advice.",
                "secret_info": None,
            },
            {
                "title": "Queen Court",
                "content": "Dealing with unreasonable authority figures.",
                "secret_info": "Undercover journal entry",
            },
            {
                "title": "Through the Looking Glass",
                "content": "Seeing the world from a reversed perspective.",
                "secret_info": None,
            },
        ]

        return articles

    @pytest.fixture(scope="class")
    def user_data(self) -> Dict[str, str]:
        return {
            "username": "alice",
            "email": "alice@example.com",
            "password": "alicePwd2024",
        }

    @pytest.fixture(scope="class")
    async def token(
        self, async_client: AsyncClient, user_data: Dict[str, str]
    ) -> Cookies:
        response = await async_client.post(
            url="/signup",
            json=user_data,
        )

        return response.cookies

    async def test_post_articles(
        self, articles_data, async_client: AsyncClient, token: Cookies
    ):
        access_token_cookie = token.get("access_token_cookie")
        csrf_access_token = token.get("csrf_access_token")

        async_client.cookies.set("access_token_cookie", access_token_cookie)
        async_client.cookies.set("csrf_access_token", csrf_access_token)

        for article_data in articles_data:
            await async_client.post(
                "/article",
                json=article_data,
                headers={"X-CSRF-TOKEN": csrf_access_token},
            )

    async def test_get_user_articles(
        self, articles_data, async_client: AsyncClient, token: Cookies, user_data
    ):
        access_token_cookie = token.get("access_token_cookie")
        csrf_access_token = token.get("csrf_access_token")

        async_client.cookies.set("access_token_cookie", access_token_cookie)
        async_client.cookies.set("csrf_access_token", csrf_access_token)

        response = await async_client.get(
            url=f"/{user_data['username']}/page/{1}",
            headers={"X-CSRF-TOKEN": csrf_access_token},
        )

        assert response.status_code == 200
        assert (
            response.text.count('<div class="article">') <= 5
            if len(articles_data) >= 5
            else len(articles_data)
        )

        # Ensure that titles of first 5 articles are present in the HTML
        for article in articles_data[-5:]:
            assert article["title"] in response.text

    async def test_get_user_articles_page_2(
        self,
        user_data: Dict[str, str],
        articles_data: List[Dict],
        async_client: AsyncClient,
        token: Cookies,
    ):
        access_token_cookie = token.get("access_token_cookie")
        csrf_access_token = token.get("csrf_access_token")

        async_client.cookies.set("access_token_cookie", access_token_cookie)
        async_client.cookies.set("csrf_access_token", csrf_access_token)

        total_articles = len(articles_data)
        if total_articles <= 5:
            pytest.skip("Not enough articles for page 2")

        response = await async_client.get(
            url=f"/{user_data['username']}/page/2",
            headers={"X-CSRF-TOKEN": csrf_access_token},
        )

        assert response.status_code == 200
        assert response.text.count('<div class="article">') == total_articles - 5

        for article in articles_data[: total_articles - 5]:
            assert article["title"] in response.text

    async def test_get_user_articles_page_not_found(
        self, user_data: Dict[str, str], async_client: AsyncClient, token
    ):
        access_token_cookie = token.get("access_token_cookie")
        csrf_access_token = token.get("csrf_access_token")

        async_client.cookies.set("access_token_cookie", access_token_cookie)
        async_client.cookies.set("csrf_access_token", csrf_access_token)

        response = await async_client.get(
            url=f"/{user_data['username']}/page/{9999}",
            headers={"X-CSRF-TOKEN": csrf_access_token},
        )

        assert response.status_code == 404

    async def test_empty_db(self, test_session: AsyncSession):
        query = Delete(ArticleSchema).where(ArticleSchema.id >= 0)
        await test_session.execute(query)

        query = Delete(UserSchema).where(UserSchema.id >= 0)
        await test_session.execute(query)

        await test_session.commit()
