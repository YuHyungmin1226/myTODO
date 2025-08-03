import os
import sys
import platform
import subprocess
import shutil

def build_executable():
    """PyInstaller를 사용하여 실행 파일을 빌드합니다."""
    
    # 현재 플랫폼 확인
    current_platform = platform.system().lower()
    print(f"현재 플랫폼: {current_platform}")
    
    # PyInstaller 명령어 구성
    cmd = [
        'pyinstaller',
        '--onefile',  # 단일 실행 파일로 생성
        '--windowed',  # 콘솔 창 숨김 (Windows/macOS)
        '--name=MyTODO',  # 실행 파일 이름
        '--add-data=templates;templates',  # templates 폴더 포함
        '--icon=icon.ico' if current_platform == 'windows' else '--icon=icon.icns',  # 아이콘
        '--clean',  # 이전 빌드 정리
        'app.py'
    ]
    
    # macOS에서는 경로 구분자를 :로 변경
    if current_platform == 'darwin':
        cmd[4] = '--add-data=templates:templates'
    
    print("빌드 시작...")
    print(f"실행 명령어: {' '.join(cmd)}")
    
    try:
        # PyInstaller 실행
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("빌드 성공!")
        
        # 실행 파일 경로
        if current_platform == 'windows':
            exe_path = os.path.join('dist', 'MyTODO.exe')
        else:
            exe_path = os.path.join('dist', 'MyTODO')
        
        if os.path.exists(exe_path):
            print(f"실행 파일 생성됨: {exe_path}")
            
            # 사용자에게 안내
            print("\n" + "="*50)
            print("빌드 완료!")
            print("="*50)
            print(f"실행 파일 위치: {exe_path}")
            print("\n사용 방법:")
            print("1. dist 폴더의 실행 파일을 원하는 위치로 복사")
            print("2. 더블클릭으로 실행")
            print("3. 브라우저에서 http://localhost:5000 접속")
            print("\n주의사항:")
            print("- 첫 실행 시 데이터베이스가 자동으로 생성됩니다")
            print("- 실행 파일과 같은 폴더에 todo.db 파일이 생성됩니다")
            print("- 다른 PC로 이동할 때는 todo.db 파일도 함께 복사하세요")
            
        else:
            print("오류: 실행 파일이 생성되지 않았습니다.")
            
    except subprocess.CalledProcessError as e:
        print(f"빌드 실패: {e}")
        print(f"오류 출력: {e.stderr}")
    except Exception as e:
        print(f"예상치 못한 오류: {e}")

def create_icon():
    """간단한 아이콘 파일을 생성합니다."""
    try:
        # Windows용 .ico 파일 생성 (간단한 텍스트 기반)
        if platform.system().lower() == 'windows':
            with open('icon.ico', 'wb') as f:
                # 간단한 ICO 파일 헤더 (16x16 픽셀)
                f.write(b'\x00\x00\x01\x00\x01\x00\x10\x10\x00\x00\x01\x00\x20\x00\x68\x04\x00\x00\x16\x00\x00\x00')
                # 나머지는 기본 아이콘 데이터
                f.write(b'\x00' * 1024)
        else:
            # macOS용 .icns 파일은 복잡하므로 건너뜀
            pass
    except:
        print("아이콘 생성 실패 (무시하고 계속)")

if __name__ == '__main__':
    print("MyTODO 애플리케이션 빌드 도구")
    print("="*30)
    
    # 아이콘 생성 시도
    create_icon()
    
    # 빌드 실행
    build_executable() 