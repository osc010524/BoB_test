@echo off
:: rabbitmqctl.bat status 명령어에서 OS PID 라인만 출력

:: 직접 명령어를 실행
call "C:\RabbitMQ\rabbitmq-server-windows-4.0.3\rabbitmq_server-4.0.3\sbin\rabbitmqctl.bat" status | findstr "OS PID"
