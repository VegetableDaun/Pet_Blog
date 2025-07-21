import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from tests.conftest import test_session, alembic_config
from src.users.utils import add_user_db, authenticate_user
from src.users.models import UserCreate, UserLogin


@pytest.mark.usefixtures("prepare_db", "test_session")
class TestUserDB:

    @pytest.fixture
    def test_user(self):
        return UserCreate(username="Test1", password="Test1", email="test1@mail.ru")

    @pytest.mark.usefixtures("test_user")
    async def test_add_user_db(self, test_session: AsyncSession, test_user: UserCreate):
        user_db = await add_user_db(Session=test_session, user_data=test_user)

        assert test_user.username == user_db.username
        assert test_user.email == user_db.email

    @pytest.mark.usefixtures("test_user")
    async def test_authenticate_user_by_username(
        self, test_session: AsyncSession, test_user: UserCreate
    ):
        test_login_user = UserLogin(
            username=test_user.username, password=test_user.password
        )
        user_schema = await authenticate_user(test_session, test_login_user)

        assert user_schema.username == test_user.username

    @pytest.mark.usefixtures("test_user")
    async def test_authenticate_user_by_email(
        self, test_session: AsyncSession, test_user: UserCreate
    ):
        test_login_user = UserLogin(email=test_user.email, password=test_user.password)
        user_schema = await authenticate_user(test_session, test_login_user)

        assert user_schema.email == test_user.email

    async def test_authenticate_uncreated_user(self, test_session: AsyncSession):
        test_login_user = UserLogin(
            username="incorrect_user", password="incorrect_password"
        )

        with pytest.raises(HTTPException, match="User not found") as ex:
            user_schema = await authenticate_user(test_session, test_login_user)

    @pytest.mark.usefixtures("test_user")
    async def test_authenticate_incorrect_password(
        self, test_session: AsyncSession, test_user: UserCreate
    ):
        test_login_user = UserLogin(
            username=test_user.username, password="incorrect_password"
        )

        with pytest.raises(HTTPException, match="Incorrect Password") as ex:
            user_schema = await authenticate_user(test_session, test_login_user)
