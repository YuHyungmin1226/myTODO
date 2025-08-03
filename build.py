#!/usr/bin/env python3
"""
MyTODO 포터블 앱 빌드 스크립트
Windows용 실행 파일 생성
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

def build_portable():
    """포터블 버전 빌드"""
    print("🚀 Windows용 포터블 빌드를 시작합니다...")
    
    # 현재 디렉터리
    current_dir = os.path.abspath(".")
    templates_path = os.path.join(current_dir, "templates")
    
    print(f"📁 현재 디렉터리: {current_dir}")
    print(f"📁 템플릿 경로: {templates_path}")
    
    # 빌드 명령어 구성
    cmd = [
        'pyinstaller',
        '--onefile',                    # 단일 실행 파일
        '--console',                    # 콘솔 창 표시 (디버깅용)
        '--name=MyTODO',                # 실행 파일명
        '--distpath=portable_build',    # 출력 디렉터리
        '--workpath=build_temp',        # 작업 디렉터리
        '--specpath=build_temp',        # spec 파일 위치
        f'--add-data={templates_path};templates',  # 템플릿 (절대 경로)
        '--hidden-import=flask',
        '--hidden-import=flask_sqlalchemy',
        '--hidden-import=werkzeug',
        '--hidden-import=jinja2',
        '--hidden-import=sqlalchemy',
        '--hidden-import=jinja2.ext',
        '--hidden-import=jinja2.loaders',
        '--hidden-import=jinja2.environment',
        '--hidden-import=jinja2.templating',
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

def create_portable_package():
    """포터블 패키지 생성"""
    print("📦 포터블 패키지를 생성합니다...")
    
    # 출력 폴더
    output_dir = "MyTODO_Portable"
    
    # 기존 폴더 삭제
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    
    # 새 폴더 생성
    os.makedirs(output_dir)
    
    # 실행 파일 복사
    exe_path = os.path.join("portable_build", "MyTODO.exe")
    if os.path.exists(exe_path):
        shutil.copy2(exe_path, os.path.join(output_dir, "MyTODO.exe"))
        print("✅ 실행 파일 복사 완료")
    else:
        print("❌ 실행 파일을 찾을 수 없습니다.")
        return False
    
    # README 파일 생성
    readme_content = """# MyTODO 포터블 앱

## 사용 방법

1. USB 드라이브에 이 폴더를 복사하세요
2. MyTODO.exe를 더블클릭하여 실행하세요
3. 웹 브라우저에서 http://127.0.0.1:5002 접속
4. 할 일을 추가, 수정, 완료, 삭제할 수 있습니다

## 주요 기능

- 📝 할 일 추가/수정/완료/삭제
- ✅ 완료 상태 표시
- 🔄 실시간 업데이트
- 💾 SQLite 데이터베이스 사용
- 🌐 웹 인터페이스
- 🇰🇷 한국 시간대 지원

## 주의사항

- Windows 10/11에서 실행됩니다
- 첫 실행 시 데이터베이스가 자동으로 생성됩니다
- 종료하려면 Ctrl+C를 누르거나 창을 닫으세요
- todo.db 파일이 데이터베이스입니다

## 문제 해결

- 실행이 안 되는 경우: 관리자 권한으로 실행해보세요
- 포트 충돌 시: 5002번 포트가 사용 중인지 확인하세요
- 데이터베이스 오류: todo.db 파일을 삭제하고 다시 실행하세요

## 지원

문제가 있으면 GitHub 이슈를 생성해주세요.
"""
    
    with open(os.path.join(output_dir, "README.txt"), "w", encoding="utf-8") as f:
        f.write(readme_content)
    print("✅ README 파일 생성 완료")
    
    # 관리자 권한 실행 배치 파일 생성
    bat_content = """@echo off
echo MyTODO 포터블 앱을 관리자 권한으로 실행합니다...
powershell -Command "Start-Process MyTODO.exe -Verb RunAs"
pause
"""
    
    with open(os.path.join(output_dir, "run_as_admin.bat"), "w", encoding="utf-8") as f:
        f.write(bat_content)
    print("✅ 관리자 권한 실행 배치 파일 생성 완료")
    
    return True

def cleanup():
    """임시 파일 정리"""
    print("🧹 임시 파일을 정리합니다...")
    
    temp_dirs = ["build_temp", "portable_build"]
    for dir_name in temp_dirs:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"✅ {dir_name} 삭제 완료")

def main():
    """메인 함수"""
    print("=" * 50)
    print("Windows용 MyTODO 포터블 빌드 도구")
    print("=" * 50)
    
    # PyInstaller 확인
    if not check_pyinstaller():
        return
    
    # 빌드 실행
    if not build_portable():
        return
    
    # 포터블 패키지 생성
    if not create_portable_package():
        return
    
    print("\n🎉 포터블 빌드 완료!")
    print(f"📁 {os.path.abspath('MyTODO_Portable')} 폴더에 포터블 버전이 생성되었습니다.")
    print("💾 이 폴더를 USB에 복사하여 어디서든 실행할 수 있습니다.")
    
    # 정리
    cleanup()

if __name__ == "__main__":
    main() 