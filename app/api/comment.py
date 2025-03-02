from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.model import (
    Comment,
    CommentGroup,
)
from app.schema import (
    CommentCreate,
    CommentUpdate,
    CommentGroupCreate,
    CommentGroupUpdate,
)
from app.database import get_db

app = FastAPI()


# コメント (Comment) 関連のAPI
@app.get("/problems/{problem_id}/comments/", response_model=list[Comment])
def read_comments(problem_id: int, db: Session = Depends(get_db)) -> list[Comment]:
    """Read all comments of the problem specified by problem id

    Args:
        problem_id (int): problem id
        db (Session): database session

    Returns:
        list[Comment]: list of comments
    """
    return db.query(Comment).filter(Comment.problem_id == problem_id).all()


@app.post("/problems/{problem_id}/comments/", response_model=Comment)
def create_comment(
    problem_id: int, comment: CommentCreate, db: Session = Depends(get_db)
) -> Comment:
    """Create a new comment for the problem specified by problem id

    Args:
        problem_id (int): problem id
        comment (CommentCreate): comment data
        db (Session): database session

    Returns:
        Comment: created comment
    """
    # Pydanticモデルを使用してリクエストデータを検証
    comment_data = comment.model_dump()
    # 必要な属性をCommentオブジェクトに設定
    comment = Comment(**comment_data)
    comment.problem_id = problem_id
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


@app.put("/comments/{comment_id}", response_model=Comment)
def update_comment(
    comment_id: int, comment: CommentUpdate, db: Session = Depends(get_db)
) -> Comment:
    """Update a comment

    Args:
        comment_id (int): comment id
        comment (CommentUpdate): comment data
        db (Session): database session

    Raises:
        HTTPException: if the comment is not found.

    Returns:
        Comment: updated comment
    """
    db_comment = db.query(Comment).filter(Comment.comment_id == comment_id).first()
    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    for key, value in comment.model_dump(exclude_unset=True).items():
        setattr(db_comment, key, value)
    db.commit()
    db.refresh(db_comment)
    return db_comment


@app.delete("/comments/{comment_id}", status_code=204)
def delete_comment(comment_id: int, db: Session = Depends(get_db)) -> None:
    """Delete a comment by comment id

    Args:
        comment_id (int): comment id
        db (Session): database session

    Raises:
        HTTPException: if the comment is not found.
    """
    db_comment = db.query(Comment).filter(Comment.comment_id == comment_id).first()
    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    db.delete(db_comment)
    db.commit()


@app.get("/comment-groups/", response_model=list[CommentGroup])
def read_comment_groups(db: Session = Depends(get_db)) -> list[CommentGroup]:
    """Read all comment groups

    Args:
        db (Session): database session

    Returns:
        list[CommentGroup]: list of comment groups
    """
    return db.query(CommentGroup).all()


@app.post("/comment-groups/", response_model=CommentGroup)
def create_comment_group(
    comment_group: CommentGroupCreate, db: Session = Depends(get_db)
) -> CommentGroup:
    """Create a new comment group

    Args:
        comment_group (CommentGroupCreate): comment group data
        db (Session): database session

    Returns:
        CommentGroup: created comment
    """
    # Pydanticモデルを使用してリクエストデータを検証
    comment_group_data = comment_group.model_dump()
    # 必要な属性をCommentGroupオブジェクトに設定
    comment_group = CommentGroup(**comment_group_data)
    db.add(comment_group)
    db.commit()
    db.refresh(comment_group)
    return comment_group


@app.put("/comment-groups/{comment_group_id}", response_model=CommentGroup)
def update_comment_group(
    comment_group_id: int,
    comment_group: CommentGroupUpdate,
    db: Session = Depends(get_db),
) -> CommentGroup:
    """Update a comment group

    Args:
        comment_group_id (int): comment group id
        comment_group (CommentGroupUpdate): comment group data
        db (Session): database session

    Raises:
        HTTPException: if the comment group is not found.

    Returns:
        CommentGroup: updated comment group
    """
    db_comment_group = (
        db.query(CommentGroup)
        .filter(CommentGroup.comment_group_id == comment_group_id)
        .first()
    )
    if not db_comment_group:
        raise HTTPException(status_code=404, detail="CommentGroup not found")
    # Pydanticモデルを使用してリクエストデータを検証
    update_data = comment_group.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_comment_group, key, value)
    db.commit()
    db.refresh(db_comment_group)
    return db_comment_group


@app.delete("/comment-groups/{comment_group_id}", status_code=204)
def delete_comment_group(comment_group_id: int, db: Session = Depends(get_db)) -> None:
    """Delete a comment group by comment group id

    Args:
        comment_group_id (int): comment group id
        db (Session): database session

    Raises:
        HTTPException: if the comment group is not found.
    """
    db_comment_group = (
        db.query(CommentGroup)
        .filter(CommentGroup.comment_group_id == comment_group_id)
        .first()
    )
    if not db_comment_group:
        raise HTTPException(status_code=404, detail="CommentGroup not found")
    db.delete(db_comment_group)
    db.commit()
