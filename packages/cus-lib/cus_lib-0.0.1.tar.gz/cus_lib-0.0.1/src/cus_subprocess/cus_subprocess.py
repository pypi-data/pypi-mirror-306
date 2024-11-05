from src import cus_subprocess


def run(command):
    # 创建不显示窗口的 startupinfo
    startupinfo = cus_subprocess.STARTUPINFO()
    startupinfo.dwFlags |= cus_subprocess.STARTF_USESHOWWINDOW

    try:
        cus_subprocess.run(command, startupinfo=startupinfo, shell=True)
    except Exception as e:
        print(f"调用subprocess{e}")
