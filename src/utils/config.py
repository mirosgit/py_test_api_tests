from typing import Literal, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyUrl


class Settings(BaseSettings):
    base_url: AnyUrl
    timeout: int = 20
    retries: int = 2
    x_api_key: Optional[str] = None
    bearer_token: Optional[str] = None
    env: Literal["local", "qa", "stage", "prod"] = "local"

    model_config = SettingsConfigDict(env_file=".env", env_prefix="API_", extra="ignore")


settings = Settings()
