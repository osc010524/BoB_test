@echo off

:: 가상환경 활성화
call ..\venv\Scripts\activate.bat

:: requirements.txt 파일의 패키지들을 설치
pip install -r requirements.txt

:: 완료 메시지 출력
echo 패키지가 설치되었습니다.
