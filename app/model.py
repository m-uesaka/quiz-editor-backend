from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Text,
    ForeignKey,
    DateTime,
    func,
    Table,
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

problem_tag_association = Table(
    "problem_tag",
    Base.metadata,
    Column("problem_id", Integer, ForeignKey("problem.problem_id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tag.tag_id"), primary_key=True),
)


class User(Base):
    """User model

    Attributes:
        __tablename__ (str): table name
        user_id (int): user id
        username (str): username
        email (str): email
        created_at (datetime): datetime created
        updated_at (datetime): datetime updated
    """

    __tablename__ = "user"
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    email = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class Genre(Base):
    """Genre model

    Attributes:
        __tablename__ (str): table name
        genre_id (int): genre id
        genre_name (str): genre name
        created_at (datetime): datetime created
        updated_at (datetime): datetime updated
        created_by (int): id of user who created the genre
        updated_by (int): id of user who updated the genre
        problems (relationship): relationship to Problem model.
    """

    __tablename__ = "genre"
    genre_id = Column(Integer, primary_key=True, index=True)
    genre_name = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    created_by = Column(Integer, ForeignKey("user.user_id"))
    updated_by = Column(Integer, ForeignKey("user.user_id"))
    problems = relationship("Problem", back_populates="genre")


class Problem(Base):
    """Problem model

    Attributes:
        __tablename__ (str): table name
        problem_id (int): problem id
        problem_text (str): problem text
        answer (str): answer
        original_text (str): original text
        genre_id (int): genre id
        sort_order (int): sort order
        created_at (datetime): datetime created
        updated_at (datetime): datetime updated
        created_by (int): id of user who created the problem
        updated_by (int): id of user who updated the problem
        genre (relationship): relationship to Genre model
        tags (relationship): relationship to Tag model
        comments (relationship): relationship to Comment model
        judging_criteria (relationship): relationship to JudgingCriteria model
    """

    __tablename__ = "problem"
    problem_id = Column(Integer, primary_key=True, index=True)
    problem_text = Column(Text, nullable=False)
    answer = Column(Text)
    original_text = Column(Text)
    genre_id = Column(Integer, ForeignKey("genre.genre_id"))
    sort_order = Column(Integer)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    created_by = Column(Integer, ForeignKey("user.user_id"))
    updated_by = Column(Integer, ForeignKey("user.user_id"))
    genre = relationship("Genre", back_populates="problems")
    tags = relationship(
        "Tag", secondary=problem_tag_association, back_populates="problems"
    )
    comments = relationship("Comment", back_populates="problem")
    judging_criteria = relationship("JudgingCriteria", back_populates="problem")


class JudgingCriteria(Base):
    """Judging Criteria model

    Attributes:
        __tablename__ (str): table name
        criteria_id (int): criteria id
        problem_id (int): problem id
        criteria_type (str): criteria type
        criteria_text (str): criteria text
        created_at (datetime): datetime created
        updated_at (datetime): datetime updated
        created_by (int): id of user who created the criteria
        updated_by (int): id of user who updated the criteria
        problem (relationship): relationship to Problem model
    """

    __tablename__ = "judging_criteria"
    criteria_id = Column(Integer, primary_key=True, index=True)
    problem_id = Column(Integer, ForeignKey("problem.problem_id"))
    criteria_type = Column(String, nullable=False)
    criteria_text = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    created_by = Column(Integer, ForeignKey("user.user_id"))
    updated_by = Column(Integer, ForeignKey("user.user_id"))
    problem = relationship("Problem", back_populates="judging_criteria")


class Comment(Base):
    """Comment model

    Attributes:
        __tablename__ (str): table name
        comment_id (int): comment id
        problem_id (int): problem id
        title (str): title
        body (str): body
        created_at (datetime): datetime created
        updated_at (datetime): datetime updated
        created_by (int): id of user who created the comment
        updated_by (int): id of user who updated the comment
        problem (relationship): relationship to Problem model
    """

    __tablename__ = "comment"
    comment_id = Column(Integer, primary_key=True, index=True)
    problem_id = Column(Integer, ForeignKey("problem.problem_id"))
    title = Column(String)
    body = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    created_by = Column(Integer, ForeignKey("user.user_id"))
    updated_by = Column(Integer, ForeignKey("user.user_id"))
    problem = relationship("Problem", back_populates="comments")


class TagGroup(Base):
    """Tag Group model

    Attributes:
        __tablename__ (str): table name
        tag_group_id (int): tag group id
        group_name (str): group name
        created_at (datetime): datetime created
        updated_at (datetime): datetime updated
        created_by (int): id of user who created the tag group
        updated_by (int): id of user who updated the tag group
        tags (relationship): relationship to Tag model
    """

    __tablename__ = "tag_group"
    tag_group_id = Column(Integer, primary_key=True, index=True)
    group_name = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    created_by = Column(Integer, ForeignKey("user.user_id"))
    updated_by = Column(Integer, ForeignKey("user.user_id"))
    tags = relationship("Tag", back_populates="tag_group")


class Tag(Base):
    """Tag model

    Attributes:
        __tablename__ (str): table name
        tag_id (int): tag id
        tag_group_id (int): tag group id
        tag_name (str): tag name
        sort_order (int): sort order
        created_at (datetime): datetime created
        updated_at (datetime): datetime updated
        created_by (int): id of user who created the tag
        updated_by (int): id of user who updated the tag
        tag_group (relationship): relationship to TagGroup model
        problems (relationship): relationship to Problem model
    """

    __tablename__ = "tag"
    tag_id = Column(Integer, primary_key=True, index=True)
    tag_group_id = Column(Integer, ForeignKey("tag_group.tag_group_id"))
    tag_name = Column(String, nullable=False)
    sort_order = Column(Integer)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    created_by = Column(Integer, ForeignKey("user.user_id"))
    updated_by = Column(Integer, ForeignKey("user.user_id"))
    tag_group = relationship("TagGroup", back_populates="tags")
    problems = relationship(
        "Problem", secondary=problem_tag_association, back_populates="tags"
    )
