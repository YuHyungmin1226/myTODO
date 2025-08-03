@echo off
echo MyTODO 할 일 목록 애플리케이션을 시작합니다...
echo.

REM Python이 설치되어 있는지 확인
python --version >nul 2>&1
if errorlevel 1 (
    echo 오류: Python이 설치되어 있지 않습니다.
    echo Python을 설치한 후 다시 시도해주세요.
    echo https://www.python.org/downloads/
    pause
    exit /b 1
)

REM 현재 디렉토리에서 MyTODO.py 실행
python MyTODO.py

REM 오류가 발생한 경우
if errorlevel 1 (
    echo.
    echo 애플리케이션 실행 중 오류가 발생했습니다.
    pause
) 