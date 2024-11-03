import shutil
import os
from datetime import datetime
from tkinter import Scale

from DCD_Fuzzer.data_model import System, logging

def backup_mnesia_folder():
    """
    Mnesia 폴더를 지정된 백업 경로로 복사하여 백업하는 함수.

    Parameters:
        None
    Returns:
        str: 백업 파일의 최종 경로
    """

    mnesia_path = System.mnesia_path
    backup_base_path = System.backup_base_path

    # 현재 날짜와 시간을 이용하여 백업 폴더 이름 생성
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(backup_base_path, f"mnesia_backup_{timestamp}")

    try:
        shutil.copytree(mnesia_path, backup_path)
        logging.info(f"The Mnesia folder has been successfully backed up.: {backup_path}")
        return True
    except Exception as e:
        logging.error(f"An error occurred during backup: {e}")
        return Exception

