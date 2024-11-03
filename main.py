from DCD_Fuzzer.ProcessRunner import ProcessRunner
from DCD_Fuzzer.add_user_fun import add_rabbitmq_user
from DCD_Fuzzer.WEB import Web_login
from DCD_Fuzzer.data_model import logging, System
from DCD_Fuzzer.DCD_snapshot import backup_mnesia_folder

from tqdm import tqdm
import time

# Rabbit 시작
# 관리 사용자가 일반 유저 추가 -> 성공 -> Rabbit 재시작 -> 성공 -> 관리사용자 로그인 -> 성공
# 관리 사용자가 일반 유저 추가 -> 성공 -> Rabbit 재시작 -> 성공 -> 관리사용자 로그인 -> 성공
# 관리 사용자가 일반 유저 추가 -> 성공 -> Rabbit 재시작 -> 성공 -> 관리사용자 로그인 -> 실폐 -> 백업 및 데이터 저장 -> 종료

def loop(id,pw):
    Web_login().admin_login()
    add_rabbitmq_user(id, pw)
    time.sleep(1)
    ProcessRunner().reboot()

    if not Web_login().admin_login():
        logging.info("Trigger!!")
        logging.error("Failed to login adminUser")
        backup_mnesia_folder()
        return Exception("Trigger!!")

    else :
        logging.info("Success to add user")
        logging.info("Success to login")



if __name__ == '__main__':
    with open(System.attck_path, "r") as file:
        total_lines = sum(1 for line in file)

    ProcessRunner().start()
    n = 0
    with open(System.attck_path, "r") as file:
        for line in tqdm(file, total=total_lines, desc="Reading lines"):
            line = line.strip()
            tqdm.write(f"PW: {line}")  # tqdm 바 외부에 출력하는 방법도 있음
            logging.info(f"{"="*10} Task {n} Start {"="*10}")
            logging.info(f"ID: Test_1_{n} PW: {line}")
            id = f"Test_1_{n}"
            pw = line
            loop(id,pw)
            n=n+1

