from pydantic import BaseModel
from src.clients.base_client import BaseAPIClient


class LoginRequest(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    token: str


class RegisterRequest(BaseModel):
    email: str
    password: str


class RegisterResponse(BaseModel):
    id: int
    token: str


class AuthClient(BaseAPIClient):
    def login(self, email: str, password: str) -> LoginResponse:
        payload = LoginRequest(email=email, password=password).model_dump()
        r = self.post("/api/login", json=payload)
        r.raise_for_status()
        return LoginResponse(**r.json())

    def register(self, email: str, password: str) -> RegisterResponse:
        payload = RegisterRequest(email=email, password=password).model_dump()
        r = self.post("/api/register", json=payload)
        r.raise_for_status()
        return RegisterResponse(**r.json())
