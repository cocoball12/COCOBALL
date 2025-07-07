# 디스코드 입장 관리 봇

새로운 멤버가 서버에 입장할 때 자동으로 비공개 방을 생성하고 관리하는 디스코드 봇입니다.

## 주요 기능

### 🚪 멤버 입장 시
- 라미 역할을 가진 관리자와 비공개 방 자동 생성
- 새 멤버는 음성채널만 볼 수 있도록 권한 설정
- 텍스트 채팅방은 비공개 방을 제외하고 모두 숨김

### 💬 안내 시스템
- **첫 번째 안내문**: 즉시 전송 (관리자 전용 버튼 포함)
- **두 번째 안내문**: 5초 후 전송 (본인 전용 버튼 포함)

### 🔘 버튼 기능

#### 관리자 전용 버튼 (라미 역할 필요)
- **삭제**: 비공개 방 삭제
- **보존**: 모든 채팅방 접근 권한 부여

#### 본인 전용 버튼
- **삭제**: 비공개 방 삭제
- **보존**: 성별에 따른 닉네임 변경
  - 남자 역할: `(단팥빵) 닉네임`
  - 여자 역할: `(메론빵) 닉네임`

## 설치 및 실행

### 1. 레포지토리 클론
```bash
git clone https://github.com/your-username/discord-entrance-bot.git
cd discord-entrance-bot
```

### 2. 필요한 패키지 설치
```bash
pip install -r requirements.txt
```

### 3. 환경 변수 설정
`.env.example`을 참고하여 `.env` 파일을 생성하고 봇 토큰을 입력하세요.

```bash
cp .env.example .env
# .env 파일을 열어서 DISCORD_TOKEN 값을 설정
```

### 4. 봇 실행
```bash
python bot.py
```

## 클라우드 배포

### Heroku 배포
1. **Heroku 앱 생성**
2. **환경 변수 설정**: Settings → Config Vars에서 `DISCORD_TOKEN` 추가
3. **깃허브 연결**: Deploy → Connect to GitHub
4. **자동 배포 활성화**: Enable Automatic Deploys
5. **Worker dyno 활성화**: Resources 탭에서 worker dyno ON

### 기타 클라우드 서비스
- **Railway**: 환경 변수에 `DISCORD_TOKEN` 설정
- **Render**: 환경 변수에 `DISCORD_TOKEN` 설정

## 서버 설정 요구사항

봇이 정상적으로 작동하려면 다음 역할이 서버에 있어야 합니다:

- **라미**: 관리자 역할
- **남자**: 남성 멤버 역할
- **여자**: 여성 멤버 역할

## 필요한 봇 권한

- 채널 관리
- 메시지 전송
- 멤버 관리
- 역할 관리
- 메시지 기록 보기

## 주의사항

- 봇은 새로운 멤버가 입장할 때만 작동합니다
- 비공개 방은 `입장-닉네임-날짜시간` 형식으로 생성됩니다
- 두 번째 안내문구는 코드에서 직접 수정할 수 있습니다

## 환경 변수 설정 방법

### 로컬 실행
`.env` 파일을 만들고 다음과 같이 설정:
```env
DISCORD_TOKEN=your_actual_bot_token_here
```

### 클라우드 배포
플랫폼의 환경 변수 설정에서 `DISCORD_TOKEN`을 추가하세요.

## 문제 해결

1. **봇이 반응하지 않는 경우**
   - 봇 토큰이 올바른지 확인
   - 봇이 서버에 초대되었는지 확인
   - 필요한 권한이 부여되었는지 확인

2. **역할 관련 오류**
   - 서버에 "라미", "남자", "여자" 역할이 존재하는지 확인
   - 역할 이름이 정확한지 확인 (대소문자 구분)

3. **권한 오류**
   - 봇의 역할이 관리하려는 역할보다 상위에 있는지 확인
   - 채널 관리, 멤버 관리 권한이 있는지 확인

## 파일 구조

```
discord-entrance-bot/
├── bot.py              # 메인 봇 코드
├── requirements.txt    # Python 패키지 목록
├── runtime.txt        # Python 버전 (Heroku용)
├── Procfile           # 실행 명령 (Heroku용)
├── .env.example       # 환경변수 예시
├── .gitignore         # Git 무시 파일
└── README.md          # 사용 설명서
```

## 라이선스

MIT License
