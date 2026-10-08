"""Sample-only configuration, isolated from the original project's secrets."""
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    REDIS_URL: str = "redis://localhost:6379/0"
    CACHE_TTL_SECONDS: int = Field(default=300, gt=0)
    CACHE_NULL_TTL_SECONDS: int = Field(default=30, gt=0)
    CACHE_TTL_JITTER_SECONDS: int = Field(default=60, ge=0)
    CACHE_LOCK_TTL_SECONDS: int = Field(default=10, gt=0)
    CACHE_LOCK_WAIT_MILLISECONDS: int = Field(default=300, ge=0)


settings = Settings()
