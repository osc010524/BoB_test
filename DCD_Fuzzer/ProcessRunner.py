import subprocess
import time
import os
from __init__ import logging, System

class ProcessRunner():
    def __init__(self):
        pass
    def run(self):

        # 로깅 설정
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

        # RabbitMQ 서버 실행 경로 설정
        rabbitmq_start_command = os.path.join(System.rabbitmq_sbin_path, "rabbitmq-server.bat")
        rabbitmq_stop_command = os.path.join(System.rabbitmq_sbin_path, "rabbitmqctl.bat") + " stop"

        try:
            # RabbitMQ 서버 시작
            logging.info("RabbitMQ 서버를 시작합니다.")
            server_process = subprocess.Popen(rabbitmq_start_command, shell=True)

            # 서버가 시작되고 실행되는 동안 대기 (여기서는 10초 대기)
            time.sleep(10)  # 필요에 따라 서버가 준비될 때까지 기다립니다
            logging.info("RabbitMQ 서버가 정상적으로 시작되었습니다.")
            print("RabbitMQ 서버가 정상적으로 시작되었습니다.")

            print("RabbitMQ 서버를 10초 동안 실행합니다.")
            time.sleep(10)  # 필요에 따라 서버가 준비될 때까지 기다립니다
            # RabbitMQ 서버 종료
            logging.info("RabbitMQ 서버를 종료합니다.")
            subprocess.run(rabbitmq_stop_command, shell=True, check=True)
            logging.info("RabbitMQ 서버가 정상적으로 종료되었습니다.")
            print("RabbitMQ 서버가 정상적으로 종료되었습니다.")

        except subprocess.CalledProcessError as e:
            logging.error(f"RabbitMQ 서버 종료에 실패했습니다: {e}")
        except Exception as e:
            logging.error(f"오류 발생: {e}")


# if __name__ == '__main__':
#     process_runner = ProcessRunner()
#     process_runner.run()