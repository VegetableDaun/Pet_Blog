import pytest
import random
from authx import RequestToken

from src.auth.utils import verify_password, get_password_hash
from src.auth.security import security


class TestHash:
    @pytest.fixture
    def test_password(self) -> str:
        return "test_password"

    @pytest.fixture
    def test_get_password_hash(self, test_password: str) -> str:
        return get_password_hash(test_password)

    def test_verify_password(self, test_password: str, test_get_password_hash: str):
        assert verify_password(test_password, test_get_password_hash)
