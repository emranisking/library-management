import os


class Config:
    """Development / production configuration.

    A relative sqlite URI is resolved by Flask-SQLAlchemy against the
    application's ``instance/`` folder, so the default DB lives at
    ``instance/library.db``.
    """

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///library.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False
    CORS_ORIGINS = os.environ.get("CORS_ORIGINS", "*")


class TestConfig(Config):
    """Isolated in-memory database for the test-suite."""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
