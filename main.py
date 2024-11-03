from DCD_Fuzzer.ProcessRunner import ProcessRunner
from DCD_Fuzzer.add_user_fun import add_rabbitmq_user
from DCD_Fuzzer.WEB import Web_login
from DCD_Fuzzer.data_model import logging, System
from DCD_Fuzzer.DCD_snapshot import backup_mnesia_folder

import re
import subprocess
import tkinter as tk
from tkinter import scrolledtext
from tqdm import tqdm
import time
import threading
import logging

# Rabbit 시작
# 관리 사용자가 일반 유저 추가 -> 성공 -> Rabbit 재시작 -> 성공 -> 관리사용자 로그인 -> 성공
# 관리 사용자가 일반 유저 추가 -> 성공 -> Rabbit 재시작 -> 성공 -> 관리사용자 로그인 -> 성공
# 관리 사용자가 일반 유저 추가 -> 성공 -> Rabbit 재시작 -> 성공 -> 관리사용자 로그인 -> 실폐 -> 백업 및 데이터 저장 -> 종료

def loop(id,pw):
    Web_login.admin_login()
    add_rabbitmq_user(id, pw)
    time.sleep(1)
    ProcessRunner().reboot()

    if not Web_login.admin_login():
        logging.info("Trigger!!")
        logging.error("Failed to add user")
        backup_mnesia_folder()
        return Exception("Trigger!!")

    else :
        logging.info("Success to add user")
        logging.info("Success to login")



# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_rabbitmqctl():
    result = subprocess.run(['rabbitmqctl', 'status'], capture_output=True, text=True)
    pid_match = re.search(r'OS PID:\s+(\d+)', result.stdout)
    if pid_match:
        pid = pid_match.group(1)
        log_message = f"Extracted PID: {pid}"
    else:
        log_message = "PID not found in the output."

    logging.info(log_message)
    log_text.insert(tk.END, f"{log_message}\n")
    log_text.see(tk.END)

def run_with_progress():
    for _ in tqdm(range(1), desc="Running rabbitmqctl status"):
        time.sleep(0.1)  # tqdm 표시를 위한 짧은 대기 시간
    run_rabbitmqctl()

def start_process():
    threading.Thread(target=run_with_progress).start()

# GUI 설정
root = tk.Tk()
root.title("RabbitMQ Status Checker")
root.geometry("500x300")

# 로그 창
log_text = scrolledtext.ScrolledText(root, width=60, height=15)
log_text.pack(pady=10)

# 실행 버튼
start_button = tk.Button(root, text="Start", command=start_process)
start_button.pack()

root.mainloop()

