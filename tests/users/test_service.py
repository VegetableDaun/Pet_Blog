import pytest
from httpx import AsyncClient, HTTPStatusError
from tests.conftest import async_client


@pytest.mark.usefixtures("prepare_db")
class TestUserService:
    @pytest.fixture
    async def payload(self) -> dict:
        return {"username": "test", "email": "test@test.com", "password": "test"}

    async def test_sign_up(self, async_client: AsyncClient, payload: dict):
        response = await async_client.post(
            url="/signup",
            json=payload,
        )

        assert response.has_redirect_location
        assert response.status_code == 301
        assert "/page/1" in response.headers["location"]

        assert "access_token_cookie" in response.cookies
        assert "csrf_access_token" in response.cookies

    async def test_sign_in(self, async_client: AsyncClient, payload: dict):
        response = await async_client.post(url="/signin", json=payload)

        assert response.has_redirect_location
        assert response.status_code == 301
        assert "/page/1" in response.headers["location"]

        assert "access_token_cookie" in response.cookies
        assert "csrf_access_token" in response.cookies


    async def test_sign_up_duplicates(self, async_client: AsyncClient):

        with pytest.raises(HTTPStatusError) as ex:
            response = await async_client.post(
                url="/signup",
                json={
                    "username": "test1",
                    "email": "test@test.com",
                    "password": "test1",
                },
            )

            response.raise_for_status()

        assert response.status_code == 409

    @pytest.mark.parametrize(
        "username, email, password",
        [
            ("x" * 17, "test@test.com", "test"),
            ("test", "x" * 24 + "@test.com", "test"),
            ("test", "test@test.com", "x" * 33),
            ("test", "not-email", "x" * 32),
            (None, "test@test.com", "x" * 32),
        ],
    )
    async def test_sign_up_invalid_data(
        self, async_client: AsyncClient, username: str, email: str, password: str
    ):
        with pytest.raises(HTTPStatusError) as ex:
            response = await async_client.post(
                url="/signup",
                json={"username": username, "email": email, "password": password},
            )

            response.raise_for_status()

        assert response.status_code == 422
