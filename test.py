from DCD_Fuzzer.__init__ import *
import requests


def check_print(tag, plan, status):
    if status:
        status_str = "Success"
    else:
        status_str = "Fail"
    print(f"{tag} check : ({status}) {plan}")


class TestRequest():
    def test_check_website_status(self, mock_get):
        tage = "Website"
        stat = False
        mock_get.return_value.status_code = 200
        response = requests.get(Rabbit.host_url)
        if response.status_code == 200:
            stat = True
        else:
            stat = False

        check_print("tage", "Website status is 200", stat)

        return stat

    def test_check_admin_login_status(self, mock_get):
        tage = "Admin Login"
        stat = False
        mock_get.return_value.status_code = 200
        response = requests.get(Rabbit.host_url, auth=Rabbit.get_bs64_auth())
        if response.status_code == 200:
            stat = True
        else:
            stat = False

        check_print(tage, "Admin login status is 200", stat)

        return stat



class TestSystem():
    def check_sbin_path(self):
        tage = "sbin_path"
        stat = False

        if os.path.exists(System.rabbitmq_sbin_path):
            stat = True
        else:
            stat = False

        check_print("sbin_path", "sbin_path is exist", stat)

        return stat

    def check_log_file_path(self):
        tage = "log_file"
        stat = False
        if os.path.exists(System.log_file_path):
            stat = True
        else:
            stat = False

        check_print("log_file_path", "log_file_path is exist", stat)

        return stat

    def check_rabbit_stat(self):
        tage = "rabbit_stat"
        stat = False
        if os.path.exists(System.rabbitmq_sbin_path, "rabbitmq-server.bat"):
            stat = True
        else:
            stat = False

        check_print("rabbit_stat", "rabbit_stat is exist", stat)

        return stat

    def check_rabbit_stop(self):
        tage = "rabbit_stop"
        stat = False
        if os.path.exists(System.rabbitmq_sbin_path, "rabbitmqctl.bat"):
            stat = True
        else:
            stat = False

        check_print("rabbit_stop", "rabbit_stop is exist", stat)

        return stat

if __name__ == '__main__':
    test_request = []

    print("="*50)
    print("Test Start")

    test_request = TestRequest()
    test_request.test_check_website_status()
    test_request.test_check_admin_login_status()

    test_system = TestSystem()
    test_system.check_sbin_path()
    test_system.check_log_file_path()
    test_system.check_rabbit_stat()
    test_system.check_rabbit_stop()

