import json
from jsonschema import validate
from src.clients.users_client import UsersClient
from pathlib import Path
import pytest

@pytest.mark.contract
def test_list_users_contract():
    client = UsersClient()
    resp_raw = client.get("/api/users", params={"page": 1})
    resp_raw.raise_for_status()
    data = resp_raw.json()

    schema_path = Path("src/schemas/list_users.json")
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validate(instance=data, schema=schema)

@pytest.mark.contract
def test_single_user_contract():
    client = UsersClient()
    resp_raw = client.get("/api/users/2")
    resp_raw.raise_for_status()
    data = resp_raw.json().get("data")
    schema_path = Path("src/schemas/user.json")
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validate(instance=data, schema=schema)
