from __init__ import Rabbit, logging
from __init__ import login_header, Default_header
import requests
from urllib.parse import urljoin
from requests.auth import HTTPBasicAuth


username = Rabbit.admin_ID
password = Rabbit.admin_PW
login_header = login_header


def login():
    endpoint = "api/whoami"
    url = urljoin(Rabbit.host_url, endpoint)
    # 로그인 요청
    response = requests.get(url, headers=login_header, auth=HTTPBasicAuth(username, password))

    # 로그인 성공 여부 확인
    if response.status_code == 200:
        print("로그인 성공!")
        # 쿠키 출력
        response = response.cookies
        for cookie in response:
            print(f"{cookie.name} = {cookie.value}")
    else:
        print(f"로그인 실패! 상태 코드: {response.status_code}")

def add_user():
    endpoint = "api/users/tset_name"
    url = urljoin(Rabbit.host_url, endpoint)

    # 새 사용자 정보
    data = {
        "username": "tset_name11",
        "password": "test_passwd11",
        "tags": "administrator"
    }


    # 요청 보내기 (PUT 요청)
    response = requests.put(url, headers=Default_header, json=data, auth=HTTPBasicAuth(Rabbit.admin_ID, Rabbit.admin_PW))
    print(response.headers)
    print(response.text)
    # 응답 결과 확인
    if response.status_code == 201:
        print("유저 생성 성공!")
    elif response.status_code == 204:
        print("유저가 이미 존재하여 정보가 업데이트되었습니다.")
    else:
        print(f"유저 생성 실패! 상태 코드: {response.status_code}")
        print("응답 내용:", response.text)

# if __name__ == '__main__':
#     # login()
#     add_user()
