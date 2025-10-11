import pytest
from src.utils.config import Settings
from src.clients.base_client import BaseAPIClient

@pytest.fixture(scope="session")
def settings() -> Settings:
    return Settings()

@pytest.fixture()
def api(settings: Settings):
    client = BaseAPIClient(base_url=str(settings.base_url))
    yield client
    client.close()
