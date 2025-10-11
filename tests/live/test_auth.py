import pytest
from src.clients.auth_client import AuthClient

@pytest.mark.live
def test_login_success():
    client = AuthClient()
    token = client.login(email="eve.holt@reqres.in", password="cityslicka")
    assert token.token and isinstance(token.token, str)

@pytest.mark.live
def test_login_unsuccessful_missing_password():
    client = AuthClient()
    import httpx
    with pytest.raises(httpx.HTTPStatusError) as exc:
        client.login(email="peter@klaven", password="")
    assert exc.value.response.status_code == 400
    assert "error" in exc.value.response.json()
