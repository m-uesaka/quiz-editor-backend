from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.model import (
    TagGroup,
    Tag,
)
from app.schema import (
    TagGroupCreate,
    TagGroupUpdate,
    TagUpdate,
    TagCreate,
)
from app.database import get_db

app = FastAPI()


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
