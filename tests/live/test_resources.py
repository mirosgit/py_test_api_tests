import pytest
from src.clients.resources_client import ResourcesClient

@pytest.mark.live
def test_list_resources_and_single():
    client = ResourcesClient()
    listing = client.list_resources(page=1)
    assert listing.page == 1
    assert len(listing.data) > 0
    res_id = listing.data[0].id
    resource = client.get_resource(res_id)
    assert resource.id == res_id

@pytest.mark.live
def test_delayed_users():
    client = ResourcesClient()
    status = client.delayed_users(delay_seconds=2)
    assert status == 200
