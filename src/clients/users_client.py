from typing import Any, Dict, List, Optional
from pydantic import BaseModel, EmailStr, Field
from src.clients.base_client import BaseAPIClient


class UserData(BaseModel):
    id: int | None = None
    email: EmailStr | None = None
    first_name: str | None = None
    last_name: str | None = None
    avatar: str | None = None


class CreateUserRequest(BaseModel):
    name: str
    job: str


class CreateUserResponse(BaseModel):
    name: str
    job: str
    id: str
    createdAt: str


class UpdateUserResponse(BaseModel):
    name: str | None = None
    job: str | None = None
    updatedAt: str


class ListUsersResponse(BaseModel):
    page: int
    per_page: int
    total: int
    total_pages: int
    data: List[UserData]


class UsersClient(BaseAPIClient):
    def list_users(self, page: int = 1) -> ListUsersResponse:
        r = self.get("/api/users", params={"page": page})
        r.raise_for_status()
        return ListUsersResponse(**r.json())

    def get_user(self, user_id: int) -> UserData:
        r = self.get(f"/api/users/{user_id}")
        r.raise_for_status()
        return UserData(**r.json().get("data", {}))

    def create_user(self, name: str, job: str) -> CreateUserResponse:
        payload = CreateUserRequest(name=name, job=job).model_dump()
        r = self.post("/api/users", json=payload)
        r.raise_for_status()
        return CreateUserResponse(**r.json())

    def update_user_put(self, user_id: int, name: str, job: str) -> UpdateUserResponse:
        r = self.put(f"/api/users/{user_id}", json={"name": name, "job": job})
        r.raise_for_status()
        return UpdateUserResponse(**r.json())

    def update_user_patch(self, user_id: int, fields: Dict[str, Any]) -> UpdateUserResponse:
        r = self.patch(f"/api/users/{user_id}", json=fields)
        r.raise_for_status()
        return UpdateUserResponse(**r.json())

    def delete_user(self, user_id: int) -> int:
        r = self.delete(f"/api/users/{user_id}")
        return r.status_code
