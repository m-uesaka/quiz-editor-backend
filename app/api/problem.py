from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.model import (
    Problem,
    Tag,
    JudgingCriteria,
)
from app.schema import (
    ProblemCreate,
    ProblemUpdate,
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
    for criteria_data in problem_data.get("judging_criteria", []):
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
        if key == "judging_criteria":
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
