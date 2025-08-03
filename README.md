# MyTODO - 할 일 목록 애플리케이션 📝

간단하고 효율적인 할 일 목록 관리 애플리케이션입니다. 사용자 인증, 할 일 추가/수정/완료/삭제 기능을 제공합니다.

## ✨ 주요 기능

- 🔐 **사용자 인증**: 회원가입 및 로그인 시스템
- 📝 **할 일 관리**: 추가, 수정, 완료, 삭제
- ✅ **완료 상태**: 완료된 할 일에 취소선 표시
- 🔄 **실시간 업데이트**: 즉시 반영되는 변경사항
- 💾 **데이터 저장**: SQLite 데이터베이스 사용
- 🌐 **웹 인터페이스**: 브라우저에서 접근 가능

## 🚀 실행 방법

### 기본 실행
```bash
python MyTODO.py
```

### 특정 호스트로 실행
```bash
python MyTODO.py --host 0.0.0.0
```

### 도움말 보기
```bash
python MyTODO.py --help
```

## 📁 프로젝트 구조

```
MyTODO/
├── MyTODO.py             # 메인 애플리케이션
├── requirements.txt       # Python 패키지 의존성
├── templates/            # HTML 템플릿
│   ├── base.html         # 기본 레이아웃
│   ├── login.html        # 로그인 페이지
│   ├── register.html     # 회원가입 페이지
│   ├── dashboard.html    # 메인 대시보드
│   └── edit_todo.html    # 할 일 수정 페이지
├── README.md             # 프로젝트 설명서
└── .gitignore           # Git 무시 파일
```

## 🛠️ 설치 및 설정

1. **Python 설치** (3.8 이상)
2. **의존성 설치**
   ```bash
   pip install -r requirements.txt
   ```
3. **애플리케이션 실행**
   ```bash
   python MyTODO.py
   ```
4. **브라우저에서 접속**
   - 자동 선택된 포트로 접속 (5001-5020 범위)
   - 터미널에 표시되는 URL 확인

## 💾 데이터 저장

- **데이터베이스**: SQLite (`todo.db`)
- **저장 위치**: 실행 파일과 같은 폴더
- **사용 방식**: USB 또는 로컬 PC에서 사용
- **백업**: `todo.db` 파일을 복사하여 백업 가능

### 📁 파일 구조
```
MyTODO/
├── MyTODO.py             # 메인 애플리케이션
├── todo.db               # 데이터베이스 (자동 생성)
├── requirements.txt       # Python 패키지 의존성
├── templates/            # HTML 템플릿
│   ├── base.html         # 기본 레이아웃
│   ├── login.html        # 로그인 페이지
│   ├── register.html     # 회원가입 페이지
│   ├── dashboard.html    # 메인 대시보드
│   └── edit_todo.html    # 할 일 수정 페이지
├── README.md             # 프로젝트 설명서
└── .gitignore           # Git 무시 파일
```

### 🔄 데이터 공유 방법

#### USB 사용
1. **USB에 복사**: 전체 MyTODO 폴더를 USB에 복사
2. **다른 PC에서 실행**: USB를 다른 PC에 연결하여 `python MyTODO.py` 실행
3. **데이터 동기화**: USB의 `todo.db` 파일이 모든 PC에서 동일하게 사용됨

#### 로컬 PC 사용
1. **로컬 폴더**: PC의 원하는 폴더에 MyTODO 저장
2. **독립적 사용**: 각 PC에서 `python MyTODO.py`로 독립적으로 데이터 관리
3. **백업**: 필요시 `todo.db` 파일을 다른 위치에 복사

## 🔧 포트 관리

### 고정 포트 사용
- **사용 포트**: 5002 (고정)
- **프로세스 종료**: 기존 MyTODO 프로세스 자동 종료
- **포트 충돌**: 5002 포트가 사용 중일 경우 오류 메시지 표시

### 포트 충돌 해결
1. **기존 프로세스 종료**: 자동으로 기존 MyTODO 프로세스 종료
2. **수동 해결**: 다른 프로그램이 5002 포트를 사용 중인 경우 종료
3. **시스템 재부팅**: 필요한 경우 시스템 재부팅

## 🛡️ 보안 기능

- **비밀번호 해싱**: Werkzeug 보안 해시 사용
- **세션 관리**: Flask-Login으로 안전한 세션
- **SQL 인젝션 방지**: SQLAlchemy ORM 사용
- **XSS 방지**: Jinja2 템플릿 엔진

## 🔍 문제 해결

### 포트 충돌
```bash
# 다른 포트 사용
python MyTODO.py --port 8080

# 또는 기존 프로세스 종료 후 재시작
```

### 데이터베이스 오류
```bash
# 데이터베이스 재생성
rm ~/MyTODO/todo.db
python MyTODO.py
```

### 권한 오류
```bash
# 관리자 권한으로 실행 (Windows)
# 또는 sudo 사용 (macOS/Linux)
```

## 📦 시스템 요구사항

- **Python**: 3.8 이상
- **운영체제**: Windows, macOS, Linux
- **메모리**: 최소 100MB
- **디스크**: 최소 50MB

## 📋 패키지 목록

- Flask (웹 프레임워크)
- Flask-SQLAlchemy (데이터베이스 ORM)
- Flask-Login (사용자 인증)
- Werkzeug (보안 유틸리티)
- SQLite3 (데이터베이스)

## 🔄 업데이트

```bash
# 최신 버전 가져오기
git pull origin main

# 의존성 업데이트
pip install -r requirements.txt --upgrade
```

## 📞 지원

문제가 발생하면 다음을 확인하세요:
1. Python 버전 (3.8 이상)
2. 모든 의존성 설치 완료
3. 포트 사용 가능 여부
4. 데이터베이스 파일 권한

---

**MyTODO** - 간단하고 효율적인 할 일 관리 🎯 