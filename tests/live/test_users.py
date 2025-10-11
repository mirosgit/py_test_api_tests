import pytest
from src.clients.users_client import UsersClient
from src.utils.factory import PersonFactory

@pytest.mark.live
def test_list_users_page_2():
    client = UsersClient()
    resp = client.list_users(page=2)
    assert resp.page == 2
    assert len(resp.data) > 0

@pytest.mark.live
def test_get_single_user():
    client = UsersClient()
    user = client.get_user(2)
    assert user.id == 2
    assert user.email and user.first_name

@pytest.mark.live
def test_user_crud_flow():
    client = UsersClient()
    p = PersonFactory()
    created = client.create_user(name=p.name, job=p.job)
    assert created.id and created.createdAt

    updated = client.update_user_patch(user_id=2, fields={"job": "zion resident"})
    assert "updatedAt" in updated.model_dump()

    status = client.delete_user(2)
    assert status in (204, 200)
