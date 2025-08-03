#!/usr/bin/env python3
"""
Windows용 MyTODO 애플리케이션 빌드 도구
단일 실행 파일(.exe)을 생성합니다.
"""

import os
import sys
import subprocess
import shutil
import time
from pathlib import Path

def print_header():
    """헤더 출력"""
    print("="*60)
    print("🚀 Windows용 MyTODO 애플리케이션 빌드 도구")
    print("="*60)

def print_step(step, title):
    """단계 출력"""
    print(f"\n📋 단계 {step}: {title}")
    print("-" * 40)

def check_requirements():
    """시스템 요구사항 확인"""
    print("🔍 시스템 요구사항 확인 중...")
    
    # Windows 확인
    if sys.platform != "win32":
        print("❌ 이 스크립트는 Windows에서만 실행할 수 있습니다.")
        return False
    
    # Python 버전 확인
    python_version = sys.version_info
    print(f"✅ Windows {os.name} 확인됨")
    print(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro} 확인됨")
    
    # PyInstaller 확인
    try:
        import PyInstaller
        print(f"✅ PyInstaller {PyInstaller.__version__} 확인됨")
    except ImportError:
        print("❌ PyInstaller가 설치되지 않았습니다.")
        print("다음 명령어로 설치하세요: pip install pyinstaller")
        return False
    
    # 필요한 파일 확인
    required_files = ['app.py', 'requirements.txt', 'templates']
    for file in required_files:
        if not os.path.exists(file):
            print(f"❌ 필수 파일이 없습니다: {file}")
            return False
        else:
            print(f"✅ {file} 확인됨")
    
    return True

def cleanup_build_files():
    """빌드 과정에서 생성된 불필요한 파일들을 정리합니다."""
    print("🧹 불필요한 파일 정리 중...")
    
    # build 폴더 제거
    if os.path.exists('build'):
        try:
            shutil.rmtree('build')
            print("✅ build 폴더 제거됨")
        except Exception as e:
            print(f"⚠️  build 폴더 제거 실패: {e}")
    
    # .spec 파일 제거
    spec_file = 'MyTODO.spec'
    if os.path.exists(spec_file):
        try:
            os.remove(spec_file)
            print("✅ MyTODO.spec 파일 제거됨")
        except Exception as e:
            print(f"⚠️  MyTODO.spec 파일 제거 실패: {e}")
    
    # __pycache__ 폴더들 제거
    for root, dirs, files in os.walk('.'):
        for dir_name in dirs:
            if dir_name == '__pycache__':
                try:
                    shutil.rmtree(os.path.join(root, dir_name))
                    print(f"✅ {os.path.join(root, dir_name)} 제거됨")
                except Exception as e:
                    print(f"⚠️  {os.path.join(root, dir_name)} 제거 실패: {e}")
    
    print("✅ 파일 정리 완료!")

def build_windows_executable():
    """Windows 실행 파일(.exe)을 빌드합니다."""
    print("🔨 빌드 시작...")
    
    cmd = [
        'pyinstaller',
        '--onefile',  # 단일 파일로 생성
        '--name=MyTODO',  # 실행 파일 이름
        '--add-data=templates;templates',  # templates 폴더 포함 (Windows용 구분자)
        '--exclude-module=matplotlib',  # 불필요한 모듈 제외
        '--exclude-module=numpy',  # 불필요한 모듈 제외
        '--exclude-module=pandas',  # 불필요한 모듈 제외
        '--exclude-module=scipy',  # 불필요한 모듈 제외
        '--exclude-module=PIL',  # 불필요한 모듈 제외
        '--exclude-module=cv2',  # 불필요한 모듈 제외
        '--exclude-module=tkinter',  # 불필요한 모듈 제외
        '--exclude-module=PyQt5',  # 불필요한 모듈 제외
        '--exclude-module=PyQt6',  # 불필요한 모듈 제외
        '--exclude-module=wx',  # 불필요한 모듈 제외
        '--strip',  # 디버그 심볼 제거
        '--clean',  # 이전 빌드 정리
        '--noconfirm',  # 기존 파일 덮어쓰기 확인 없이 진행
        'app.py'
    ]
    
    try:
        print(f"📝 실행 명령어: {' '.join(cmd)}")
        start_time = time.time()
        
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        end_time = time.time()
        build_time = end_time - start_time
        
        print(f"✅ 빌드 성공! (소요 시간: {build_time:.1f}초)")
        
        # 실행 파일 경로 확인
        exe_path = os.path.join('dist', 'MyTODO.exe')
        if os.path.exists(exe_path):
            # 파일 크기 계산
            file_size = os.path.getsize(exe_path)
            file_size_mb = file_size / (1024 * 1024)
            
            print(f"📦 실행 파일 생성됨: {exe_path}")
            print(f"📏 파일 크기: {file_size_mb:.2f} MB")
            
            # 실행 권한 확인 (Windows에서는 기본적으로 실행 가능)
            print("🔐 실행 파일이 생성되었습니다.")
            
            return True, exe_path, file_size_mb
        else:
            print("❌ 실행 파일이 생성되지 않았습니다.")
            return False, None, 0
            
    except subprocess.CalledProcessError as e:
        print(f"❌ 빌드 실패: {e}")
        if e.stderr:
            print(f"📋 오류 출력: {e.stderr}")
        return False, None, 0
    except Exception as e:
        print(f"❌ 예상치 못한 오류: {e}")
        return False, None, 0

def test_executable(exe_path):
    """실행 파일 테스트"""
    print("🧪 실행 파일 테스트 중...")
    
    try:
        # 기존 프로세스 종료 (Windows용)
        try:
            subprocess.run(['taskkill', '/f', '/im', 'MyTODO.exe'], 
                         capture_output=True, text=True)
            time.sleep(1)
        except Exception:
            pass
        
        # 실행 파일 테스트
        process = subprocess.Popen([exe_path], 
                                 stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE,
                                 text=True)
        
        # 5초 대기
        time.sleep(5)
        
        if process.poll() is None:
            print("✅ 애플리케이션이 정상적으로 실행되었습니다!")
            
            # 웹 서버 응답 확인 (5001-5010 포트 중 하나에서 시도)
            try:
                import requests
                for test_port in range(5001, 5011):
                    try:
                        response = requests.get(f'http://localhost:{test_port}', timeout=2)
                        if response.status_code in [200, 302]:
                            print(f"✅ 웹 서버가 포트 {test_port}에서 정상적으로 응답합니다!")
                            break
                    except requests.exceptions.RequestException:
                        continue
                else:
                    print("⚠️  웹 서버 응답을 확인할 수 없습니다.")
            except ImportError:
                print("ℹ️  requests 모듈이 없어 웹 서버 테스트를 건너뜁니다.")
            except Exception as e:
                print(f"⚠️  웹 서버 테스트 실패: {e}")
            
            # 프로세스 종료
            process.terminate()
            process.wait()
            return True
        else:
            stdout, stderr = process.communicate()
            print(f"❌ 애플리케이션 실행 실패")
            if stderr:
                print(f"📋 오류 출력: {stderr}")
            return False
            
    except Exception as e:
        print(f"❌ 테스트 중 오류 발생: {e}")
        return False

def print_success_info(exe_path, file_size_mb):
    """성공 정보 출력"""
    print_step(4, "빌드 완료")
    
    print("🎉 Windows 빌드 완료!")
    print("="*60)
    print(f"📦 단일 실행 파일: {exe_path}")
    print(f"📏 파일 크기: {file_size_mb:.2f} MB")
    print("✅ 단일 실행 파일이 성공적으로 생성되었습니다!")
    
    print("\n📖 사용 방법:")
    print("1. dist/MyTODO.exe 파일을 더블클릭하거나 명령 프롬프트에서 실행")
    print("2. 브라우저에서 http://localhost:5001-5010 중 표시된 포트로 접속")
    
    print("\n⚠️  주의사항:")
    print("- 첫 실행 시 데이터베이스가 자동으로 생성됩니다")
    print("- 실행 파일과 같은 폴더에 todo.db 파일이 생성됩니다")
    print("- 다른 PC로 이동할 때는 todo.db 파일도 함께 복사하세요")
    print("- Windows Defender에서 차단될 수 있습니다 (속성에서 '차단 해제' 체크)")
    print("- 기존 프로세스가 있으면 자동으로 종료되고 새로 시작됩니다")
    print("- 포트 충돌 시 자동으로 다른 포트를 선택합니다")
    print("- 단일 파일로 빌드되어 별도의 의존성 파일이 필요하지 않습니다")
    
    print("\n🚀 이제 MyTODO 애플리케이션을 사용할 수 있습니다!")

def main():
    """메인 함수"""
    print_header()
    
    # 요구사항 확인
    if not check_requirements():
        print("\n❌ 빌드를 중단합니다.")
        return False
    
    # 단일 실행 파일 빌드
    print_step(2, "단일 실행 파일 빌드")
    success, exe_path, file_size_mb = build_windows_executable()
    
    if not success:
        print("\n❌ 단일 실행 파일 빌드가 실패했습니다.")
        return False
    
    # 불필요한 파일 정리
    cleanup_build_files()
    
    # 실행 파일 테스트
    print_step(3, "실행 파일 테스트")
    test_success = test_executable(exe_path)
    
    if test_success:
        print_success_info(exe_path, file_size_mb)
        return True
    else:
        print("\n⚠️  빌드는 성공했지만 테스트에서 문제가 발생했습니다.")
        print("실행 파일을 직접 테스트해보세요.")
        return False

if __name__ == '__main__':
    try:
        success = main()
        if success:
            print("\n✅ 모든 작업이 성공적으로 완료되었습니다!")
        else:
            print("\n❌ 작업 중 문제가 발생했습니다.")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⏹️  사용자에 의해 중단되었습니다.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 예상치 못한 오류: {e}")
        sys.exit(1) 