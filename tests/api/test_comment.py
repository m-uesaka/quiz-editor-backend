from fastapi.testclient import TestClient
from app.api.comment import app
from app.database import SessionLocal, Base, engine
from app.model import Comment, Problem
import pytest

client = TestClient(app)


@pytest.fixture(scope="module")
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session(setup_database):
    session = SessionLocal()
    yield session
    session.close()


def test_read_comments_empty(db_session):
    response = client.get("/problems/1/comments/")
    assert response.status_code == 200
    assert response.json() == []


def test_read_comments(db_session):
    # Create a problem
    problem = Problem(
        problem_text="Sample problem",
        answer="Sample answer",
        created_by=1,
        updated_by=1,
    )
    db_session.add(problem)
    db_session.commit()

    # Create comments
    comment1 = Comment(
        problem_id=problem.problem_id, body="Comment 1", created_by=1, updated_by=1
    )
    comment2 = Comment(
        problem_id=problem.problem_id, body="Comment 2", created_by=1, updated_by=1
    )
    db_session.add(comment1)
    db_session.add(comment2)
    db_session.commit()

    response = client.get(f"/problems/{problem.problem_id}/comments/")
    assert response.status_code == 200
    comments = response.json()
    assert len(comments) == 2
    assert comments[0]["body"] == "Comment 1"
    assert comments[1]["body"] == "Comment 2"


def test_read_comments_nonexistent_problem(db_session):
    response = client.get("/problems/999/comments/")
    assert response.status_code == 200
    assert response.json() == []
