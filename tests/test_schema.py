from pydantic import ValidationError
from app.schema import CommentCreate


def test_comment_create_valid():
    comment = CommentCreate(comment_group_id=1, body="This is a test comment.")
    assert comment.comment_group_id == 1
    assert comment.body == "This is a test comment."


def test_comment_create_optional_comment_group_id():
    comment = CommentCreate(comment_group_id=None, body="This is a test comment.")
    assert comment.comment_group_id is None
    assert comment.body == "This is a test comment."


def test_comment_create_missing_body():
    try:
        CommentCreate(comment_group_id=1)
    except ValidationError as e:
        assert "field required" in str(e)


def test_comment_create_empty_body():
    try:
        CommentCreate(comment_group_id=1, body="")
    except ValidationError as e:
        assert "ensure this value has at least 1 characters" in str(e)


def test_comment_create_invalid_comment_group_id():
    try:
        CommentCreate(comment_group_id="invalid", body="This is a test comment.")
    except ValidationError as e:
        assert "value is not a valid integer" in str(e)
