"""服务模块：钱与消费相关功能。"""
from typing import Dict, Any, List
from datetime import datetime


class BudgetService:
    """预算管理服务。"""

    def __init__(self) -> None:
        self._budgets: Dict[str, Any] = {}

    async def create_budget(
        self,
        user_id: str,
        category: str,
        amount: float,
        period: str,
    ) -> Dict[str, Any]:
        """创建预算。"""
        budget_id = f"{user_id}_{category}_{datetime.now().strftime('%Y%m')}"
        budget = {
            "id": budget_id,
            "user_id": user_id,
            "category": category,
            "amount": amount,
            "period": period,
            "remaining": amount,
            "created_at": datetime.now().isoformat(),
        }
        self._budgets[budget_id] = budget
        return budget

    async def check_budget_status(
        self, user_id: str, category: str
    ) -> Dict[str, Any]:
        """检查预算状态。"""
        budget_id = f"{user_id}_{category}_{datetime.now().strftime('%Y%m')}"
        if budget_id not in self._budgets:
            return {"status": "no_budget", "message": "暂无预算"}
        budget = self._budgets[budget_id]
        status = "ok"
        if budget["remaining"] <= 0:
            status = "exceeded"
        elif budget["remaining"] / budget["amount"] < 0.2:
            status = "low"
        return {"status": status, "remaining": budget["remaining"]}


class ShoppingComparisonService:
    """购物比较服务。"""

    def __init__(self) -> None:
        self._price_records: Dict[str, Any] = {}

    async def record_shopping(
        self, user_id: str, product: str, price: float, store: str
    ) -> Dict[str, Any]:
        """记录购物信息。"""
        record_id = f"{user_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        record = {
            "id": record_id,
            "user_id": user_id,
            "product": product,
            "price": price,
            "store": store,
            "time": datetime.now().isoformat(),
        }
        self._price_records[record_id] = record
        return record

    async def compare_products(
        self, user_id: str, product: str, category: str
    ) -> List[Dict[str, Any]]:
        """比较同类产品价格。"""
        similar_products = []
        for record in self._price_records.values():
            if record["user_id"] == user_id and record["product"] == product:
                similar_products.append(
                    {
                        "id": record["id"],
                        "product": record["product"],
                        "price": record["price"],
                        "store": record["store"],
                        "time": record["time"],
                    }
                )
        return sorted(similar_products, key=lambda x: x["price"])

    async def get_price_alert(
        self, user_id: str, threshold: float, category: str
    ) -> List[Dict[str, Any]]:
        """获取价格预警。"""
        alerts = []
        for record in self._price_records.values():
            if record["user_id"] == user_id and record["price"] <= threshold:
                alerts.append(
                    {
                        "id": record["id"],
                        "product": record["product"],
                        "price": record["price"],
                        "store": record["store"],
                        "alert_type": "price_below_threshold",
                    }
                )
        return alerts


# 全局服务实例
budget_service = BudgetService()
shopping_service = ShoppingComparisonService()