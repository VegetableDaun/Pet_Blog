import pytest
from httpx import AsyncClient, Cookies


@pytest.mark.usefixtures("prepare_db", "async_client")
class TestExceptions:

    @pytest.fixture(scope="class")
    async def token(self, async_client: AsyncClient) -> Cookies:
        response = await async_client.post(
            url="/signup",
            json={"username": "test", "email": "test@test.com", "password": "test"},
        )

        return response.cookies

    @pytest.mark.asyncio
    async def test_unauthorized_handler(self, async_client: AsyncClient):
        response = await async_client.get("/page/1")

        assert response.status_code == 401
        assert "Oops! You are not authorized to view this page." in response.text

    # @pytest.mark.asyncio
    # async def test_forbidden_handler(test_app):
    #     async with AsyncClient(app=test_app, base_url="http://test") as ac:
    #         response = await ac.get("/forbidden")
    #     assert response.status_code == 403
    #     assert "403" in response.text

    @pytest.mark.asyncio
    async def test_not_found_handler(self, async_client: AsyncClient, token: Cookies):
        access_token_cookie = token.get("access_token_cookie")
        csrf_access_token = token.get("csrf_access_token")

        async_client.cookies.set("access_token_cookie", access_token_cookie)
        async_client.cookies.set("csrf_access_token", csrf_access_token)

        response = await async_client.get(
            url="/notfound",
            headers={"X-CSRF-TOKEN": csrf_access_token},
        )

        assert response.status_code == 404
        assert "Oops! The page you're looking for doesn't exist." in response.text
