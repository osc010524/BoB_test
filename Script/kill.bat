@echo off
:: 배치 파일이 인자로 받은 PID를 종료하는 스크립트

if "%~1"=="" (
    echo 오류: PID를 입력해야 합니다.
    echo 사용법: kill_process.bat [PID]
    exit /b 1
)

set PID=%~1
echo 프로세스 %PID% 종료 중...

:: PID로 프로세스를 강제로 종료
taskkill /PID %PID% /F

:: 종료 결과 확인
if %errorlevel% == 0 (
    echo 프로세스 %PID%가 성공적으로 종료되었습니다.
) else (
    echo 프로세스 %PID% 종료 실패. PID가 존재하지 않거나 관리자 권한이 필요할 수 있습니다.
)
