# They — 个人生活管理 Agent

基于 [Hermes Agent](https://github.com/NousResearch/hermes-agent) 的个人生活管理助手。

> **MVP 聚焦「钱与消费」** 领域：记账、购物比价、账单管理、预算控制，支持主动提醒与自主安排。

## 核心定位

| 维度 | 选择 |
|------|------|
| **使用场景** | 手机 + 电脑双端同步，随时随地管理生活事务 |
| **角色定位** | 平时听指令执行，关键时刻主动提醒、主动规划 |
| **数据接入** | Google 全家桶、Apple 生态、国内服务（微信/支付宝/淘宝等） |
| **部署** | 先本地跑通，后续可上云常驻 |

## 架构原理

> **方案 A：基于 Hermes Agent 改造（在边缘加 skill）**

本项目**不 fork Hermes core**，而是利用 Hermes 的 **project-level skills** 机制（`HERMES_HOME/skills/` + project `./.hermes/skills/`），在 Hermes 运行时之上添加生活管理领域技能。

Hermes 提供的核心能力（直接复用）：
- **学习循环** — Agent 从经验创建技能、自改进、持久化知识、跨会话记忆
- **多平台网关** — Telegram/Discord/Slack/WhatsApp/Signal + CLI
- **cron 调度** — 内置定时自动化
- **子代理委派** — 并行子 Agent 工作流
- **多模型供应商** — Nous Portal/OpenRouter/OpenAI/自定义端点
- **6 种终端后端** — 本地/Docker/SSH/Modal/Daytona/Vercel Sandbox

## 技能

| 技能 | 说明 |
|------|------|
| `budget-tracking` | 创建和管理预算，按类别/周期跟踪支出 |
| `expense-tracking` | 记录消费、分类、生成日报/周报/月报 |
| `shopping-comparison` | 记录商品价格、比较不同平台、价格预警 |
| `lifestyle-reminder` | 定时提醒、每日汇报、异常检测、主动安排 |

## 技术栈

| 层级 | 技术 |
|------|------|
| **Agent 运行时** | Hermes Agent (Python 3.11+ / OpenRouter / OpenAI / Nous) |
| **技能框架** | Hermes SKILL.md 标准 (YAML frontmatter + 章节结构) |
| **调度** | Hermes 内置 cron (`cronjob()`) |
| **记忆/学习** | Hermes state (FTS5 + LLM 摘要 + 跨会话检索) |
| **部署** | Docker Compose / 本地 CLI / 云端 VPS |
| **数据存储** | 本地文件 (`~/.hermes/`) + 可选 Qdrant 向量存储 |

## 快速开始

```bash
# 1. 克隆仓库
git clone https://github.com/pingfeng1989/They.git
cd They

# 2. 复制环境变量模板并填入 API Key
cp .env.example .env
# 编辑 .env，填入 OPENROUTER_API_KEY 等

# 3. 启动 Hermes 运行时（Docker Compose）
docker compose up -d

# 4. 或直接使用本地 CLI（推荐开发阶段）
# 安装 Hermes: 详见 https://hermes-agent.nousresearch.com/docs/getting-started/installation
hermes
```

服务启动后：

- Web 仪表板：`http://localhost:8000`（如果启用 gateway）
- CLI：直接运行 `hermes`
- 技能列表：`hermes skills list`

## 项目结构

```
They/
├── .github/                # GitHub Actions 工作流
├── .hermes/skills/         # ← 项目技能目录（Hermes 自动发现，最高优先级）
│   ├── budget-tracking/
│   ├── expense-tracking/
│   ├── shopping-comparison/
│   └── lifestyle-reminder/
├── .agents/skills/         # 备用技能目录（Hermes 也会扫描）
├── docs/                   # 项目文档
├── docker-compose.yml      # Docker Compose 部署
├── .env.example            # 环境变量模板（secrets only）
├── README.md               # 项目说明
└── LICENSE                 # MIT License
```

## 核心概念

### Project-level skills

Hermes 支持 **project-level skills**（`get_project_skills_dirs()`），目录在：
- `./.hermes/skills/`  (项目根目录下)
- `./.agents/skills/`  (备用)

Hermes 启动时会自动扫描并加载这些技能，**优先级最高**。因此本项目只需在仓库中放置 `.hermes/skills/` 即可。

### Skills 配置

技能配置通过 `config.yaml` 中的 `skills.config.<key>` 注入，在 `.env.example` 中已标记：

```yaml
skills:
  config:
    budgeting.enabled: true
    expense_tracking.enabled: true
    shopping_comparison.enabled: true
    lifestyle_reminder.enabled: true
    lifestyle_reminder.morning_time: "08:00"
    lifestyle_reminder.evening_time: "20:00"
```

## 数据存储

技能运行时产生的数据存储在 `HERMES_HOME` 下（默认 `~/.hermes/`）：

```
~/.hermes/
├── budgets/               # budget-tracking
├── expenses/              # expense-tracking
├── price-watches/         # shopping-comparison
├── reminders/             # lifestyle-reminder
├── skills/                # Hermes skills 缓存
├── memory/                # 跨会话记忆
├── cron/                  # cron job 状态
└── logs/                  # 日志
```

## 外部 API 集成（后续扩展）

| 生态 | 状态 | 说明 |
|------|------|------|
| Google Calendar/Gmail | 🔜 计划中 | 通过 `google-workspace` skill |
| Apple Calendar/Reminders | 🔜 计划中 | macOS 原生集成 |
| 国内服务 (微信/支付宝/淘宝) | 🔜 计划中 | 需自研或 MCP 适配 |

## 开发路线图

- [x] 项目初始化与目录结构
- [x] 4 个核心技能 SKILL.md（budget, expense, shopping, reminder）
- [ ] 阶段 1 (1-2月)：Hermes runtime + skills 落地 + 本地验证
- [ ] 阶段 2 (3-4月)：外部 API 接入 + 工作流编排 + 多端同步
- [ ] 阶段 3 (5-6月)：多 Agent 协作 + 插件扩展 + 公开发布

## 许可证

MIT License — 详见 [LICENSE](LICENSE)。

---

> **为什么选择 Hermes 作为基础？**
> - **学习循环**是个人 Agent 的核心护城河：它会从你的使用中学习、自动生成技能、持续改进。
> - **狭腰设计**：核心稳定，能力在边缘扩展，维护成本极低。
> - **原生多平台**：手机、电脑、Telegram、桌面端一次配置，到处可用。