#!/bin/bash

echo "=== Render Discord Bot 시작 ==="
echo "현재 디렉토리: $(pwd)"
echo "파일 목록:"
ls -la

# 가능한 경로들 확인
echo "=== 파일 찾기 ==="
if [ -f "bot.py" ]; then
    echo "✅ bot.py 발견: $(pwd)/bot.py"
    python bot.py
elif [ -f "/opt/render/project/src/bot.py" ]; then
    echo "✅ bot.py 발견: /opt/render/project/src/bot.py"
    cd /opt/render/project/src && python bot.py
else
    echo "❌ bot.py 찾기 실패, 전체 검색 중..."
    find /opt/render/project -name "bot.py" -type f
    BOT_PATH=$(find /opt/render/project -name "bot.py" -type f | head -1)
    if [ -n "$BOT_PATH" ]; then
        echo "✅ bot.py 발견: $BOT_PATH"
        python "$BOT_PATH"
    else
        echo "❌ bot.py 파일을 찾을 수 없습니다!"
        exit 1
    fi
fi
