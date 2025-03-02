from pydantic import BaseModel


# Pydanticモデルの定義
class JudgingCriteriaCreate(BaseModel):
    criteria_type: str
    criteria_text: str


class JudgingCriteriaUpdate(BaseModel):
    criteria_type: str | None
    criteria_text: str | None


class ProblemCreate(BaseModel):
    """Pydantic model that defines the schema for creating a new problem.

    Attributes:
        problem_text (str): problem text
        answer (str): answer
        original_text (str | None): original text
        genre_id (int | None): genre id
        sort_order (int | None): sort order
        tags (list[int]): list of tag ids
        judging_criteria (list[JudgingCriteriaCreate]): list of judging criteria
    """

    problem_text: str
    answer: str
    original_text: str | None
    genre_id: int | None
    sort_order: int | None
    tags: list[int]
    judging_criteria: list[JudgingCriteriaCreate]  # 新しいフィールド


class ProblemUpdate(BaseModel):
    """Pydantic model that defines the schema for updating a problem.

    Attributes:
        problem_text (str | None): problem text
        answer (str | None): answer
        original_text (str | None): original text
        genre_id (int | None): genre id
        sort_order (int | None): sort order
        tags (list[int] | None): list of tag ids
        judging_criteria (list[JudgingCriteriaUpdate] | None): list of judging criteria
    """

    problem_text: str | None
    answer: str | None
    original_text: str | None
    genre_id: int | None
    sort_order: int | None
    tags: list[int] | None
    judging_criteria: list[JudgingCriteriaUpdate] | None  # 新しいフィールド


class TagGroupCreate(BaseModel):
    """Pydantic model that defines the schema for creating a new tag group.

    Attributes:
        group_name (str): group name
    """

    group_name: str


class TagGroupUpdate(BaseModel):
    """Pydantic model that defines the schema for updating a tag group.

    Attributes:
        group_name (str | None): group name
    """

    group_name: str | None


class TagCreate(BaseModel):
    """Pydantic model that defines the schema for creating a new tag.

    Attributes:
        tag_name (str): tag name
        sort_order (int | None): sort order
    """

    tag_name: str
    sort_order: int | None


class TagUpdate(BaseModel):
    """Pydantic model that defines the schema for updating a tag.

    Attributes:
        tag_name (str | None): tag name
        sort_order (int | None): sort order
    """

    tag_name: str | None
    sort_order: int | None


class CommentGroupCreate(BaseModel):
    """Pydantic model that defines the schema for creating a new comment group.

    Attributes:
        group_name (str): group name
    """

    group_name: str


class CommentGroupUpdate(BaseModel):
    """Pydantic model that defines the schema for updating a comment group.

    Attributes:
        group_name (str | None): group name
    """

    group_name: str | None


class CommentCreate(BaseModel):
    """Pydantic model that defines the schema for creating a new comment.

    Attributes:
        comment_group_id (int | None): comment group id
        body (str): body
    """

    comment_group_id: int | None
    body: str


class CommentUpdate(BaseModel):
    """Pydantic model that defines the schema for updating a comment.

    Attributes:
        comment_group_id (int | None): comment group id
        body (str | None): body
    """

    comment_group_id: int | None
    body: str | None
