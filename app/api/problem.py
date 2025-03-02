from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.model import (
    Problem,
    TagGroup,
    Tag,
    JudgingCriteria,
    Comment,
    CommentGroup,
)
from app.schema import (
    ProblemCreate,
    ProblemUpdate,
    TagGroupCreate,
    TagGroupUpdate,
    TagUpdate,
    TagCreate,
    CommentCreate,
    CommentUpdate,
    CommentGroupCreate,
    CommentGroupUpdate,
)
from app.database import get_db

app = FastAPI()


# 問題 (Problem) 関連のAPI
@app.get("/problems/", response_model=list[Problem])
def read_problems(
    db: Session = Depends(get_db),
    genre_id: int | None = Query(None),
    tag_id: list[int] | None = Query(None),
    keyword: str | None = Query(None),
    order_by: str | None = Query(None),
    order_dir: str | None = Query("ASC"),
) -> list[Problem]:
    """Read problems

    Args:
        db (Session): database session
        genre_id (int, optional): genre id.
            Defaults to None.
        tag_id (list[int], optional): list of tag ids.
            Defaults to None.
        keyword (str, optional): keyword.
            Defaults to None.
        order_by (str, optional): the key to order by.
            Defaults to None.
        order_dir (str, optional): order direction.
            The value is either"ASC", "DESC" or None.
            Defaults to "ASC".

    Returns:
        list[Problem]: list of problems
    """
    query = db.query(Problem)
    if genre_id:
        query = query.filter(Problem.genre_id == genre_id)
    if tag_id:
        query = query.filter(Problem.tags.any(Tag.tag_id.in_(tag_id)))
    if keyword:
        query = query.filter(Problem.problem_text.ilike(f"%{keyword}%"))

    if order_by:
        order_keys = []
        for key in order_by.split(","):
            if hasattr(Problem, key):
                order_keys.append(getattr(Problem, key))
            elif hasattr(Tag, key):
                order_keys.append(Tag.tag_name)
        if order_dir == "DESC":
            order_keys = [key.desc() for key in order_keys]
        query = query.order_by(*order_keys)

    return query.all()


@app.post("/problems/", response_model=Problem)
def create_problem(problem: ProblemCreate, db: Session = Depends(get_db)) -> Problem:
    """Create a new problem

    Args:
        problem (ProblemCreate): problem data
        db (Session): database session

    Returns:
        Problem: created problem
    """
    # Pydanticモデルを使用してリクエストデータを検証
    problem_data = problem.model_dump()
    # 必要な属性を問題オブジェクトに設定
    problem = Problem(**problem_data)
    for criteria_data in problem_data.get('judging_criteria', []):
        criteria = JudgingCriteria(**criteria_data.dict())
        criteria.problem = problem
        db.add(criteria)
    db.add(problem)
    db.commit()
    db.refresh(problem)
    return problem


@app.get("/problems/{problem_id}", response_model=Problem)
def read_problem(problem_id: int, db: Session = Depends(get_db)) -> Problem:
    """Read a problem by problem id

    Args:
        problem_id (int): problem id
        db (Session): database session

    Returns:
        Problem: problem
    """
    db_problem = db.query(Problem).filter(Problem.problem_id == problem_id).first()
    if not db_problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    return db_problem


@app.put("/problems/{problem_id}", response_model=Problem)
def update_problem(
    problem_id: int, problem: ProblemUpdate, db: Session = Depends(get_db)
) -> Problem:
    """Update a problem

    Args:
        problem_id (int): problem id
        problem (ProblemUpdate): problem data
        db (Session): database session

    Returns:
        Problem: updated problem
    """
    db_problem = db.query(Problem).filter(Problem.problem_id == problem_id).first()
    if not db_problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    # Pydanticモデルを使用してリクエストデータを検証
    update_data = problem.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        if key == 'judging_criteria':
            # 判定基準は個別に処理
            for criteria_data in value:
                criteria = JudgingCriteria(**criteria_data.dict())
                criteria.problem_id = problem_id
                db.add(criteria)
        else:
            setattr(db_problem, key, value)
    db.commit()
    db.refresh(db_problem)
    return db_problem


@app.delete("/problems/{problem_id}", status_code=204)
def delete_problem(problem_id: int, db: Session = Depends(get_db)) -> None:
    """Delete a problem by problem id

    Args:
        problem_id (int): problem id
        db (Session): database session

    Raises:
        HTTPException: if the problem is not found.
    """
    db_problem = db.query(Problem).filter(Problem.problem_id == problem_id).first()
    if not db_problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    db.delete(db_problem)
    db.commit()


# タググループ (TagGroup) / タグ (Tag) 関連のAPI
@app.get("/tag-groups/", response_model=list[TagGroup])
def read_tag_groups(db: Session = Depends(get_db)) -> list[TagGroup]:
    """Read tag groups

    Args:
        db (Session): database session
    """
    return db.query(TagGroup).all()


@app.post("/tag-groups/", response_model=TagGroup)
def create_tag_group(
    tag_group: TagGroupCreate, db: Session = Depends(get_db)
) -> TagGroup:
    """Create a new tag group

    Args:
        tag_group (TagGroupCreate): tag group data
        db (Session): database session

    Returns:
        TagGroup: created tag group
    """
    # Pydanticモデルを使用してリクエストデータを検証
    tag_group_data = tag_group.model_dump()
    # 必要な属性をTagGroupオブジェクトに設定
    tag_group = TagGroup(**tag_group_data)
    db.add(tag_group)
    db.commit()
    db.refresh(tag_group)
    return tag_group


@app.put("/tag-groups/{tag_group_id}", response_model=TagGroup)
def update_tag_group(
    tag_group_id: int, tag_group: TagGroupUpdate, db: Session = Depends(get_db)
) -> TagGroup:
    """Update a tag group

    Args:
        tag_group_id (int): tag group id
        tag_group (TagGroupUpdate): tag group data
        db (Session): database session

    Raises:
        HTTPException: if the tag group is not found.

    Returns:
        TagGroup: updated tag group
    """
    db_tag_group = (
        db.query(TagGroup).filter(TagGroup.tag_group_id == tag_group_id).first()
    )
    if not db_tag_group:
        raise HTTPException(status_code=404, detail="TagGroup not found")

    update_data = tag_group.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_tag_group, key, value)
    db.commit()
    db.refresh(db_tag_group)
    return db_tag_group


@app.delete("/tag-groups/{tag_group_id}", status_code=204)
def delete_tag_group(tag_group_id: int, db: Session = Depends(get_db)) -> None:
    """Delete a tag group by tag group id

    Args:
        tag_group_id (int): tag group id
        db (Session): database session

    Raises:
        HTTPException: if the tag group is not found.
    """
    db_tag_group = (
        db.query(TagGroup).filter(TagGroup.tag_group_id == tag_group_id).first()
    )
    if not db_tag_group:
        raise HTTPException(status_code=404, detail="TagGroup not found")
    db.delete(db_tag_group)
    db.commit()


@app.get("/tag-groups/{tag_group_id}/tags/", response_model=list[Tag])
def read_tags(tag_group_id: int, db: Session = Depends(get_db)) -> list[Tag]:
    """Read all tags in the tag group specified by tag group id

    Args:
        tag_group_id (int): tag group id
        db (Session): database session

    Returns:
        list[Tag]: list of tags in the tag group
    """
    return db.query(Tag).filter(Tag.tag_group_id == tag_group_id).all()


@app.post("/tag-groups/{tag_group_id}/tags/", response_model=Tag)
def create_tag(tag_group_id: int, tag: TagCreate, db: Session = Depends(get_db)) -> Tag:
    """Create a new tag in the tag group specified by tag group id

    Args:
        tag_group_id (int): tag group id
        tag (TagCreate): tag data to be created
        db (Session): database session

    Returns:
        Tag: created tag
    """
    tag.tag_group_id = tag_group_id
    # Pydanticモデルを使用してリクエストデータを検証
    tag_data = tag.model_dump()
    # 必要な属性をTagオブジェクトに設定
    tag = Tag(**tag_data)
    db.add(tag)
    db.commit()
    db.refresh(tag)
    return tag


@app.put("/tags/{tag_id}", response_model=Tag)
def update_tag(tag_id: int, tag: TagUpdate, db: Session = Depends(get_db)) -> Tag:
    """Update a tag

    Args:
        tag_id (int): tag id
        tag (TagUpdate): tag data
        db (Session): database session

    Raises:
        HTTPException: if the tag is not found.

    Returns:
        Tag: updated tag
    """
    db_tag = db.query(Tag).filter(Tag.tag_id == tag_id).first()
    if not db_tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    update_data = tag.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_tag, key, value)
    db.commit()
    db.refresh(db_tag)
    return db_tag

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
def create_comment(problem_id: int, comment: CommentCreate, db: Session = Depends(get_db)) -> Comment:
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
def update_comment(comment_id: int, comment: CommentUpdate, db: Session = Depends(get_db)) -> Comment:
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
def create_comment_group(comment_group: CommentGroupCreate, db: Session = Depends(get_db)) -> CommentGroup:
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
def update_comment_group(comment_group_id: int, comment_group: CommentGroupUpdate, db: Session = Depends(get_db)) -> CommentGroup:
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
    db_comment_group = db.query(CommentGroup).filter(CommentGroup.comment_group_id == comment_group_id).first()
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
    db_comment_group = db.query(CommentGroup).filter(CommentGroup.comment_group_id == comment_group_id).first()
    if not db_comment_group:
        raise HTTPException(status_code=404, detail="CommentGroup not found")
    db.delete(db_comment_group)
    db.commit()
