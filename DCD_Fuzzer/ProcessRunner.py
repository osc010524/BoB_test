import subprocess
import time
import os
from turtledemo.clock import setup
import re


from DCD_Fuzzer.data_model import logging, System

import psutil

def is_pid_alive(pid):
    """주어진 PID가 살아있는지 확인"""
    return psutil.pid_exists(pid)

class ProcessRunner():
    def __init__(self):
        pass
    def run(self):

        # 로깅 설정
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

        # RabbitMQ 서버 실행 경로 설정
        rabbitmq_start_command = os.path.join(System.rabbitmq_sbin_path, "rabbitmq-server.bat")
        rabbitmq_start_command = "start cmd /c" + rabbitmq_start_command
        rabbitmq_stop_command = os.path.join(System.rabbitmq_sbin_path, "rabbitmqctl.bat") + " stop"
        rabbitmq_stop_command = "start cmd /c" + rabbitmq_stop_command

        try:
            # RabbitMQ 서버 시작
            logging.info("RabbitMQ Server Start.")
            server_process = subprocess.Popen(rabbitmq_start_command, shell=False)

            time.sleep(1)  # 필요에 따라 서버가 준비될 때까지 기다립니다
            logging.info("The RabbitMQ server started successfully.")

            # time.sleep(1)  # 필요에 따라 서버가 준비될 때까지 기다립니다
            # RabbitMQ 서버 종료
            logging.info("Shut down the RabbitMQ server.")
            subprocess.run(rabbitmq_stop_command, shell=False, check=True)
            logging.info("RabbitMQ server terminated normally")

        except subprocess.CalledProcessError as e:
            logging.error(f"RabbitMQ server shutdown failed: {e}")
        except Exception as e:
            logging.error(f"오류 발생: {e}")

    def start(self) :
        # 로깅 설정
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

        # RabbitMQ 서버 실행 경로 설정
        rabbitmq_start_command = os.path.join(System.rabbitmq_sbin_path, "rabbitmq-server.bat")+ " -detached"

        try:
            # RabbitMQ 서버 시작
            logging.info("RabbitMQ Server start.")
            server_process = subprocess.Popen(rabbitmq_start_command, shell=False)
            pid = server_process.pid

            # 서버가 시작되고 실행되는 동안 대기 (여기서는 10초 대기)
            if not self.start_rabbitmq_server():
                logging.error("RabbitMQ server startup failed.")
            else:
                logging.info("The RabbitMQ server started successfully.")

        except subprocess.CalledProcessError as e:
            logging.error(f"RabbitMQ server failed to start: {e}")
        except Exception as e:
            logging.error(f"Error: {e}")


    def stop(self, pid) :
        # 로깅 설정
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

        # RabbitMQ 서버 실행 경로 설정
        rabbitmq_stop_command = os.path.join(System.rabbitmq_sbin_path, "rabbitmqctl.bat")

        try:
            # RabbitMQ 서버 종료
            logging.info("Shut down the RabbitMQ server")
            subprocess.run(rabbitmq_stop_command, shell=False, check=True)
            self.is_server_stopped(pid)

            logging.info("RabbitMQ server terminated normally.")

        except subprocess.CalledProcessError as e:
            logging.error(f"RabbitMQ server shutdown failed: {e}")
        except Exception as e:
            logging.error(f"오류 발생: {e}")

    def kill_pocess(self) :
        pid = self.get_pid()
        if pid != None and type(pid) == int :
            # pid에 시그널 9를 보내 프로세스 강제 종료
            try:
                subprocess.run(["taskkill", "/PID", str(pid), "/F"], check=True)
            except:
                Exception("RabbitMQ process termination failed")

        if not is_pid_alive(pid):
            logging.info("The process ended successfully.")
        else:
            logging.error("The process has not terminated.")
            Exception("RabbitMQ process termination failed")

    def get_pid(self) :
        # RabbitMQ 서버 실행 경로 설정
        rabbitmq_pid_command = os.path.join(System.rabbitmq_sbin_path, "rabbitmqctl.bat") + " status"
        _pid = None
        try:
            # RabbitMQ 서버 시작
            result = subprocess.run(rabbitmq_pid_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            pid_match = re.search(rb'OS PID:\s+(\d+)', result.stdout)
            if pid_match:
                _pid = int(pid_match.group(1))
                logging.info(f"RabbitMQ 서버 PID: {_pid}")
            else:
                logging.error("PID not found in the output.")
                Exception("PID not found in the output.")
                
        except subprocess.CalledProcessError as e:
            logging.error(f"RabbitMQ server PID not found: {e}")
            return False
        except Exception as e:
            logging.error(f"오류 발생: {e}")
        else:
            if _pid == None :
                return True
            else :
                return _pid

    def reboot(self) :
        self.kill_pocess()
        time.sleep(1)
        self.start()

# RabbitMQ 서버 시작 및 상태 확인 함수
    def start_rabbitmq_server(self, max_retries=1, wait_interval=1):
        command = os.path.join(System.rabbitmq_sbin_path, "rabbitmqctl.bat") + " start_app"

        def is_rabbitmq_running():
            try:
                # rabbitmqctl status 명령 실행
                result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                return result.returncode == 0  # 성공적으로 실행되면 서버가 실행 중
            except Exception as e:
                logging.error(f"Error occurred while checking server status: {e}")
                return False

        time.sleep(wait_interval)
        # 서버 준비 대기
        for _ in range(max_retries):
            if is_rabbitmq_running():
                logging.info("RabbitMQ server started successfully")
                return True
            logging.info("Waiting for server to start...")
            time.sleep(wait_interval)

        logging.error("RabbitMQ server failed to start.")
        return False

    def is_server_stopped(self, pid, max_retries=1, wait_interval=1):
        def check_pid(pid):
            try:
                if pid == True:
                    return True
                elif pid == False:
                    return False
                elif pid == None:
                    return True
                else:
                    # pid에 시그널 0을 보냄으로써 프로세스 존재 여부 확인
                    subprocess.run(["taskkill", "/PID", str(pid), "/F"], check=True)
            except OSError:
                return True  # 프로세스가 존재하지 않으면 서버가 종료된 상태
            except subprocess.CalledProcessError:
                return True
            else:
                return False  # 프로세스가 존재하면 서버가 아직 실행 중

        time.sleep(wait_interval)
        # 서버가 종료될 때까지 대기
        for _ in range(max_retries):
            if check_pid(pid):
                logging.info("RabbitMQ server terminated.")
                return True
            logging.info("Waiting for server shutdown...")
            time.sleep(wait_interval)

        logging.error("The server is still running.")
        return False

if __name__ == '__main__':
    # process_runner = ProcessRunner()
    # process_runner.run()
    # pid=ProcessRunner().get_pid()
    # print(pid)
    ProcessRunner().kill_pocess()

    pass