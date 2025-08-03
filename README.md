# MyTODO - 할 일 목록 애플리케이션 📝

간단하고 효율적인 할 일 목록 관리 애플리케이션입니다. 완전한 포터블 사용을 위해 설계되었으며, 할 일 추가/수정/완료/삭제 기능을 제공합니다.

## ✨ 주요 기능

- 📝 **할 일 관리**: 추가, 수정, 완료, 삭제
- ✅ **완료 상태**: 완료된 할 일에 취소선 표시
- 🔄 **실시간 업데이트**: 즉시 반영되는 변경사항
- 💾 **데이터 저장**: SQLite 데이터베이스 사용
- 🌐 **웹 인터페이스**: 브라우저에서 접근 가능
- 🚀 **완전한 포터블**: Python 설치 없이도 사용 가능
- 🇰🇷 **한국 시간대**: 정확한 한국 시간 표시

## 🚀 실행 방법

### 완전한 포터블 사용 (권장)
1. **다운로드**: `MyTODO_Portable.zip` 파일 다운로드
2. **압축 해제**: USB나 원하는 폴더에 압축 해제
3. **실행**: `MyTODO.exe` 더블클릭
4. **접속**: 브라우저에서 `http://127.0.0.1:5002` 접속

### 개발자용 실행
```bash
# 1. 의존성 설치
pip install -r requirements.txt

# 2. 애플리케이션 실행
python MyTODO.py

# 3. 브라우저에서 접속
# http://127.0.0.1:5002
```

### 포터블 패키지 생성
```bash
# PyInstaller 설치
pip install pyinstaller

# 포터블 패키지 생성
pyinstaller --onedir --name MyTODO --add-data "templates;templates" MyTODO.py

# 생성된 파일들을 MyTODO_Portable 폴더로 복사
xcopy dist\MyTODO MyTODO_Portable /E /I

# ZIP 파일 생성
powershell Compress-Archive -Path "MyTODO_Portable" -DestinationPath "MyTODO_Portable.zip" -Force
```

## 📁 프로젝트 구조

```
MyTODO/
├── MyTODO.py             # 메인 애플리케이션
├── requirements.txt      # Python 패키지 의존성
├── templates/            # HTML 템플릿
│   ├── base.html         # 기본 레이아웃
│   ├── dashboard.html    # 메인 대시보드
│   └── edit_todo.html    # 할 일 수정 페이지
├── todo.db               # 데이터베이스 (자동 생성)
├── README.md             # 프로젝트 설명서
└── .gitignore           # Git 무시 파일
```

## 💾 데이터 저장

- **데이터베이스**: SQLite (`todo.db`)
- **저장 위치**: 실행 파일과 같은 폴더
- **사용 방식**: USB 또는 로컬 PC에서 사용
- **백업**: `todo.db` 파일을 복사하여 백업 가능
- **시간대**: 한국 표준시 (KST) 기준

## 🔧 포트 관리

- **사용 포트**: 5002 (고정)
- **접속 주소**: `http://127.0.0.1:5002`

## 🔍 문제 해결

### 포트 충돌
- 5002번 포트가 사용 중인 경우 다른 프로그램을 종료 후 재시작

### 데이터베이스 오류
- `todo.db` 파일을 삭제 후 재시작하면 새로운 데이터베이스가 생성됩니다

### 템플릿 오류 (PyInstaller)
- `templates` 폴더가 실행 파일과 같은 위치에 있는지 확인
- `--add-data "templates;templates"` 옵션으로 템플릿 포함

## 📦 시스템 요구사항

### 포터블 버전
- **운영체제**: Windows
- **메모리**: 최소 100MB
- **디스크**: 최소 50MB

### 개발 환경
- **Python**: 3.8 이상
- **운영체제**: Windows, macOS, Linux
- **메모리**: 최소 100MB
- **디스크**: 최소 50MB

## 📋 사용된 기술

- **Flask** (웹 프레임워크)
- **Flask-SQLAlchemy** (데이터베이스 ORM)
- **SQLite3** (데이터베이스)
- **PyInstaller** (포터블 패키지 생성)
- **Bootstrap 5** (UI 프레임워크)
- **Font Awesome** (아이콘)

## 📦 패키지 목록

```
Flask==3.0.0
Flask-SQLAlchemy==3.1.1
Werkzeug==3.0.1
Jinja2==3.1.2
MarkupSafe==2.1.3
itsdangerous==2.1.2
click==8.1.7
blinker==1.7.0
SQLAlchemy==2.0.23
typing_extensions==4.8.0
greenlet==3.0.1
```

---

**MyTODO** - 간단하고 효율적인 할 일 관리 🎯 