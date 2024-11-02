:: @echo off

:: 프로젝트 내부의 venv 경로 설정
set VENV_DIR=venv

:: 가상 환경 활성화
call %VENV_DIR%\Scripts\activate.bat

:: 파이썬 메인 파일 실행
python main.py

:: 가상 환경 비활성화
:: deactivate
