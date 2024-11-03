from DCD_Fuzzer.ProcessRunner import ProcessRunner
from DCD_Fuzzer.add_user_fun import add_rabbitmq_user
from DCD_Fuzzer.WEB import Web_login
from DCD_Fuzzer.data_model import logging, System
from DCD_Fuzzer.DCD_snapshot import backup_mnesia_folder

import tkinter as tk
from tkinter import scrolledtext
import time
import logging

class TextHandler(logging.Handler):
    """로그를 tkinter ScrolledText 위젯에 출력하는 핸들러"""

    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget

    def emit(self, record):
        # 로그 메시지 생성
        msg = self.format(record)
        # ScrolledText에 추가
        self.text_widget.insert(tk.END, msg + "\n")
        # 스크롤을 자동으로 아래로 이동
        self.text_widget.see(tk.END)

def loop(id, pw):
    Web_login().admin_login()
    add_rabbitmq_user(id, pw)
    time.sleep(1)
    ProcessRunner().reboot()

    if not Web_login.admin_login():
        logging.info("Trigger!!")
        logging.error("Failed to add user")
        backup_mnesia_folder()
        return Exception("Trigger!!")

    else:
        logging.info("Success to add user")
        logging.info("Success to login")

def start_process():
    with open(System.attck_path, "r") as file:
        total_lines = sum(1 for line in file)

    ProcessRunner().start()
    n = 0
    with open(System.attck_path, "r") as file:
        for line in file:
            line = line.strip()
            logging.info(f"{'='*10} Task {n} Start {'='*10}")
            logging.info(f"ID: Test_1_{n} PW: {line}")
            id = "Test_1_" + str(n)
            pw = line
            loop(id, pw)

            # GUI의 진행 상태 표시 업데이트
            update_progress(n, total_lines)
            n += 1

# GUI 설정
root = tk.Tk()
root.title("RabbitMQ Status Checker")
root.geometry("500x400")

# 로그 창
log_text = scrolledtext.ScrolledText(root, width=60, height=15)
log_text.pack(pady=10)

# 진행 상태 표시 라벨
progress_label = tk.Label(root, text="Progress: 0%", font=("Helvetica", 12))
progress_label.pack(pady=10)

def update_progress(current, total):
    percentage = int((current / total) * 100)
    progress_label.config(text=f"Progress: {percentage}%")
    root.update_idletasks()

# 시작 버튼
start_button = tk.Button(root, text="Start Process", command=start_process)
start_button.pack(pady=20)

root.mainloop()
