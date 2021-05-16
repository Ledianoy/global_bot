from pydantic import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    bot_token: str = Field(..., env="BOT_TOKEN")
    database_url: str = Field(..., env="DATABASE_URL")
    index_path: str = Field(..., env="INDEX_PATH")
    admin_password: str = Field(..., env="PASSWORD")
    python_path: str = Field(..., env="PYTHONPATH")
    service_url: str = Field(..., env="SERVICE_URL")
    webhook_secret: str = Field(..., env="WEBHOOK_SECRET")
    debug: bool = Field(env="DEBUG", default=False)

    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"


class Pass(BaseSettings):
    password: str


settings: Settings = Settings()
