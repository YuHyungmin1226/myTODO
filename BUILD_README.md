# MyTODO 애플리케이션 빌드 가이드 🚀

이 가이드는 MyTODO 할 일 목록 애플리케이션을 Windows와 macOS용 실행 파일로 빌드하는 방법을 설명합니다.

## 📋 사전 요구사항

### Windows
- Python 3.8 이상
- pip (Python 패키지 관리자)

### macOS
- Python 3.8 이상
- pip (Python 패키지 관리자)
- Xcode Command Line Tools (선택사항)

## 🔧 빌드 방법

### Windows에서 빌드

1. **패키지 설치**
   ```bash
   pip install -r requirements.txt
   ```

2. **빌드 실행**
   ```bash
   python build.py
   ```

3. **결과 확인**
   - `dist/MyTODO.exe` 파일이 생성됩니다
   - 파일 크기: 약 15MB

### macOS에서 빌드

1. **패키지 설치**
   ```bash
   pip install -r requirements.txt
   ```

2. **빌드 실행**
   ```bash
   python build_macos.py
   ```

3. **결과 확인**
   - `dist/MyTODO` 실행 파일이 생성됩니다
   - `dist/MyTODO.app` 앱 번들도 생성됩니다 (선택사항)

## 📦 배포 방법

### Windows 배포

1. **단일 파일 배포**
   - `dist/MyTODO.exe` 파일만 복사
   - 어디든 복사하여 실행 가능

2. **USB 배포**
   - `MyTODO.exe`를 USB에 복사
   - 다른 Windows PC에서 실행 가능

### macOS 배포

1. **실행 파일 배포**
   - `dist/MyTODO` 파일을 복사
   - 터미널에서 `./MyTODO` 실행

2. **앱 번들 배포**
   - `dist/MyTODO.app`을 Applications 폴더에 복사
   - Launchpad에서 실행 가능

## 🚀 사용 방법

### 첫 실행

1. **실행 파일 더블클릭**
2. **콘솔 창에서 확인**
   ```
   ==================================================
   MyTODO 할 일 목록 애플리케이션
   ==================================================
   서버가 시작되었습니다!
   브라우저에서 http://localhost:5000 으로 접속하세요
   종료하려면 Ctrl+C를 누르세요
   ==================================================
   ```

3. **브라우저 접속**
   - http://localhost:5000 으로 접속
   - 회원가입 후 로그인하여 사용

### 데이터 관리

- **데이터베이스**: `todo.db` 파일이 자동 생성됩니다
- **백업**: `todo.db` 파일을 복사하여 백업
- **복원**: 백업한 `todo.db` 파일을 실행 파일과 같은 폴더에 복사

## 🔒 보안 설정

### Windows
- Windows Defender에서 실행 허용
- 필요시 "추가 정보" → "실행" 클릭

### macOS
- 시스템 환경설정 → 보안 및 개인 정보 보호
- "확인되지 않은 개발자" 허용
- 또는 터미널에서 `sudo spctl --master-disable` (관리자 권한 필요)

## 🐛 문제 해결

### 빌드 실패
1. **Python 버전 확인**: Python 3.8 이상 필요
2. **패키지 재설치**: `pip install --upgrade -r requirements.txt`
3. **캐시 정리**: `pyinstaller --clean app.py`

### 실행 실패
1. **포트 충돌**: 다른 프로그램이 5000번 포트 사용 중
2. **방화벽**: Windows 방화벽에서 허용
3. **권한**: 관리자 권한으로 실행

### 데이터 손실
1. **백업 복원**: `todo.db` 파일 복사
2. **재설치**: 실행 파일 재다운로드

## 📁 파일 구조

```
MyTODO/
├── app.py              # 메인 애플리케이션
├── build.py            # Windows 빌드 스크립트
├── build_macos.py      # macOS 빌드 스크립트
├── requirements.txt    # Python 패키지 목록
├── templates/          # HTML 템플릿
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   └── dashboard.html
├── dist/               # 빌드 결과물
│   ├── MyTODO.exe     # Windows 실행 파일
│   └── MyTODO         # macOS 실행 파일
└── README.md           # 프로젝트 문서
```

## 🔄 업데이트

1. **새 버전 다운로드**
2. **기존 `todo.db` 백업**
3. **새 실행 파일로 교체**
4. **백업한 `todo.db` 복원**

## 📞 지원

문제가 있으면 GitHub 이슈를 생성해주세요.

---

**MyTODO 애플리케이션** - 간단하고 효율적인 할 일 관리! ✨📝 