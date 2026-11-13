#!/usr/bin/env bash
# scripts/setup-external-apis.sh — Hermes Agent 外部 API 接入指引执行器

set -e

echo "=== Hermes Agent 外部 API 接入 引导 ==="
echo ""
echo "本脚本帮助你完成以下任务："
echo "1. Google Workspace OAuth2 授权（google-workspace skill）"
echo "2. Apple Calendar/Reminders/Notes/iMessage（macOS 本机）"
echo "3. 国内服务适配（待自研 MCP 或第三方网关）"

read -p "请选择要配置的生态系统（comma-separated, 空格分隔）: " ECOSYSTEMS

case "$ECOSYSTEMS" in
    google,gws)  # Google Workspace
        echo "--- Google Workspace ---"
        echo "运行 setup.py --check 验证当前授权状态:"
        hermes run --skill google-workspace --prompt "Run the google-workspace setup.py --check"
        read -p "Google OAuth2 token 已存在? (y/n): " GOOGLE_TOKEN
        if [[ $GOOGLE_TOKEN != "y" ]]; then
            echo "请在 ~/.hermes/google_token.json 中添加你的 Google OAuth2 token（自动刷新）。"
            echo "运行: hermes run --skill google-workspace --prompt 'Run the google-workspace setup.py --client-secret /path/to/client_secret.json'"
        fi
        ;;
    apple)  # Apple 生态
        echo "--- Apple 生态 ---"
        echo "Apple Calendar/Reminders/Notes/iMessage 已支持 macOS 本机，无需额外配置。"
        echo "首次运行时，系统会弹窗询问是否允许 Hermes 访问这些 App。点击 '允许' 即可。"
        ;;
    *)
        echo "未识别的生态系统：$ECOSYSTEMS"
        echo "可选：提供微信/支付宝/淘宝等国内服务的 MCP 适配器或自研 API 接口。"
        ;;
esac

echo ""
echo "=== 下一步 ==="
echo "1. 填写 .env.example 中的 API key 占位符"
echo "2. 运行: docker compose up -d"
echo "3. 启动 Hermes: hermes"
echo "4. 检查技能加载: hermes skills list"