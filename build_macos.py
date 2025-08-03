#!/usr/bin/env python3
"""
macOS용 MyTODO 애플리케이션 빌드 스크립트
"""

import os
import sys
import platform
import subprocess
import shutil

def cleanup_build_files():
    """빌드 과정에서 생성된 불필요한 파일들을 제거합니다."""
    print("\n불필요한 파일 정리 중...")
    
    # 제거할 폴더들
    folders_to_remove = ['build', '__pycache__']
    
    # 제거할 파일들
    files_to_remove = ['MyTODO.spec']
    
    # dist 폴더 내의 불필요한 MyTODO 폴더 제거 (--onefile 옵션 사용 시 폴더가 생성되면 안됨)
    dist_todo_folder = os.path.join('dist', 'MyTODO')
    if os.path.isdir(dist_todo_folder):
        try:
            shutil.rmtree(dist_todo_folder)
            print("✓ dist/MyTODO 폴더 제거됨 (단일 파일 빌드이므로 불필요)")
        except Exception as e:
            print(f"✗ dist/MyTODO 폴더 제거 실패: {e}")
    
    # 폴더 제거
    for folder in folders_to_remove:
        if os.path.exists(folder):
            try:
                shutil.rmtree(folder)
                print(f"✓ {folder} 폴더 제거됨")
            except Exception as e:
                print(f"✗ {folder} 폴더 제거 실패: {e}")
    
    # 파일 제거
    for file in files_to_remove:
        if os.path.exists(file):
            try:
                os.remove(file)
                print(f"✓ {file} 파일 제거됨")
            except Exception as e:
                print(f"✗ {file} 파일 제거 실패: {e}")
    
    # templates 폴더 내의 __pycache__ 제거
    templates_cache = os.path.join('templates', '__pycache__')
    if os.path.exists(templates_cache):
        try:
            shutil.rmtree(templates_cache)
            print("✓ templates/__pycache__ 폴더 제거됨")
        except Exception as e:
            print(f"✗ templates/__pycache__ 폴더 제거 실패: {e}")
    
    print("파일 정리 완료!")

def build_macos_executable():
    """macOS용 실행 파일을 빌드합니다."""
    
    # macOS 확인
    if platform.system().lower() != 'darwin':
        print("이 스크립트는 macOS에서만 실행할 수 있습니다.")
        return
    
    print("macOS용 MyTODO 애플리케이션 빌드")
    print("="*40)
    
    # PyInstaller 명령어 구성 (macOS용 - 단일 파일 최적화)
    cmd = [
        'pyinstaller',
        '--onefile',  # 단일 실행 파일로 생성
        '--windowed',  # GUI 모드 (콘솔 창 숨김)
        '--name=MyTODO',  # 실행 파일 이름
        '--add-data=templates:templates',  # templates 폴더 포함
        '--exclude-module=matplotlib',  # 불필요한 모듈 제외
        '--exclude-module=numpy',  # 불필요한 모듈 제외
        '--exclude-module=pandas',  # 불필요한 모듈 제외
        '--exclude-module=scipy',  # 불필요한 모듈 제외
        '--exclude-module=PIL',  # 불필요한 모듈 제외
        '--exclude-module=cv2',  # 불필요한 모듈 제외
        '--strip',  # 디버그 심볼 제거로 파일 크기 감소
        '--clean',  # 이전 빌드 정리
        '--noconfirm',  # 기존 파일 덮어쓰기 확인 없이 진행
        'app.py'
    ]
    
    print("빌드 시작...")
    print(f"실행 명령어: {' '.join(cmd)}")
    
    try:
        # PyInstaller 실행
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("빌드 성공!")
        
        # 실행 파일 경로
        exe_path = os.path.join('dist', 'MyTODO')
        
        if os.path.exists(exe_path):
            # 파일 크기 확인
            file_size = os.path.getsize(exe_path)
            file_size_mb = file_size / (1024 * 1024)
            
            print(f"실행 파일 생성됨: {exe_path}")
            print(f"파일 크기: {file_size_mb:.2f} MB")
            
            # 실행 권한 부여
            os.chmod(exe_path, 0o755)
            print("실행 권한이 부여되었습니다.")
            
            # 불필요한 파일 정리
            cleanup_build_files()
            
            # 사용자에게 안내
            print("\n" + "="*50)
            print("macOS 빌드 완료!")
            print("="*50)
            print(f"실행 파일 위치: {exe_path}")
            print(f"파일 크기: {file_size_mb:.2f} MB")
            print("\n사용 방법:")
            print("1. dist 폴더의 MyTODO 파일을 원하는 위치로 복사")
            print("2. 터미널에서 ./MyTODO 실행 또는 더블클릭")
            print("3. 브라우저에서 http://localhost:5000 접속")
            print("\n주의사항:")
            print("- 첫 실행 시 데이터베이스가 자동으로 생성됩니다")
            print("- 실행 파일과 같은 폴더에 todo.db 파일이 생성됩니다")
            print("- 다른 Mac으로 이동할 때는 todo.db 파일도 함께 복사하세요")
            print("- macOS 보안 설정에서 '확인되지 않은 개발자' 허용이 필요할 수 있습니다")
            print("- 단일 파일로 빌드되어 별도의 의존성 파일이 필요하지 않습니다")
            print("- 빌드 과정에서 생성된 불필요한 파일들은 자동으로 정리되었습니다")
            
        else:
            print("오류: 실행 파일이 생성되지 않았습니다.")
            
    except subprocess.CalledProcessError as e:
        print(f"빌드 실패: {e}")
        print(f"오류 출력: {e.stderr}")
    except Exception as e:
        print(f"예상치 못한 오류: {e}")

def create_app_bundle():
    """macOS 앱 번들(.app)을 생성합니다."""
    print("\n앱 번들 생성 중...")
    
    cmd = [
        'pyinstaller',
        '--onedir',  # 디렉토리 형태로 생성
        '--windowed',  # GUI 모드
        '--name=MyTODO',  # 앱 이름
        '--add-data=templates:templates',  # templates 폴더 포함
        '--exclude-module=matplotlib',  # 불필요한 모듈 제외
        '--exclude-module=numpy',  # 불필요한 모듈 제외
        '--exclude-module=pandas',  # 불필요한 모듈 제외
        '--exclude-module=scipy',  # 불필요한 모듈 제외
        '--exclude-module=PIL',  # 불필요한 모듈 제외
        '--exclude-module=cv2',  # 불필요한 모듈 제외
        '--strip',  # 디버그 심볼 제거
        '--clean',  # 이전 빌드 정리
        '--noconfirm',  # 기존 파일 덮어쓰기 확인 없이 진행
        'app.py'
    ]
    
    try:
        subprocess.run(cmd, check=True)
        
        # 앱 번들 생성
        app_path = os.path.join('dist', 'MyTODO.app')
        if os.path.exists(app_path):
            print(f"앱 번들 생성됨: {app_path}")
            print("이제 Applications 폴더로 복사하여 사용할 수 있습니다.")
            
            # 불필요한 파일 정리
            cleanup_build_files()
        else:
            print("앱 번들 생성 실패")
            
    except subprocess.CalledProcessError as e:
        print(f"앱 번들 생성 실패: {e}")

if __name__ == '__main__':
    print("macOS용 MyTODO 애플리케이션 빌드 도구")
    print("="*40)
    
    # 앱 번들 생성
    create_app_bundle() 