# Blueprint: 晨间简报 (Morning Brief)

每天上午 8:00 执行一次，汇总当天的预算状态、日程安排、待办提醒和异常检测。作为“管家”模式的核心触发点。

## 元数据

| 字段 | 值 |
|------|-----|
| 名称 | `morning-brief` |
| 触发类型 | Schedule（定时） |
| 触发规则 | `0 8 * * *`（每天 08:00） |
| 交付目标 | `origin`（回到当前会话）或 `local` |
| 必需技能 | `lifestyle-reminder`, `budget-tracking`, `expense-tracking` |
| 可选技能 | `google-workspace`（日历）、`apple-calendar`（苹果日历） |

## `hermes cron create` 命令

```bash
hermes cron create "0 8 * * *" \
  "你是我的个人生活管理助手（管家模式）。请执行晨间简报任务：

1. 检查 `lifestyle-reminder` 技能：获取今天的所有待办提醒和即将到来的日程。
2. 检查 `budget-tracking` 技能：当前各预算类别的剩余额度和状态（ok/low/exceeded）。
3. 检查 `expense-tracking` 技能：昨天的支出汇总、本月累计支出。
4. 运行 `lifestyle-reminder` 的 anomaly check：检查预算超支、支出异常、账单到期等异常。
5. （可选）如果已接入 `google-workspace` 或 `apple-calendar`，抓取今日日历事件并整合。

输出格式（中文，简洁）：
- 【今日日程】...（若有接入日历）
- 【预算状态】...（各分类剩余/状态）
- 【近期支出】...（昨日/本月累计）
- 【异常提醒】...（如无异常则写“无异常”）
- 【建议动作】...（如超支提醒、账单到期等）

如果没有任何异常，句尾写 '✅ 一切正常，祝您今天愉快。'

若发现 budget status 为 'exceeded'，请用 '⚠️' 标记并优先提醒。

若日历/苹果日历技能未授权，请提示用户运行相应的 setup 脚本。" \
  --name "morning-brief" \
  --deliver origin \
  --skill lifestyle-reminder \
  --skill budget-tracking \
  --skill expense-tracking
```

## 使用前提

- `lifestyle_reminder.enabled=true`（`.env` / `config.yaml`）
- `budgeting.enabled=true`
- 若需要日历：预先完成 `google-workspace` 或 `apple-calendar` OAuth 授权

---

## Blueprint: 晚间复盘 (Evening Digest)

每天晚上 20:00，汇总今日花费、预算进度和明日提醒。

| 字段 | 值 |
|------|-----|
| 名称 | `evening-digest` |
| 触发规则 | `0 20 * * *`（每天 20:00） |
| 交付目标 | `origin` |
| 必需技能 | `expense-tracking`, `budget-tracking`, `lifestyle-reminder` |

```bash
hermes cron create "0 20 * * *" \
  "你是我的个人生活管理助手。请执行晚间复盘任务：

1. `expense-tracking`：统计今日支出总额、按类别分布、今日最大单笔支出。
2. `budget-tracking`：本月累计支出 / 预算总额、各分类剩余额度、是否有 'exceeded' 预算。
3. `lifestyle-reminder`：获取明日所有提醒和日程。
4. 若已接入 `google-workspace`/`apple-calendar`，抓取明日日历事件。

输出格式（中文）：
- 【今日支出】总额：¥xxx，按类别：...
- 【预算进度】本月累计 ¥xxx / ¥xxx，剩余 ¥xxx，状态：ok/low/exceeded
- 【明日日程】...（日程与提醒）
- 【异常检测】...（支出异常、预算超支提醒）

若无支出记录，写 '今日暂无支出记录'。" \
  --name "evening-digest" \
  --deliver origin \
  --skill expense-tracking \
  --skill budget-tracking \
  --skill lifestyle-reminder
```

---

## Blueprint: 周度复盘 (Weekly Review)

每周日 09:00，总结本周消费、预算执行率，规划下周。

| 字段 | 值 |
|------|-----|
| 名称 | `weekly-review` |
| 触发规则 | `0 9 * * 0`（每周日 09:00） |
| 交付目标 | `origin` |
| 必需技能 | `expense-tracking`, `budget-tracking`, `weekly-review-planning` |
| 可选技能 | `lifestyle-reminder` |

```bash
hermes cron create "0 9 * * 0" \
  "你是我的个人生活管理助手。请执行周度复盘任务：

1. `expense-tracking`：按周汇总支出（按日/按类别）、与上周对比、最大单笔支出。
2. `budget-tracking`：本周各预算类别执行率（已花/预算）、本月累计执行率。
3. `weekly-review-planning`：识别本周待办未完成事项、重复性模式。
4. `lifestyle-reminder`：下周重要日程与提醒预告。

输出格式（中文）：
- 【周度支出总览】本周总额：¥xxx，上周：¥xxx，同比变化...
- 【预算执行率】各分类：...，本月累计执行率：...
- 【支出模式】...（发现的重复支出、可优化点）
- 【下周展望】...（日程与提醒）

若无数据，提示用户先使用 `expense-tracking` 记录支出。" \
  --name "weekly-review" \
  --deliver origin \
  --skill expense-tracking \
  --skill budget-tracking \
  --skill weekly-review-planning \
  --skill lifestyle-reminder
```

---

## Blueprint: 异常检测 (Anomaly Detection)

每天 10:00 检查一次，在异常发生时主动推送。适合管家模式的“主动操心”特征。

| 字段 | 值 |
|------|-----|
| 名称 | `anomaly-detection` |
| 触发规则 | `0 10 * * *`（每天 10:00） |
| 交付目标 | `origin`（正常时） / `local`（静默失败） |
| 必需技能 | `budget-tracking`, `expense-tracking`, `lifestyle-reminder` |
| 推送策略 | 发现异常时主动提醒，无异常时不打扰（设 `failure-deliver local` 或在 prompt 内判断） |

```bash
hermes cron create "0 10 * * *" \
  "你是我的个人生活管理助手。请执行异常检测任务：

1. `budget-tracking`：检查是否有预算状态为 'exceeded'（超支）或 'low'（低余额）。
2. `expense-tracking`：今日支出是否异常（超出近 7 天日均的 1.5 倍）；是否有大额单笔支出（> ¥500）。
3. 检查近期是否有账单到期提醒。

输出规则：
- 若检测到任何异常（超支/低余额/支出异常/账单到期）：用 '⚠️ 异常提醒' 开头，列出每个异常及建议动作。
- 若无异常：静默输出 '[SILENT]'，不要发送任何正文。

请使用中文。若发现超支预算，建议动作包括 '降低其他分类预算' 或 '暂停非必要支出'。" \
  --name "anomaly-detection" \
  --deliver origin \
  --failure-deliver local \
  --skill budget-tracking \
  --skill expense-tracking \
  --skill lifestyle-reminder
```

---

## Blueprint: 价格预警检查 (Price Watch Tick)

每 6 小时检查一次追踪商品的价格变化。

| 字段 | 值 |
|------|-----|
| 名称 | `price-watch-tick` |
| 触发规则 | `every 6h`（每 6 小时） |
| 交付目标 | `origin` |
| 必需技能 | `shopping-comparison`（或内置 `product-price-monitor`） |

```bash
hermes cron create "every 6h" \
  "你是我的个人生活管理助手。请执行价格预警检查：

1. `shopping-comparison`：遍历所有追踪中的商品 watch 合约。
2. 对每个 watch，比对当前价格与阈值/基准价。
3. 若满足 alert 条件（价格跌破阈值/回到库存/超过上限）：用 '🛒 价格预警' 开头，说明商品、当前价格、阈值、建议动作。
4. 若无预警触发：静默输出 '[SILENT]'。

请使用中文。若商品已有最近一次预警（冷却期内），不重复提醒。" \
  --name "price-watch-tick" \
  --deliver origin \
  --skill shopping-comparison
```

---

## 查看/管理已创建的任务

```bash
# 查看所有定时任务
hermes cron list

# 查看任务执行历史
hermes cron runs

# 暂停某个任务
hermes cron pause <job-name>

# 移除某个任务
hermes cron remove <job-name>

# 立即执行一次（测试）
hermes cron run <job-name>
```
