import os
from app.core.config import settings, Settings


def test_load_dotenv():
    assert os.getenv("SECRET_KEY") is not None
    assert os.getenv("DATABASE_URL") is not None


def test_settings_secret_key():
    assert settings.SECRET_KEY == os.getenv("SECRET_KEY")


def test_settings_database_url():
    assert settings.DATABASE_URL == os.getenv("DATABASE_URL")


def test_settings_instance():
    assert isinstance(settings, Settings)
