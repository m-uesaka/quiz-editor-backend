import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.model import (
    Base,
    User,
    Genre,
    Problem,
    JudgingCriteria,
    CommentGroup,
    Comment,
    TagGroup,
    Tag,
)

DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


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


def test_create_user(db_session):
    new_user = User(username="testuser", email="testuser@example.com")
    db_session.add(new_user)
    db_session.commit()
    assert new_user.user_id is not None


def test_create_genre(db_session):
    new_genre = Genre(genre_name="Science", created_by=1, updated_by=1)
    db_session.add(new_genre)
    db_session.commit()
    assert new_genre.genre_id is not None


def test_create_problem(db_session):
    new_problem = Problem(
        problem_text="What is the capital of France?",
        genre_id=1,
        created_by=1,
        updated_by=1,
    )
    db_session.add(new_problem)
    db_session.commit()
    assert new_problem.problem_id is not None


def test_create_judging_criteria(db_session):
    new_criteria = JudgingCriteria(
        problem_id=1,
        criteria_type="accuracy",
        criteria_text="Must be correct",
        created_by=1,
        updated_by=1,
    )
    db_session.add(new_criteria)
    db_session.commit()
    assert new_criteria.criteria_id is not None


def test_create_comment_group(db_session):
    new_comment_group = CommentGroup(
        group_name="General Comments", created_by=1, updated_by=1
    )
    db_session.add(new_comment_group)
    db_session.commit()
    assert new_comment_group.comment_group_id is not None


def test_create_comment(db_session):
    new_comment = Comment(
        problem_id=1,
        title="Sample Comment",
        body="This is a sample comment.",
        created_by=1,
        updated_by=1,
    )
    db_session.add(new_comment)
    db_session.commit()
    assert new_comment.comment_id is not None


def test_create_tag_group(db_session):
    new_tag_group = TagGroup(group_name="Difficulty", created_by=1, updated_by=1)
    db_session.add(new_tag_group)
    db_session.commit()
    assert new_tag_group.tag_group_id is not None


def test_create_tag(db_session):
    new_tag = Tag(tag_group_id=1, tag_name="Easy", created_by=1, updated_by=1)
    db_session.add(new_tag)
    db_session.commit()
    assert new_tag.tag_id is not None
