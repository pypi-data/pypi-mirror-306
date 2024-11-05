import os
import tempfile


def replace_extension(file_path, new_extension):
    # 分离路径和扩展名，然后拼接新的扩展名
    base = os.path.splitext(file_path)[0]
    return f"{base}{new_extension}"


def delete_file(file_path):
    # 检查文件是否存在，然后删除
    if os.path.exists(file_path):
        os.remove(file_path)


def create_temp_file(content: str, auto_del=False):
    """
    创建临时文件写入content并获取路径
    :param content:要写入的内容
    :param auto_del: 是否自动删除临时文件
    :return:
    """
    temp_file = tempfile.NamedTemporaryFile(delete=auto_del)  # 不自动删除
    temp_file.write(content)  # 写入初始内容
    temp_file.close()  # 关闭文件
    return temp_file.name  # 返回文件路径
