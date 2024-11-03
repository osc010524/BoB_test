import requests
from requests.auth import HTTPBasicAuth

from DCD_Fuzzer.data_model import Rabbit

# RabbitMQ 관리자 계정 정보
admin_user = Rabbit.admin_ID  # 관리자 계정 ID
admin_pass = Rabbit.admin_PW  # 관리자 계정 비밀번호

# mnesia database
mdata = '\x00jbWLAƒh\x06w\x0dinternal_userm\x00\x00\x00\x04userm\x00\x00\x00$\x1dn%F‰ÌK%DÏ\xcc@?’‹"¿äô8¯,¨×°â.Ž\x90\x0büW\x15¡i\x1fjw\x7erabbit_password_hashing_sha256t\x00\x00\x00\x00\x00\x00'

# 새로 추가할 유저 정보
new_user = "m\x00"
new_password = "user"
tags = "management"  # 유저 권한 (예: "administrator", "management", "monitoring")

# RabbitMQ 서버 URL (관리 포트: 15672)
rabbitmq_url = f"{Rabbit.host_url}api/users/{new_user}"

# HTTP PUT 요청 데이터 (유저 추가 정보)
data = {
    "password": new_password,
    "tags": tags
}

# 유저 추가 요청
response = requests.put(rabbitmq_url, json=data, auth=HTTPBasicAuth(admin_user, admin_pass))

# 결과 확인
if response.status_code == 204:
    print(f"User '{new_user}' added successfully.")
else:
    print(f"Failed to add user. Status code: {response.status_code}, Response: {response.text}")
