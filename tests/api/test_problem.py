from fastapi.testclient import TestClient
from app.api.problem import app
from app.database import SessionLocal, Base, engine
from app.model import Problem
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


def test_read_problems_empty(db_session):
    response = client.get("/problems/")
    assert response.status_code == 200
    assert response.json() == []


def test_create_problem(db_session):
    problem_data = {
        "problem_text": "What is the capital of France?",
        "answer": "Paris",
        "genre_id": 1,
        "sort_order": 1,
        "tags": [],
        "judging_criteria": [],
    }
    response = client.post("/problems/", json=problem_data)
    assert response.status_code == 200
    problem = response.json()
    assert problem["problem_text"] == "What is the capital of France?"
    assert problem["answer"] == "Paris"


def test_read_problem(db_session):
    problem = Problem(
        problem_text="Sample problem",
        answer="Sample answer",
        created_by=1,
        updated_by=1,
    )
    db_session.add(problem)
    db_session.commit()
    response = client.get(f"/problems/{problem.problem_id}")
    assert response.status_code == 200
    problem_data = response.json()
    assert problem_data["problem_text"] == "Sample problem"
    assert problem_data["answer"] == "Sample answer"


def test_update_problem(db_session):
    problem = Problem(
        problem_text="Old problem", answer="Old answer", created_by=1, updated_by=1
    )
    db_session.add(problem)
    db_session.commit()
    update_data = {"problem_text": "Updated problem", "answer": "Updated answer"}
    response = client.put(f"/problems/{problem.problem_id}", json=update_data)
    assert response.status_code == 200
    updated_problem = response.json()
    assert updated_problem["problem_text"] == "Updated problem"
    assert updated_problem["answer"] == "Updated answer"


def test_delete_problem(db_session):
    problem = Problem(
        problem_text="Problem to delete",
        answer="Answer to delete",
        created_by=1,
        updated_by=1,
    )
    db_session.add(problem)
    db_session.commit()
    response = client.delete(f"/problems/{problem.problem_id}")
    assert response.status_code == 204
    response = client.get(f"/problems/{problem.problem_id}")
    assert response.status_code == 404


def test_read_problems_with_filters(db_session):
    problem1 = Problem(
        problem_text="Problem 1",
        answer="Answer 1",
        genre_id=1,
        created_by=1,
        updated_by=1,
    )
    problem2 = Problem(
        problem_text="Problem 2",
        answer="Answer 2",
        genre_id=2,
        created_by=1,
        updated_by=1,
    )
    db_session.add(problem1)
    db_session.add(problem2)
    db_session.commit()

    response = client.get("/problems/?genre_id=1")
    assert response.status_code == 200
    problems = response.json()
    assert len(problems) == 1
    assert problems[0]["problem_text"] == "Problem 1"

    response = client.get("/problems/?keyword=Problem")
    assert response.status_code == 200
    problems = response.json()
    assert len(problems) == 2

    response = client.get("/problems/?order_by=problem_text&order_dir=DESC")
    assert response.status_code == 200
    problems = response.json()
    assert problems[0]["problem_text"] == "Problem 2"
