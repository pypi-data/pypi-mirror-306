from webdriver_manager.microsoft import EdgeChromiumDriverManager
import os
import shutil
import sys




def download_driver():
    folder_path = r'./'
    file_path = os.path.join(folder_path, 'msedgedriver.exe')
    if os.path.exists(file_path):
        os.remove(file_path)
    download_driver_path = EdgeChromiumDriverManager().install()
    print(download_driver_path)
    shutil.move(download_driver_path, folder_path)
    return folder_path



class NullDevice:
    """一个哑设备，用于重定向输出"""
    def write(self, s):
        pass

    def flush(self):
        pass

# 重定向stdout的函数
def redirect_stdout():
    sys.stdout = NullDevice()


def restore_stdout():
    sys.stdout = sys.__stdout__



