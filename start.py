#!/usr/bin/env python3
"""
Render 배포용 시작 파일
bot.py를 찾아서 실행합니다.
"""

import os
import sys
import subprocess

def find_and_run_bot():
    """bot.py 파일을 찾아서 실행"""
    
    # 가능한 bot.py 위치들
    possible_paths = [
        'bot.py',
        './bot.py',
        '/opt/render/project/src/bot.py',
        os.path.join(os.path.dirname(__file__), 'bot.py'),
        os.path.join(os.getcwd(), 'bot.py')
    ]
    
    print("=== Render Discord Bot 시작 ===")
    print(f"현재 작업 디렉토리: {os.getcwd()}")
    print(f"스크립트 위치: {os.path.dirname(__file__)}")
    print(f"파일 목록: {os.listdir('.')}")
    
    # bot.py 찾기
    bot_path = None
    for path in possible_paths:
        if os.path.exists(path):
            bot_path = path
            print(f"✅ bot.py 파일 발견: {path}")
            break
        else:
            print(f"❌ 경로 확인: {path}")
    
    if not bot_path:
        print("❌ bot.py 파일을 찾을 수 없습니다!")
        print("\n현재 디렉토리의 모든 .py 파일:")
        for root, dirs, files in os.walk('.'):
            for file in files:
                if file.endswith('.py'):
                    print(f"  - {os.path.join(root, file)}")
        sys.exit(1)
    
    # 환경 변수 확인
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        print("❌ DISCORD_TOKEN 환경변수가 설정되지 않았습니다!")
        sys.exit(1)
    else:
        print("✅ DISCORD_TOKEN 환경변수 확인됨")
    
    # bot.py 실행
    print(f"🚀 봇 실행: {bot_path}")
    try:
        # subprocess로 실행
        result = subprocess.run([sys.executable, bot_path], check=True)
        print(f"봇이 종료되었습니다. 종료 코드: {result.returncode}")
    except subprocess.CalledProcessError as e:
        print(f"❌ 봇 실행 실패: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n봇이 사용자에 의해 중단되었습니다.")
    except Exception as e:
        print(f"❌ 예상치 못한 오류: {e}")
        sys.exit(1)

if __name__ == "__main__":
    find_and_run_bot()
