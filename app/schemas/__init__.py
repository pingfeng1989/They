"""Pydantic 数据模型定义。"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class BudgetCreate(BaseModel):
    """创建预算请求。"""
    category: str = Field(..., description="预算分类，如：食品、交通、娱乐")
    amount: float = Field(..., gt=0, description="预算金额")
    period: str = Field(default="monthly", description="周期：weekly/monthly/yearly")


class BudgetResponse(BaseModel):
    """预算响应。"""
    id: str
    category: str
    amount: float
    remaining: float
    period: str
    created_at: str
    class Config:
        from_attributes = True


class ShoppingRecordCreate(BaseModel):
    """购物记录请求。"""
    product: str = Field(..., description="商品名称")
    price: float = Field(..., gt=0, description="购买价格")
    store: str = Field(..., description="购买店铺/平台")
    category: str = Field(default="general", description="商品分类")


class ShoppingRecordResponse(BaseModel):
    """购物记录响应。"""
    id: str
    product: str
    price: float
    store: str
    category: str
    time: str
    class Config:
        from_attributes = True


class ComparisonResult(BaseModel):
    """比价结果。"""
    product: str
    stores: List[dict]
    cheapest: Optional[dict] = None
    average_price: float


class PriceAlert(BaseModel):
    """价格预警。"""
    product: str
    current_price: float
    threshold: float
    store: str
    alert_type: str


class AgentRequest(BaseModel):
    """Agent 请求。"""
    user_id: str = Field(..., description="用户ID")
    message: str = Field(..., description="用户输入")
    context: Optional[dict] = None


class AgentResponse(BaseModel):
    """Agent 响应。"""
    success: bool
    data: Optional[dict] = None
    message: str
    actions_taken: List[str] = []


class HealthResponse(BaseModel):
    """健康检查响应。"""
    status: str = "ok"
    version: str = "0.1.0"