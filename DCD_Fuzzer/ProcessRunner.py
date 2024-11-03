import subprocess
import time
import os
from DCD_Fuzzer.data_model import logging, System

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

            # time.sleep(1)  # 필요에 따라 서버가 준비될 때까지 기다립니다
            # RabbitMQ 서버 종료
            logging.info("RabbitMQ 서버를 종료합니다.")
            subprocess.run(rabbitmq_stop_command, shell=True, check=True)
            logging.info("RabbitMQ 서버가 정상적으로 종료되었습니다.")

        except subprocess.CalledProcessError as e:
            logging.error(f"RabbitMQ 서버 종료에 실패했습니다: {e}")
        except Exception as e:
            logging.error(f"오류 발생: {e}")

    def start(self) :
        # 로깅 설정
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

        # RabbitMQ 서버 실행 경로 설정
        rabbitmq_start_command = os.path.join(System.rabbitmq_sbin_path, "rabbitmq-server.bat")

        try:
            # RabbitMQ 서버 시작
            logging.info("RabbitMQ 서버를 시작합니다.")
            server_process = subprocess.Popen(rabbitmq_start_command, shell=True)
            pid = server_process.pid

            # 서버가 시작되고 실행되는 동안 대기 (여기서는 10초 대기)
            if not self.start_rabbitmq_server():
                logging.error("RabbitMQ 서버 시작에 실패했습니다.")
            else:
                logging.info("RabbitMQ 서버가 정상적으로 시작되었습니다.")

        except subprocess.CalledProcessError as e:
            logging.error(f"RabbitMQ 서버 시작에 실패했습니다: {e}")
        except Exception as e:
            logging.error(f"오류 발생: {e}")

        return pid

    def stop(self, pid) :
        # 로깅 설정
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

        # RabbitMQ 서버 실행 경로 설정
        rabbitmq_stop_command = os.path.join(System.rabbitmq_sbin_path, "rabbitmqctl.bat") + " stop"

        try:
            # RabbitMQ 서버 종료
            logging.info("RabbitMQ 서버를 종료합니다.")
            subprocess.run(rabbitmq_stop_command, shell=True, check=True)
            self.is_server_stopped(pid)

            logging.info("RabbitMQ 서버가 정상적으로 종료되었습니다.")

        except subprocess.CalledProcessError as e:
            logging.error(f"RabbitMQ 서버 종료에 실패했습니다: {e}")
        except Exception as e:
            logging.error(f"오류 발생: {e}")

    def reboot(self) :
        pid = self.stop()
        self.start(pid)

    # RabbitMQ 서버 시작 및 상태 확인 함수
    def start_rabbitmq_server(self, max_retries=10, wait_interval=1):
        command = os.path.join(System.rabbitmq_sbin_path, "rabbitmqctl.bat") + " start_app"

        def is_rabbitmq_running():
            try:
                # rabbitmqctl status 명령 실행
                result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                return result.returncode == 0  # 성공적으로 실행되면 서버가 실행 중
            except Exception as e:
                logging.error(f"서버 상태 확인 중 오류 발생: {e}")
                return False

        time.sleep(wait_interval)
        # 서버 준비 대기
        for _ in range(max_retries):
            if is_rabbitmq_running():
                logging.info("RabbitMQ 서버가 성공적으로 시작되었습니다.")
                return True
            logging.info("서버 시작 대기 중...")
            time.sleep(wait_interval)

        logging.error("RabbitMQ 서버 시작에 실패했습니다.")
        return False

    def is_server_stopped(self, pid, max_retries=10, wait_interval=1):
        def check_pid(pid):
            try:
                # pid에 시그널 0을 보냄으로써 프로세스 존재 여부 확인
                os.kill(pid, 0)
            except OSError:
                return True  # 프로세스가 존재하지 않으면 서버가 종료된 상태
            else:
                return False  # 프로세스가 존재하면 서버가 아직 실행 중

        # 서버가 종료될 때까지 대기
        for _ in range(max_retries):
            if check_pid(pid):
                logging.info("RabbitMQ 서버가 종료되었습니다.")
                return True
            logging.info("서버 종료 대기 중...")
            time.sleep(wait_interval)

        logging.error("서버가 여전히 실행 중입니다.")
        return False

# if __name__ == '__main__':
#     process_runner = ProcessRunner()
#     process_runner.run()