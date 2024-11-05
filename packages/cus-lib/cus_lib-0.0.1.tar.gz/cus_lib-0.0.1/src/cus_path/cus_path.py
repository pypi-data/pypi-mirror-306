import os, sys


def __get_tmp_path():
    """
    获取程序运行时的临时文件
    :return:
    """
    # 如果是从可执行文件运行，获取可执行文件的路径
    if getattr(sys, "frozen", False):
        return sys._MEIPASS
    else:
        # 如果是从源代码运行，获取当前脚本的路径
        return os.path.dirname(os.path.abspath(__file__))


def get_tmp_src_path(src):
    """
    获取src拼接临时目录的全路径
    :param src:
    :return:
    """
    return os.path.join(__get_tmp_path(), src)


def __get_current_file_path():
    """
    获取exe或者脚本的路径
    :return:
    """
    # 如果是从可执行文件运行，获取可执行文件的路径
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    else:
        # 如果是从源代码运行，获取当前脚本的路径
        return os.path.dirname(os.path.abspath(__file__))


def get_src_path(src):
    """
    获取资源路径
    :param src:
    :return:
    """
    return os.path.join(__get_current_file_path(), src)


def has(file_or_dir_path):
    """
    是否有某个文件/目录
    :param file_or_dir_path:
    :return:
    """
    return os.path.exists(file_or_dir_path)


if __name__ == '__main__':
    print(has("c:/1.txt"))
    print(has(r"/"))
