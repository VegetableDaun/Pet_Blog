import pytest
from pydantic import ValidationError
from src.users.models import UserCreate, UserLogin, UserPublic, UserUpdate


class TestUserCreate:

    def test_valid(self):
        user = UserCreate(
            username="john", email="john@example.com", password="secure123"
        )

        assert user.username == "john"
        assert user.email == "john@example.com"
        assert user.password == "secure123"

    def test_invalid_email(self):
        with pytest.raises(ValidationError):
            UserCreate(username="john", email="not-an-email", password="secure123")

    def test_username_too_long(self):
        with pytest.raises(ValidationError):
            UserCreate(
                username="x" * 17, email="john@example.com", password="secure123"
            )

    def test_email_too_long(self):
        with pytest.raises(ValidationError):
            UserCreate(
                username="john", email="john" * 6 + "@example.com", password="secure123"
            )

    def test_password_too_long(self):
        with pytest.raises(ValidationError):
            UserCreate(username="john", email="john@example.com", password="x" * 33)


class TestUserPublic:

    def test_valid(self):
        user = UserPublic(username="john")
        assert user.username == "john"

    def test_username_too_long(self):
        with pytest.raises(ValidationError):
            UserPublic(username="x" * 17)


class TestUserLogin:

    def test_valid_with_username(self):
        user = UserLogin(username="john", password="secure123")

        assert user.username == "john"
        assert user.password == "secure123"

    def test_valid_with_email(self):
        user = UserLogin(email="john@example.com", password="secure123")

        assert user.email == "john@example.com"
        assert user.password == "secure123"

    def test_no_username_or_email(self):
        with pytest.raises(
            ValidationError, match="At least one of Username or Email must be filled."
        ) as ex:
            UserLogin(password="secure123")

    def test_valid_both_username_and_email(self):
        user = UserLogin(
            username="john", email="john@example.com", password="secure123"
        )

        assert user.username == "john"
        assert user.email == "john@example.com"

    def test_invalid_email(self):
        with pytest.raises(ValidationError):
            UserUpdate(email="invalid-email")

    def test_too_long_username(self):
        with pytest.raises(ValidationError):
            UserLogin(username="x" * 17, password="secure123")

    def test_too_long_email_(self):
        with pytest.raises(ValidationError):
            UserLogin(email="john" * 6 + "@example.com", password="secure123")

    def test_too_long_password_(self):
        with pytest.raises(ValidationError):
            UserLogin(username="john", password="x" * 33)


class TestUserUpdate:

    @pytest.mark.parametrize(
        "username, email, password",
        [
            ("john", "updated@example.com", "secure123"),
            ("john", "updated@example.com", None),
            ("john", None, "secure123"),
            (None, "updated@example.com", "secure123"),
            (None, None, "secure123"),
            (None, "updated@example.com", None),
            ("john", None, None),
            (None, None, None),
        ],
    )
    def test_valid(self, username, email, password):
        user = UserUpdate(username=username, email=email, password=password)

        assert user.username == username
        assert user.email == email
        assert user.password == password

    def test_invalid_email(self):
        with pytest.raises(ValidationError):
            UserUpdate(email="invalid-email")

    def test_username_too_long(self):
        with pytest.raises(ValidationError):
            UserUpdate(username="x" * 17)

    def test_too_long_email_(self):
        with pytest.raises(ValidationError):
            UserUpdate(email="john" * 6 + "@example.com")

    def test_too_long_password_(self):
        with pytest.raises(ValidationError):
            UserUpdate(password="x" * 33)
