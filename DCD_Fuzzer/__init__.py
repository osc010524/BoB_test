import os.path
import json
import logging
from datetime import datetime
from requests.auth import HTTPBasicAuth
import configparser

if os.path.exists("../config.ini"):
    config = configparser.ConfigParser()
    config.read("../config.ini")


class Rabbit:
    host_url = config['Rabbit']['host_url']
    admin_ID = config['Rabbit']['admin_ID']
    admin_PW = config['Rabbit']['admin_PW']

    def get_bs64_auth(self):
        bs64_auth = HTTPBasicAuth(Rabbit.admin_ID, Rabbit.admin_PW)
        return bs64_auth


class System:
    log_level = getattr(logging, config['System']["log_level"].upper(), logging.INFO)
    log_file_path = config['System']['log_file_path']
    rabbitmq_sbin_path = config['System']['rabbitmq_sbin_path']


# 로깅 설정 (파일에 기록)
current_time = datetime.now().strftime("%Y%m%d_%H%M%S")  # 예: "20241102_101530"
logging.basicConfig(
    filename=os.path.join(System.log_file_path, f"DCD_Fuzzer_{current_time}.log"),
    level= System.log_level,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(System.log_file_path),
        logging.StreamHandler()
    ]
)

with open("./json/login.json", "r") as file:
    login_header = json.load(file)
with open("./json/Default.json", "r") as file:
    Default_header = json.load(file)
