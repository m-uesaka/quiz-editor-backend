from app.database import engine, SessionLocal, get_db, Base


def test_engine_creation():
    assert engine is not None


def test_session_local_creation():
    session = SessionLocal()
    assert session is not None
    session.close()


def test_get_db():
    db_gen = get_db()
    db = next(db_gen)
    assert db is not None
    db.close()


def test_base_declarative():
    assert Base is not None


def test_base_query_property():
    assert hasattr(Base, "query")
