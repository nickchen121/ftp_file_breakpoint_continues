import os
import struct
from socket import *
from lib import common
from conf import settings

logger = common.load_my_logging_cfg('server')

server = socket()
server.bind((settings.IP, settings.PORT))
server.listen(5)


def get_filename_list():
    """获取db/server下的所有文件名"""
    filename_list = os.listdir(settings.SERVER_DB_PATH)

    return filename_list


def get_file_content(filename, file_size):
    """通过文件名获取文件路径"""
    filename_path = os.path.join(settings.SERVER_DB_PATH, filename)
    with open(filename_path, 'rb') as fr:
        fr.seek(file_size, 0)
        file_content = fr.read(1024)

    return file_content


def get_file_content_iter(filename, file_size):
    """通过文件名获取文件路径"""
    filename_path = os.path.join(settings.SERVER_DB_PATH, filename)
    with open(filename_path, 'rb') as fr:
        fr.seek(file_size, 0)
        while True:
            file_content = fr.read(10240)
            yield file_content


def set_file_head(filename, file_size):
    """设计一个文件头"""
    filename_path = os.path.join(settings.SERVER_DB_PATH, filename)
    file_head = os.path.getsize(filename_path) - file_size
    file_head = struct.pack('i', file_head)

    return file_head


print('start...')
while True:
    conn, client_addr = server.accept()
    print(client_addr)
    while True:
        try:
            # 发送文件列表
            data = conn.recv(1024)
            if data.decode('utf8') == 'ls':
                filename_list = get_filename_list()
                conn.send(str(filename_list).encode('utf8'))
                logger.info(f'{client_addr}查看文件列表')

            # 收到文件名
            filename, file_size = eval(conn.recv(1024).decode('utf8'))
            logger.info(f'{client_addr}下载文件{filename}')
            file_content = get_file_content(filename, file_size)

            # 发送文件
            file_head = set_file_head(filename, file_size)
            # 发送文件头
            conn.send(file_head)

            # 发送文件内容
            for file in get_file_content_iter(filename, file_size):
                conn.send(file)
            logger.info(f'成功给{client_addr}发送文件{filename}')

        except ConnectionResetError:
            break
    conn.close()
