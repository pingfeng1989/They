from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """应用配置，支持环境变量和文件配置。"""

    project_name: str = "They"
    description: str = "个人生活管理 Agent"
    version: str = "0.1.0"
    # 后端
    python_version: str = ">=3.11"
    fastapi_app: str = "app.main:app"
    celery_app: str = "app.core.celery_app"
    redis_url: str = "redis://localhost:6379/0"
    postgresql_url: str = "postgresql+asyncpg://user:pass@localhost:5432/fp_db"
    qdrant_url: str = "qdrant://localhost:8645"
    # Hermes Agent 集成
    hermes_model: str = "hermes_agent"  # OpenRouter / OpenAI / Nous Portal / 自建
    hermes_skills_path: str = "/Users/ping/.claude/skills/hermes-agent"
    # 数据存储
    db_name: str = "fp_db"
    # 日历/邮箱 API
    google_calendar_api_key: str = ""
    gmail_api_token: str = ""
    shopping_api_token: str = ""
    apple_calendar_api_key: str = ""
    # 国内服务
    wechat_api_key: str = ""
    douban_api_key: str = ""
    # 预算/收费工具
    budgeting_enabled: bool = True
    # 主动提醒
    auto_reminder: bool = True
    # 部署
    docker_compose_file: str = "docker-compose.yml"
    cloud_deploy: bool = False

    class Config:
        env_prefix = "__"
        case_sensitive = True


settings = Settings()