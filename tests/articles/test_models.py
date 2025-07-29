import pytest
from pydantic import ValidationError
from src.articles.models import ArticleCreate, ArticlePublic, ArticleUpdate


class TestArticleCreate:

    def test_valid(self):
        article = ArticleCreate(
            title="Breaking News", content="This is a short article.", secret_info="Top secret"
        )
        assert article.title == "Breaking News"
        assert article.content == "This is a short article."
        assert article.secret_info == "Top secret"

    def test_valid_without_secret_info(self):
        article = ArticleCreate(
            title="Update", content="Public content only"
        )
        assert article.secret_info is None

    def test_title_too_long(self):
        with pytest.raises(ValidationError):
            ArticleCreate(
                title="x" * 81, content="Short", secret_info="Optional"
            )

    def test_content_too_long(self):
        with pytest.raises(ValidationError):
            ArticleCreate(
                title="Valid", content="x" * 281, secret_info="Optional"
            )

    def test_secret_info_too_long(self):
        with pytest.raises(ValidationError):
            ArticleCreate(
                title="Valid", content="Valid", secret_info="x" * 81
            )


class TestArticlePublic:

    def test_valid(self):
        article = ArticlePublic(title="Public Title", content="Visible content")

        assert article.title == "Public Title"
        assert article.content == "Visible content"

    def test_title_too_long(self):
        with pytest.raises(ValidationError):
            ArticlePublic(title="x" * 81, content="Content")

    def test_content_too_long(self):
        with pytest.raises(ValidationError):
            ArticlePublic(title="Valid", content="x" * 281)


class TestArticleUpdate:

    @pytest.mark.parametrize(
        "title, content",
        [
            ("New Title", "New content"),
            (None, "Only content updated"),
            ("Only title updated", None),
            (None, None),
        ],
    )
    def test_valid(self, title, content):
        article = ArticleUpdate(title=title, content=content)

        assert article.title == title
        assert article.content == content

    def test_title_too_long(self):
        with pytest.raises(ValidationError):
            ArticleUpdate(title="x" * 81)

    def test_content_too_long(self):
        with pytest.raises(ValidationError):
            ArticleUpdate(content="x" * 281)
