import os.path
from traceback import print_exception

import json
import logging
from datetime import datetime
from requests.auth import HTTPBasicAuth
import configparser
from root_path import project_root_path

config_path = os.path.join(project_root_path, "config.ini")
json_path = os.path.join(project_root_path, "DCD_Fuzzer", "json")

if os.path.exists(config_path):
    config = configparser.ConfigParser()
    config.read(config_path, encoding="utf-8")
else:
    print("config.ini is not exist")
    exit(1)


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
    mnesia_path = config['System']['mnesia_path']
    backup_base_path = config['System']['backup_base_path']

    attck_path = config['System']['attck_path']


# 로깅 설정 (파일에 기록)
current_time = datetime.now().strftime("%Y%m%d_%H%M%S")  # 예: "20241102_101530"
log_file_name = f"DCD_Fuzzer_{current_time}.log"
log_file_path = os.path.join(System.log_file_path, log_file_name)
logging.basicConfig(
    filename=log_file_path,
    level= System.log_level,
    format='%(asctime)s - %(levelname)s - %(message)s',
)

with open(os.path.join(json_path,"login.json"), "r") as file:
    login_header = json.load(file)
with open(os.path.join(json_path,"Default.json"), "r") as file:
    Default_header = json.load(file)
