"""
Application configuration - single source of truth.

LOADING ORDER (highest priority wins):
    1. Real OS environment variables (set by Docker/K8s/systemd in production)
    2. The .env file (local development)
    3. Defaults declared in the Settings calss below

This means: in production you don't ship a .env file. You set real env vars.
In dev, .env is a convenience. The class defaults are last-resort fallbacks.

Why PYDANTIC BaseSettings:
- Type-safe: PORT becomes int, DEBUG becomes bool - no manual casting.
- Validates at startup: missing/malformed values crash immediatly, not later.
- Auto-loads from .env without extra code.
- IDE autocomplete: settings.DATABASE_URL is a know attribute not a dict key

WHY @lru_cache on get_settings():
- Settings() reads .env from dick and validates every field. Doing this on 
  every import is wasteful. lru_cache make it a singleton-per-process.
- Critically, this is still OVERRIDABLE in tests via dependency injection 
  or by clearing the cache - unlike a true module-level singleton. 
"""
from functools import lru_cache
from typing import Literal

from pydantic import Field, PostgresDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # --- How Pydantic loads this ---
    model_config = SettingsConfigDict(
        env_file=".env",            # Read from .env in the working directory
        env_file_encoding="utf-8",
        core_sensitive=True,         
        extra="ignore"              # Ignore unknown env vars instead of crashing
    )

    # --- Application ---
    ENVIRONMENT: Literal["development", "test", "staging", "production"] = "development"
    PROJECT_NAME: str = "My App"
    API_V1_PREFIX: str = "/api/v1"
    DEBUG: bool = False

    # --- Database ---
    DATABASE_URL: PostgresDsn
    DB_POOL_MIN_SIZE: int = Field(default=2, ge=1, le=100)
    DB_POOL_MAX_SIZE: int = Field(default=10, ge=1, le=100)
    DB_POOL_TIMEOUT: float = Field(default=30.0)

    # --- Security ---
    SECRET_KEY: str = Field(min_length=32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=60, ge=1)

    # --- CORS ---
    BACKEND_CORS_ORIGINS: list[str] = []

    # --- Logging ---
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    LOG_DIR: str = "logs"
    LOG_TO_FILE: bool = True

    # @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    # @classmethod
    # def parse_cors_origins(cls, v: str | list[str]) -> list[str]:
    #     if isinstance(v, str) and v:
    #         return [i.strip() for i in v.split(",") if i.stripe]
    #     return v
    
    @field_validator("DB_POOL_MAX_SIZE")
    @classmethod
    def max_must_exceed_min(cls, max: int, info) -> int:
        min = info.data.get("DB_POOL_MIN_SIZE")
        if max < min:
            raise ValueError(
                f"DB_POOL_MAX_SIZE ({max}) must be >= DB_POOL_MIN_SIZE"
            )
        return max
    
    @property
    def is_production(self) -> bool:
      return self.ENVIRONMENT == 'production'
    
    @property
    def is_test(self) -> bool:
      return self.ENVIRONMENT == 'test'

"""
lru_cache it tells python to create the below function only once, 
pull it from cache whenever you need it and no need to change the result.
When it get rexecuted:
 - different inputs
 - cache limit: with different inputs, different results gets saved in cache, setting
   limit @lru_cache(maxsize=128)tells python to drop the least recently
   used when the results saved exceed the limit (128 in this example)
 - manually clear cache: in this case getSettings().cache_clear()
 """
@lru_cache
def get_settings() -> Settings:
   return Settings()