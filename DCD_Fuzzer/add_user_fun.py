from site import ENABLE_USER_SITE

import requests
from requests.auth import HTTPBasicAuth
from DCD_Fuzzer.data_model import Rabbit
from DCD_Fuzzer.data_model import logging

def add_rabbitmq_user(new_user, new_password, tags="management"):
    """
    RabbitMQ에 새 유저를 추가하는 함수.

    Parameters:
        new_user (str): 추가할 유저 이름
        new_password : 추가할 유저 비밀번호
        tags (str): 유저 권한 (기본값: "management")

    Returns:
        str: 성공 또는 실패 메시지
    """
    # RabbitMQ 관리자 계정 정보 및 서버 URL
    admin_user = Rabbit.admin_ID
    admin_pass = Rabbit.admin_PW
    rabbitmq_url = f"{Rabbit.host_url}api/users/{new_user}"

    # HTTP PUT 요청 데이터 (유저 추가 정보)
    data = {
        "password": new_password,
        "tags": tags
    }

    try:
        response = requests.put(rabbitmq_url, json=data, auth=HTTPBasicAuth(admin_user, admin_pass))

        if 200 <= response.status_code < 300:
            logging.info(f"User '{new_user}' added successfully.")
            return True
        else:
            logging.error(f"Failed to add user. Status code: {response.status_code}, Response: {response.text}")
            return False
    except requests.RequestException as e:
        logging.error(f"An error occurred: {e}")
        return Exception



# # 사용 예제
# new_user = "m\x00"
# new_password = "user"
#
# result = add_rabbitmq_user(new_user, new_password)
# print(result)
