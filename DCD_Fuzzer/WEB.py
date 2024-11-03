from DCD_Fuzzer.data_model import Rabbit, logging
from DCD_Fuzzer.data_model import login_header, Default_header
import requests
from urllib.parse import urljoin
from requests.auth import HTTPBasicAuth


username = Rabbit.admin_ID
password = Rabbit.admin_PW
login_header = login_header

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Web_login:
    def admin_login(self):
        endpoint = "api/whoami"
        url = urljoin(Rabbit.host_url, endpoint)
        # 로그인 요청
        response = requests.get(url, headers=login_header, auth=HTTPBasicAuth(username, password))

        # 로그인 성공 여부 확인
        if response.status_code == 200:
            logging.info("로그인 성공!")
        else:
            logging.error(f"로그인 실패! 상태 코드: {response.status_code}")

def user_login(self,id, pw):
        endpoint = "api/whoami"
        url = urljoin(Rabbit.host_url, endpoint)
        # 로그인 요청
        response = requests.get(url, headers=login_header, auth=HTTPBasicAuth(id, pw))

        # 로그인 성공 여부 확인
        if response.status_code == 200:
            logging.info("로그인 성공!")
        else:
            logging.error(f"로그인 실패! 상태 코드: {response.status_code}")

if __name__ == '__main__':
    login()
    # add_user()
