from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    anthropic_api_key: str
    voyage_api_key: str | None = None
    supabase_url: str
    supabase_service_key: str
    supabase_db_url: str
    exa_api_key: str | None = None
    tavily_api_key: str | None = None
    github_token: str | None = None
    env: str = "development"
    allow_origins: str = "http://localhost:3000"

    @property
    def cors_origins(self) -> list[str]:
        return [o.strip() for o in self.allow_origins.split(",")]

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()  # type: ignore[call-arg]
