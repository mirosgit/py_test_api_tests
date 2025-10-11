from pydantic import BaseModel
from typing import List, Optional
from src.clients.base_client import BaseAPIClient


class Resource(BaseModel):
    id: int
    name: str
    year: int
    color: str | None = None
    pantone_value: str | None = None


class ListResourcesResponse(BaseModel):
    page: int
    per_page: int
    total: int
    total_pages: int
    data: List[Resource]


class ResourcesClient(BaseAPIClient):
    def list_resources(self, page: int = 1) -> ListResourcesResponse:
        r = self.get("/api/unknown", params={"page": page})
        r.raise_for_status()
        return ListResourcesResponse(**r.json())

    def get_resource(self, resource_id: int) -> Resource:
        r = self.get(f"/api/unknown/{resource_id}")
        r.raise_for_status()
        return Resource(**r.json().get("data", {}))

    def delayed_users(self, delay_seconds: int = 3) -> int:
        r = self.get("/api/users", params={"delay": delay_seconds})
        r.raise_for_status()
        return r.status_code
