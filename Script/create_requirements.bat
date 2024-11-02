@echo off

:: 가상환경 활성화
call ..\venv\Scripts\activate.bat

:: 현재 가상환경의 패키지 목록을 requirements.txt 파일로 저장
pip freeze > requirements.txt

:: 완료 메시지 출력
echo requirements.txt 파일이 생성되었습니다.
