"""API 路由文件。"""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import List, Optional
from app.schemas import (
    AgentRequest,
    AgentResponse,
    BudgetCreate,
    BudgetResponse,
    ShoppingRecordCreate,
    ShoppingRecordResponse,
    ComparisonResult,
    PriceAlert,
    HealthResponse,
)
from app.services import budget_service, shopping_service
from app.core.agent import engine

router = APIRouter(prefix="/api/v1")

# 预算管理端点
@router.post("/budgets")
async def create_budget(
    budget: BudgetCreate, user_id: str = "demo_user"
) -> BudgetResponse:
    """创建预算。"""
    result = await budget_service.create_budget(
        user_id=user_id,
        category=budget.category,
        amount=budget.amount,
        period=budget.period,
    )
    return BudgetResponse(**result)

@router.get("/budgets")
async def get_budgets(user_id: str = "demo_user") -> List[BudgetResponse]:
    """获取预算列表。"""
    # TODO: 实现数据库查询
    return []

@router.get("/budgets/{category}")
async def check_budget_status(
    category: str, user_id: str = "demo_user"
) -> dict:
    """检查预算状态。"""
    return await budget_service.check_budget_status(user_id, category)

# 购物管理端点
@router.post("/shopping")
async def record_shopping(
    shopping: ShoppingRecordCreate, user_id: str = "demo_user"
) -> ShoppingRecordResponse:
    """记录购物信息。"""
    result = await shopping_service.record_shopping(
        user_id=user_id,
        product=shopping.product,
        price=shopping.price,
        store=shopping.store,
        category=shopping.category,
    )
    return ShoppingRecordResponse(**result)

@router.get("/shopping/compare")
async def compare_products(
    user_id: str = "demo_user", product: Optional[str] = None
) -> List[ComparisonResult]:
    """比较产品价格。"""
    # TODO: 实现按产品分类比较
    return []

@router.get("/shopping/alerts")
async def get_price_alerts(
    user_id: str = "demo_user", threshold: float = 0.0
) -> List[PriceAlert]:
    """获取价格预警。"""
    return await shopping_service.get_price_alert(user_id, threshold, "general")

# Agent API 端点
@router.post("/agent/chat")
async def chat_with_agent(
    request: AgentRequest,
    background_tasks: BackgroundTasks,
) -> AgentResponse:
    """与 Agent 对话。"""
    try:
        # 记录对话历史
        background_tasks.add_task(
            log_conversation,
            request.user_id,
            request.message,
            "agent",
        )
        # 利用 Agent 引擎处理
        result = await engine.process(request.message)
        return AgentResponse(
            success=True,
            data=result,
            message="请求处理成功",
            actions_taken=["processed_request", "recorded_conversation"],
        )
    except Exception as e:
        return AgentResponse(
            success=False,
            data=None,
            message=f"请求处理失败: {str(e)}",
            actions_taken=[],
        )

# 辅助函数
def log_conversation(user_id: str, message: str, response: str, intent: str) -> None:
    """记录对话历史。"""
    # TODO: 实现对话历史记录
    pass

@router.get("/health")
async def health() -> HealthResponse:
    """健康检查。"""
    return HealthResponse()

@router.get("/stats")
async def get_stats(user_id: str = "demo_user") -> dict:
    """获取用户统计信息。"""
    budgets = await get_budgets(user_id)
    shopping = await shopping_service.record_shopping(
        user_id=user_id,
        product="test",
        price=100.0,
        store="test_store",
        category="general",
    )
    return {
        "total_budgets": len(budgets),
        "total_shopping_records": 1,
        "total_spent": 100.0,
        "average_transaction": 100.0,
        "categories": ["test"],
    }