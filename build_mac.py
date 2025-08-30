#!/usr/bin/env python3
"""
MyTODO 맥용 포터블 앱 빌드 스크립트
macOS용 실행 파일 생성
"""

import os
import sys
import shutil
import subprocess

def check_pyinstaller():
    """PyInstaller 설치 확인"""
    try:
        subprocess.run(['pyinstaller', '--version'], capture_output=True, check=True)
        print("✅ PyInstaller가 설치되어 있습니다.")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ PyInstaller가 설치되지 않았습니다.")
        print("💡 설치 명령어: pip install pyinstaller")
        return False

def build_portable_mac():
    """맥용 포터블 버전 빌드"""
    print("🚀 macOS용 포터블 빌드를 시작합니다...")
    
    # 현재 디렉터리
    current_dir = os.path.abspath(".")
    templates_path = os.path.join(current_dir, "templates")
    
    print(f"📁 현재 디렉터리: {current_dir}")
    print(f"📁 템플릿 경로: {templates_path}")
    
    # 빌드 명령어 구성 (맥용)
    cmd = [
        'pyinstaller',
        '--onefile',                    # 단일 실행 파일
        '--console',                    # 콘솔 창 표시 (디버깅용)
        '--name=MyTODO',                # 실행 파일명
        '--distpath=portable_build',    # 출력 디렉터리
        '--workpath=build_temp',        # 작업 디렉터리
        '--specpath=build_temp',        # spec 파일 위치
        f'--add-data={templates_path}:templates',  # 템플릿 (맥용 구분자)
        '--hidden-import=flask',
        '--hidden-import=flask_sqlalchemy',
        '--hidden-import=werkzeug',
        '--hidden-import=jinja2',
        '--hidden-import=sqlalchemy',
        '--hidden-import=jinja2.ext',
        '--hidden-import=jinja2.loaders',
        '--hidden-import=jinja2.environment',
        '--hidden-import=jinja2.templating',
        '--hidden-import=codecs',       # 인코딩 지원
        '--hidden-import=locale',       # 로케일 지원
        '--hidden-import=sqlalchemy.text',  # SQLAlchemy text 지원
        '--collect-all=jinja2',         # Jinja2 전체 수집
        '--collect-all=flask',          # Flask 전체 수집
        'MyTODO.py'                     # 메인 스크립트
    ]
    
    print("🔨 PyInstaller로 빌드를 시작합니다...")
    print(f"명령어: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ 빌드 성공!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 빌드 실패: {e}")
        print(f"오류 출력: {e.stderr}")
        return False

def build_app_bundle():
    """앱 번들 빌드"""
    print("🍎 macOS 앱 번들 빌드를 시작합니다...")
    
    # 기존 앱 빌드 디렉터리 정리
    app_build_dir = "app_build"
    if os.path.exists(app_build_dir):
        shutil.rmtree(app_build_dir)
        print("✅ 기존 앱 빌드 디렉터리를 정리했습니다.")
    
    # 현재 디렉터리
    current_dir = os.path.abspath(".")
    templates_path = os.path.join(current_dir, "templates")
    
    # 빌드 명령어 구성 (앱 번들용)
    cmd = [
        'pyinstaller',
        '--windowed',                   # GUI 앱 (콘솔 창 없음)
        '--name=MyTODO',                # 앱 이름
        '--distpath=app_build',         # 출력 디렉터리
        '--workpath=build_temp',        # 작업 디렉터리
        '--specpath=build_temp',        # spec 파일 위치
        f'--add-data={templates_path}:templates',  # 템플릿
        '--hidden-import=flask',
        '--hidden-import=flask_sqlalchemy',
        '--hidden-import=werkzeug',
        '--hidden-import=jinja2',
        '--hidden-import=sqlalchemy',
        '--hidden-import=jinja2.ext',
        '--hidden-import=jinja2.loaders',
        '--hidden-import=jinja2.environment',
        '--hidden-import=jinja2.templating',
        '--hidden-import=codecs',       # 인코딩 지원
        '--hidden-import=locale',       # 로케일 지원
        '--hidden-import=sqlalchemy.text',  # SQLAlchemy text 지원
        '--collect-all=jinja2',         # Jinja2 전체 수집
        '--collect-all=flask',          # Flask 전체 수집
        'MyTODO.py'                     # 메인 스크립트
    ]
    
    print("🔨 앱 번들 빌드를 시작합니다...")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ 앱 번들 빌드 성공!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 앱 번들 빌드 실패: {e}")
        print(f"오류 출력: {e.stderr}")
        return False

def create_portable_package_mac():
    """맥용 포터블 패키지 생성"""
    print("📦 맥용 포터블 패키지를 생성합니다...")
    
    # 출력 폴더
    output_dir = "MyTODO_Portable_Mac"
    
    # 기존 폴더 삭제
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    
    # 새 폴더 생성
    os.makedirs(output_dir)
    
    # 실행 파일 복사
    exe_path = os.path.join("portable_build", "MyTODO")
    if os.path.exists(exe_path):
        shutil.copy2(exe_path, os.path.join(output_dir, "MyTODO"))
        print("✅ 실행 파일 복사 완료")
    else:
        print("❌ 실행 파일을 찾을 수 없습니다.")
        return False
    
    # 실행 스크립트 생성
    script_content = """#!/bin/bash

# MyTODO 실행 스크립트
echo "=================================================="
echo "MyTODO 할 일 목록 애플리케이션"
echo "=================================================="
echo "애플리케이션을 시작합니다..."
echo ""

# 현재 디렉토리로 이동
cd "$(dirname "$0")"

# 실행 권한 확인 및 설정
if [ ! -x "./MyTODO" ]; then
    echo "실행 권한을 설정합니다..."
    chmod +x ./MyTODO
fi

# 실행 파일 실행
./MyTODO

echo ""
echo "애플리케이션이 종료되었습니다."
echo "엔터를 눌러 터미널을 닫습니다..."
read
"""
    
    script_path = os.path.join(output_dir, "MyTODO.command")
    with open(script_path, "w", encoding="utf-8") as f:
        f.write(script_content)
    
    # 실행 권한 부여
    os.chmod(script_path, 0o755)
    os.chmod(os.path.join(output_dir, "MyTODO"), 0o755)
    print("✅ 실행 스크립트 생성 완료")
    
    # README 파일 생성
    readme_content = """# MyTODO - 맥용 포터블 할 일 목록 애플리케이션 📝

## 사용 방법

### 방법 1: 터미널에서 실행 (권장)
1. **MyTODO.command** 파일을 더블클릭
2. 터미널이 열리면서 애플리케이션이 자동으로 시작됩니다
3. 브라우저에서 `http://127.0.0.1:5002` 접속

### 방법 2: 터미널에서 직접 실행
```bash
# 1. 터미널 열기
# 2. MyTODO_Portable_Mac 폴더로 이동
cd /path/to/MyTODO_Portable_Mac

# 3. 실행 파일 실행
./MyTODO

# 4. 브라우저에서 접속
# http://127.0.0.1:5002
```

## 주요 기능

- 📝 할 일 관리: 추가, 수정, 완료, 삭제
- ✅ 완료 상태: 완료된 할 일에 취소선 표시
- 🔄 실시간 업데이트: 즉시 반영되는 변경사항
- 💾 데이터 저장: SQLite 데이터베이스 사용
- 🌐 웹 인터페이스: 브라우저에서 접근 가능
- 🇰🇷 한국 시간대: 정확한 한국 시간 표시

## 포터블 사용

- **USB 사용**: USB 드라이브에 복사하여 어디서든 사용 가능
- **로컬 사용**: 원하는 폴더에 복사하여 사용
- **데이터 저장**: `todo.db` 파일이 실행 파일과 같은 폴더에 자동 생성
- **백업**: `todo.db` 파일을 복사하여 백업 가능

## 문제 해결

### 포트 충돌
- 5002번 포트가 사용 중인 경우 다른 프로그램을 종료 후 재시작

### 데이터베이스 오류
- `todo.db` 파일을 삭제 후 재시작하면 새로운 데이터베이스가 생성됩니다

### 실행 권한 오류
```bash
chmod +x MyTODO
chmod +x MyTODO.command
```

### 보안 경고 (macOS)
- macOS에서 "확인되지 않은 개발자" 경고가 나타날 수 있습니다
- 시스템 환경설정 > 보안 및 개인 정보 보호에서 "허용" 선택

## 시스템 요구사항

- **운영체제**: macOS 10.14 이상
- **아키텍처**: Intel 또는 Apple Silicon (M1/M2)
- **메모리**: 최소 100MB
- **디스크**: 최소 50MB

## 지원

문제가 있으면 GitHub 이슈를 생성해주세요.
"""
    
    with open(os.path.join(output_dir, "README_Mac.md"), "w", encoding="utf-8") as f:
        f.write(readme_content)
    print("✅ README 파일 생성 완료")
    
    return True

def create_app_package():
    """앱 번들 패키지 생성"""
    print("🍎 앱 번들 패키지를 생성합니다...")
    
    # 앱 번들 경로
    app_path = os.path.join("app_build", "MyTODO.app")
    
    if os.path.exists(app_path):
        print("✅ 앱 번들이 생성되었습니다.")
        print(f"📁 앱 번들 경로: {os.path.abspath(app_path)}")
        return True
    else:
        print("❌ 앱 번들을 찾을 수 없습니다.")
        return False

def cleanup():
    """임시 파일 정리"""
    print("🧹 임시 파일을 정리합니다...")
    
    temp_dirs = ["build_temp", "portable_build", "app_build"]
    for dir_name in temp_dirs:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"✅ {dir_name} 삭제 완료")

def main():
    """메인 함수"""
    print("=" * 50)
    print("macOS용 MyTODO 포터블 빌드 도구")
    print("=" * 50)
    
    # PyInstaller 확인
    if not check_pyinstaller():
        return
    
    # 포터블 버전 빌드
    if not build_portable_mac():
        return
    
    # 포터블 패키지 생성
    if not create_portable_package_mac():
        return
    
    # 앱 번들 빌드
    if not build_app_bundle():
        return
    
    # 앱 번들 패키지 생성
    if not create_app_package():
        return
    
    print("\n🎉 맥용 빌드 완료!")
    print(f"📁 {os.path.abspath('MyTODO_Portable_Mac')} 폴더에 포터블 버전이 생성되었습니다.")
    print(f"🍎 {os.path.abspath('app_build/MyTODO.app')} 앱 번들이 생성되었습니다.")
    print("💾 이 폴더들을 USB에 복사하여 어디서든 실행할 수 있습니다.")
    
    # 정리
    cleanup()

if __name__ == "__main__":
    main() 