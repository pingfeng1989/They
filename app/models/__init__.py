"""数据库模型定义。"""
from sqlalchemy import Column, String, Float, DateTime, Text, BigInteger
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class UserBudget(Base):
    """预算表。"""
    __tablename__ = "user_budgets"

    id = Column(String, primary_key=True)
    user_id = Column(String, index=True)
    category = Column(String)
    amount = Column(Float)
    period = Column(String)
    remaining = Column(Float)
    created_at = Column(DateTime)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "category": self.category,
            "amount": self.amount,
            "period": self.period,
            "remaining": self.remaining,
            "created_at": self.created_at,
        }


class ShoppingRecord(Base):
    """购物记录表。"""
    __tablename__ = "shopping_records"

    id = Column(String, primary_key=True)
    user_id = Column(String, index=True)
    product = Column(String)
    price = Column(Float)
    store = Column(String)
    category = Column(String)
    time = Column(DateTime)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "product": self.product,
            "price": self.price,
            "store": self.store,
            "category": self.category,
            "time": self.time,
        }


class UserSettings(Base):
    """用户设置表。"""
    __tablename__ = "user_settings"

    id = Column(String, primary_key=True)
    user_id = Column(String, unique=True, index=True)
    preferences = Column(Text)
    notifications = Column(String)
    language = Column(String, default="zh-CN")
    timezone = Column(String, default="Asia/Shanghai")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "preferences": self.preferences,
            "notifications": self.notifications,
            "language": self.language,
            "timezone": self.timezone,
        }


class ConversationHistory(Base):
    """对话历史表。"""
    __tablename__ = "conversation_history"

    id = Column(String, primary_key=True)
    user_id = Column(String, index=True)
    message = Column(Text)
    response = Column(Text)
    timestamp = Column(DateTime)
    intent = Column(String)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "message": self.message,
            "response": self.response,
            "timestamp": self.timestamp,
            "intent": self.intent,
        }


class SystemLogs(Base):
    """系统日志表。"""
    __tablename__ = "system_logs"

    id = Column(String, primary_key=True)
    level = Column(String)
    message = Column(Text)
    user_id = Column(String, index=True)
    timestamp = Column(DateTime)
    metadata = Column(Text)

    def to_dict(self) -> dict:
        return {
            "id": self.id,\n            "level": self.level,
            "message": self.message,
            "user_id": self.user_id,
            "timestamp": self.timestamp,
            "metadata": self.metadata,
        }
