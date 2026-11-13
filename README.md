# They — 个人生活管理 Agent

基于 [Hermes Agent](https://github.com/NousResearch/hermes-agent) 架构的个人生活管理助手。

> MVP 聚焦 **"钱与消费"** 领域：记账、购物比价、账单管理、预算控制，支持主动提醒与自主安排。

## 核心定位

- **使用场景**：手机 + 电脑双端同步，随时随地管理生活事务
- **角色定位**：平时听指令执行，关键时刻主动提醒、主动规划
- **数据接入**：Google 全家桶、Apple 生态、国内服务（微信/支付宝/淘宝等）
- **部署**：先本地跑通，后续可上云常驻

## 技术栈

| 层级 | 技术 |
|------|------|
| 后端 | Python 3.11+ / FastAPI / SQLAlchemy / Pydantic |
| 异步任务 | Celery + Redis |
| 向量数据库 | Qdrant |
| 关系数据库 | PostgreSQL |
| 前端 | React 18 / TypeScript / Ant Design |
| Agent 基础 | Hermes Agent (学习循环、记忆模型、cron调度) |
| 容器化 | Docker + Docker Compose |

## 项目结构

```
They/
├── app/
│   ├── api/          # FastAPI 路由
│   ├── core/         # Agent 引擎、配置
│   ├── models/       # 数据库模型
│   ├── schemas/      # Pydantic 数据模型
│   ├── services/     # 业务服务（预算、比价）
│   └── utils/        # 工具函数
├── docker/           # Dockerfile
├── docs/             # 项目文档
├── tests/            # 测试用例
├── scripts/          # 部署脚本
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```

## 快速开始

```bash
git clone https://github.com/pingfeng1989/They.git
cd They
cp .env.example .env
# 填入你的 LLM API Key（OpenRouter / OpenAI / Nous Portal 等）
docker compose up -d
```

服务启动后：

- API 文档：http://localhost:8000/docs
- 健康检查：http://localhost:8000/health

## 开发路线图

- [x] 项目初始化与目录结构
- [ ] 阶段 1（第 1-2 个月）：钱与消费 MVP + 基础 Agent 引擎
- [ ] 阶段 2（第 3-4 个月）：工作流编排 + 多端同步
- [ ] 阶段 3（第 5-6 个月）：多 Agent 协作 + 插件扩展

## 许可证

MIT License