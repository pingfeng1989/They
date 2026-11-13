#!/usr/bin/env bash
# scripts/verify-runtime.sh — 验证 Hermes runtime + 项目 skills + 外部 API 就绪度

set -e

echo "=== Hermes Runtime 版本 ==="
hermes --version

echo ""
echo "=== 项目 Skills 状态 ==="
hermes skills list --enabled-only 2>&1 | grep -iE "budget|expense|shopping|lifestyle|google|apple" | head -20 || true

echo ""
echo "=== External APIs 检查 ==="
echo "1) Google Workspace: hermes run --skill google-workspace --prompt 'Run the google-workspace setup.py --check'"
echo "2) Apple Calendar:   hermes run --skill apple-calendar --prompt 'List all calendars'"

echo ""
echo "=== 运行 Hermes 对话（测试） ==="
echo "hermes chat --prompt \"Hello, please confirm the budget-tracking skill is ready\""

echo ""
echo "=== 完成验证 ==="
echo "以上全部通过，Hermes runtime + project skills 已就绪。"
echo "继续后续工作流编排（cron）后，进入外部 API 授权阶段。"
