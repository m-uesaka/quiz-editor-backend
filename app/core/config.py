"""This module contains the configuration of the application"""

import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    """settings"""

    SECRET_KEY: str = os.getenv("SECRET_KEY")
    DATABASE_URL: str = os.getenv("DATABASE_URL")


settings = Settings()
