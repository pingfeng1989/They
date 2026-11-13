# 外部 API 接入指南

本文档记录 They 生活管理 Agent 需要接入的外部服务及配置方法。

---

## 1. Google Workspace (Calendar / Gmail / Drive)

**对应 Skill**：`google-workspace`（内置 skill，skills.sh 托管）

**功能**：
- Google Calendar：读取日程、创建事件、搜索事件
- Gmail：搜索邮件、获取未读、日常摘要
- Drive / Docs / Sheets：文档操作

**所需凭据**：
1. **Google Cloud 项目**：启用 Calendar API、Gmail API
2. **OAuth 2.0 Client ID/Secret**：创建 "Web application" 类型
3. **重定向 URI**：`http://localhost:8080/callback`（或按 setup.py 提示）

**配置步骤**：

```bash
# 1. 检查当前授权状态
hermes run --skill google-workspace --prompt "Run the google-workspace setup.py --check"

# 2. 若未授权，提供 client_secret.json
#    先下载 Google Cloud Console 的 OAuth client secret
hermes run --skill google-workspace --prompt "Run the google-workspace setup.py --client-secret /path/to/client_secret.json"

# 3. 获取授权 URL
hermes run --skill google-workspace --prompt "Run the google-workspace setup.py --auth-url"
# 打开打印的 URL，在浏览器授权，复制授权码

# 4. 提交授权码
hermes run --skill google-workspace --prompt "Run the google-workspace setup.py --auth-code <AUTH_CODE>"

# 5. 验证
hermes run --skill google-workspace --prompt "Run the google-workspace setup.py --check"
```

**文件存储位置**：
- `~/.hermes/google_token.json` — OAuth token（自动刷新）
- `~/.hermes/google_client_secret.json` — Client secret

**验证**：
```bash
# 测试日历读取
hermes run --skill google-workspace --prompt "List my calendars"

# 测试 Gmail
hermes run --skill google-workspace --prompt "Show my unread emails from last 24 hours"
```

---

## 2. Apple 生态 (Calendar / Reminders / Notes / iMessage)

**对应 Skills**：
- `apple-calendar` — macOS Calendar.app CRUD
- `apple-reminders` — Reminders.app
- `apple-notes` — Notes.app
- `imessage` — iMessage 发送/读取

**平台要求**：macOS（AppleScript 依赖）

**配置**：
- **无需额外配置** — macOS 原生权限即可
- 首次运行时，系统会弹窗询问 "允许 Hermes 访问 Calendar/Reminders/Notes"
- 点击"允许"即可

**验证**：
```bash
# 列出所有日历
hermes run --skill apple-calendar --prompt "List all calendars"

# 列出未来 7 天事件
hermes run --skill apple-calendar --prompt "List events for the next 7 days"

# 创建测试事件
hermes run --skill apple-calendar --prompt "Create an event 'Test' in 'Home' calendar from '2026-11-14 10:00' to '2026-11-14 11:00'"

# 测试提醒事项
hermes run --skill apple-reminders --prompt "List all reminders"

# 测试 Notes
hermes run --skill apple-notes --prompt "List all notes"
```

**权限问题排查**：
```bash
# macOS 系统偏好设置 → 安全性与隐私 → 隐私 → 日历/提醒事项/备忘录
# 确保 "hermes" 或 "Terminal" 或 "Python" 在列表中且已勾选
```

---

## 3. 国内服务 (微信 / 支付宝 / 淘宝 / 京东)

**现状**：Hermes 无现成 skill

**适配方案**：

| 服务 | 接入方式 | 难度 | 备注 |
|------|----------|------|------|
| 微信 | 官方无公开 API，需自研 | 高 | 可通过企业微信 API、微信小程序云开发、或第三方网关 |
| 支付宝 | 开放平台 API | 中 | 需商家入驻、密钥配置 |
| 淘宝/京东 | 商家开放平台 API | 中 | 需商家权限，普通用户无 API |
| 钉钉/飞书 | 企业开放平台 | 中 | 企业级接入 |

**短期替代方案**：
1. **手动记录** → `expense-tracking` skill 手动输入
2. **导出 CSV** → 银行/支付宝/微信账单导出 CSV → 批量导入
3. **邮件解析** → 通过 Gmail/Outlook 解析账单邮件 → 自动提取
4. **MCP 适配器** → 编写 MCP server 暴露国内服务 API → Hermes 加载

**预留接口设计**：
```python
# scripts/domestic_adapters/__init__.py
# 统一接口：record_expense(amount, category, note, source, raw_data)

class WeChatAdapter:
    """微信账单解析：解析微信账单 CSV/Excel"""
    
class AlipayAdapter:
    """支付宝账单解析：解析支付宝账单 CSV/Excel"""

class BankStatementAdapter:
    """银行账单解析：通用银行流水 CSV/Excel"""
```

**当前可行路径**：
```bash
# 1. 微信/支付宝 APP 导出账单 CSV
# 2. 使用 expense-tracking 批量导入（待实现 batch import）
# 3. 或手动通过对话录入："记录一笔支出：¥45，餐饮，微信支付，备注：午餐"
```

---

## 4. 其他有用的内置 Skills

| Skill | 用途 | 配置 |
|-------|------|------|
| `product-price-monitor` | 价格监控 | 无需配置，直接用 |
| `weekly-review-planning` | 周度复盘 | 无需配置 |
| `email-inbox-triage` | 邮箱分拣 | 需 IMAP 配置 |
| `maps` | 地图/导航 | 无需配置 |
| `pdf` | PDF 处理 | 无需配置 |

---

## 5. 完整验证清单

运行以下命令验证所有外部接口：

```bash
#!/bin/bash
# scripts/verify-external-apis.sh

echo "=== 验证 Hermes Runtime ==="
hermes --version

echo "=== 验证 Project Skills ==="
hermes skills list --enabled-only | grep -E "budget|expense|shopping|lifestyle"

echo "=== 验证 Google Workspace ==="
hermes run --skill google-workspace --prompt "Run setup.py --check" || echo "Google Workspace 未授权，运行 setup 步骤"

echo "=== 验证 Apple Calendar ==="
hermes run --skill apple-calendar --prompt "List all calendars" || echo "Apple Calendar 权限可能缺失"

echo "=== 验证内置 Skills ==="
for skill in product-price-monitor weekly-review-planning; do
  hermes run --skill $skill --prompt "Describe your capabilities" 2>/dev/null || echo "$skill 未就绪"
done

echo "=== 完成 ==="
```

---

## 6. 配置文件位置汇总

| 文件 | 路径 | 说明 |
|------|------|------|
| Hermes 主配置 | `~/.hermes/config.yaml` | 全局行为配置 |
| 环境变量 | `~/.hermes/.env` | Secrets（API keys, tokens） |
| Google Token | `~/.hermes/google_token.json` | OAuth token |
| Google Client Secret | `~/.hermes/google_client_secret.json` | Client secret |
| Project Skills | `./.hermes/skills/` | 仓库级技能（优先级最高） |
| Profile Skills | `~/.hermes/skills/` | 用户级技能 |
| Cron Jobs | `~/.hermes/cron/` | 定时任务状态 |