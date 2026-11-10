import pytest

from app import create_app
from app.config.settings import TestConfig
from app.extensions import db


@pytest.fixture()
def app():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def make_book(client):
    def _make(**overrides):
        payload = {
            "title": "Clean Code",
            "author": "Robert Martin",
            "category": "Technology",
            "published_year": 2008,
        }
        payload.update(overrides)
        res = client.post("/api/books", json=payload)
        assert res.status_code == 201, res.get_json()
        return res.get_json()

    return _make
