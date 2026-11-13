"""FastAPI application entry point for FP-Agent."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import api_router
from app.core.config import settings

app = FastAPI(
    title=settings.project_name,
    description="基于 Hermes Agent 的个人生活管理助手",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS 配置（允许移动端 + 桌面端访问）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册所有 API 路由
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root():
    """根路由，返回服务基本信息。"""
    return {
        "service": settings.project_name,
        "version": "0.1.0",
        "description": settings.description,
        "docs": "/docs",
    }


@app.get("/health")
async def health():
    """健康检查接口。"""
    return {"status": "ok", "version": "0.1.0"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )