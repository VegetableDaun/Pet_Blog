from src.users.schemas import UserSchema
from src.users.utils import add_user_db
from src.users.models import UserCreate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Select, func, Delete
from sqlalchemy.exc import IntegrityError, DBAPIError
import pytest


@pytest.mark.usefixtures("prepare_db", "test_session")
class TestUserSchema:

    @pytest.mark.parametrize(
        "username, email, password",
        [
            ("user1", "user1@example.com", "pass1234"),
            ("alice", "alice@example.com", "alicePwd2024"),
            ("bob_smith", "bob.smith@example.org", "bobSecure!"),
            ("charlie99", "charlie99@domain.net", "charliePass99"),
            ("daisy", "daisy@flower.com", "daisy12345"),
            ("user2", "user2@example.com", "pass5678"),
            ("eve", "eve@example.com", "evePwd2024"),
            ("john_doe", "john.doe@example.org", "johnSecure!"),
            ("lucy88", "lucy88@domain.net", "lucyPass88"),
            ("rose", "rose@flower.com", "rose12345"),
            ("user3", "user3@example.com", "pass9012"),
            ("mark", "mark@example.com", "markPwd2024"),
            ("anna_k", "anna.k@example.org", "annaSecure!"),
            ("mike77", "mike77@domain.net", "mikePass77"),
            ("lily", "lily@flower.com", "lily12345"),
            ("moly", "funy.moly.colida@flower.moly.com", "lily12345"),
        ],
    )
    async def test_add_users(
        self, test_session: AsyncSession, username, email, password
    ):
        user = UserCreate(username=username, email=email, password=password)
        user_db = await add_user_db(Session=test_session, user_data=user)

        assert user_db is not None

    async def test_get_user(self, test_session: AsyncSession):
        query = Select(func.count(UserSchema.id))
        results = await test_session.execute(query)

        len_users = results.scalar()

        assert len_users == 16

    async def test_delete_users(self, test_session: AsyncSession):
        query = Delete(UserSchema).where(UserSchema.id >= 0)

        await test_session.execute(query)
        await test_session.commit()

        assert True

    async def test_too_long_username(self, test_session: AsyncSession):
        user = UserSchema(
            username="x" * 17, email="eve@example.com", password="evePwd2024"
        )

        with pytest.raises(DBAPIError) as ex_pytest:
            test_session.add(user)

            try:
                await test_session.commit()
            except DBAPIError as ex_db:
                await test_session.rollback()

                raise

    async def test_too_long_email(self, test_session: AsyncSession):
        user = UserSchema(
            username="eve", email="no-correct-email", password="evePwd2024"
        )

        # with pytest.raises(IntegrityError) as ex:
        #     test_session.add(user)
        #     await test_session.commit()

        with pytest.raises(IntegrityError) as ex_pytest:
            test_session.add(user)

            try:
                await test_session.commit()
            except DBAPIError as ex_db:
                await test_session.rollback()

                raise

        # assert isinstance(ex.type, CheckViolationError)

    async def test_too_long_password(self, test_session: AsyncSession):
        user = UserSchema(username="eve8", email="eve@example.com", password="x" * 73)

        with pytest.raises(DBAPIError) as ex_pytest:
            test_session.add(user)

            try:
                await test_session.commit()
            except DBAPIError as ex_db:
                await test_session.rollback()

                raise
