from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from app.core.config import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)
Base = declarative_base()
Base.query = SessionLocal.query_property()


def get_db():
    """get database session

    Yields:
        Session: database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
