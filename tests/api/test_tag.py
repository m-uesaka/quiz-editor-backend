from fastapi.testclient import TestClient
from app.api.tag import app
from app.database import SessionLocal, Base, engine
from app.model import TagGroup, Tag
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


def test_read_tag_groups_empty(db_session):
    response = client.get("/tag-groups/")
    assert response.status_code == 200
    assert response.json() == []


def test_create_tag_group(db_session):
    tag_group_data = {"group_name": "Difficulty"}
    response = client.post("/tag-groups/", json=tag_group_data)
    assert response.status_code == 200
    tag_group = response.json()
    assert tag_group["group_name"] == "Difficulty"


def test_update_tag_group(db_session):
    tag_group = TagGroup(group_name="Old Group")
    db_session.add(tag_group)
    db_session.commit()
    update_data = {"group_name": "Updated Group"}
    response = client.put(f"/tag-groups/{tag_group.tag_group_id}", json=update_data)
    assert response.status_code == 200
    updated_tag_group = response.json()
    assert updated_tag_group["group_name"] == "Updated Group"


def test_delete_tag_group(db_session):
    tag_group = TagGroup(group_name="Group to delete")
    db_session.add(tag_group)
    db_session.commit()
    response = client.delete(f"/tag-groups/{tag_group.tag_group_id}")
    assert response.status_code == 204
    response = client.get(f"/tag-groups/{tag_group.tag_group_id}")
    assert response.status_code == 404


def test_read_tags_empty(db_session):
    tag_group = TagGroup(group_name="Group with no tags")
    db_session.add(tag_group)
    db_session.commit()
    response = client.get(f"/tag-groups/{tag_group.tag_group_id}/tags/")
    assert response.status_code == 200
    assert response.json() == []


def test_create_tag(db_session):
    tag_group = TagGroup(group_name="Group for tags")
    db_session.add(tag_group)
    db_session.commit()
    tag_data = {"tag_name": "Easy"}
    response = client.post(f"/tag-groups/{tag_group.tag_group_id}/tags/", json=tag_data)
    assert response.status_code == 200
    tag = response.json()
    assert tag["tag_name"] == "Easy"
    assert tag["tag_group_id"] == tag_group.tag_group_id


def test_update_tag(db_session):
    tag_group = TagGroup(group_name="Group for updating tags")
    db_session.add(tag_group)
    db_session.commit()
    tag = Tag(tag_group_id=tag_group.tag_group_id, tag_name="Old Tag")
    db_session.add(tag)
    db_session.commit()
    update_data = {"tag_name": "Updated Tag"}
    response = client.put(f"/tags/{tag.tag_id}", json=update_data)
    assert response.status_code == 200
    updated_tag = response.json()
    assert updated_tag["tag_name"] == "Updated Tag"


def test_delete_tag(db_session):
    tag_group = TagGroup(group_name="Group for deleting tags")
    db_session.add(tag_group)
    db_session.commit()
    tag = Tag(tag_group_id=tag_group.tag_group_id, tag_name="Tag to delete")
    db_session.add(tag)
    db_session.commit()
    response = client.delete(f"/tags/{tag.tag_id}")
    assert response.status_code == 204
    response = client.get(f"/tags/{tag.tag_id}")
    assert response.status_code == 404
