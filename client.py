import os
import struct
from socket import *
from conf import settings
from lib import common

logger = common.load_my_logging_cfg('client')

client = socket()
client.connect(('192.168.11.210', 8000))


def save_file_content(filename, file_content):
    """保存文件内容"""
    file_path = os.path.join(settings.CLIENT_DB_PATH, filename)
    with open(file_path, 'ab') as fw:
        fw.write(file_content)


while True:

    # 接收文件列表
    client.send('ls'.encode('utf8'))

    file_list = client.recv(1024)
    print('请选择下列文件进行下载:')
    file_list = eval(file_list.decode('utf8'))
    for ind, val in enumerate(file_list):
        print(ind, val)

    # 选择文件
    file_choice = input('请选择你需要下载的文件:')  # 0
    filename = file_list[int(file_choice)]  # type:str

    # 发送文件和文件大小
    file_path = os.path.join(settings.CLIENT_DB_PATH, filename)
    if os.path.exists(file_path):
        file_size = os.path.getsize(file_path)
        client.send(str((filename, file_size)).encode('utf8'))
    else:
        client.send(str((filename, 0)).encode('utf8'))

    # 接收文件并保存
    # 接收文件头
    file_head = client.recv(4)
    file_head = struct.unpack('i', file_head)[0]  # file_size

    # 接收文件内容
    recv_size = 0
    while recv_size <= file_head:
        file_content = client.recv(10240)
        recv_size += 10240
        print('recv_size:', recv_size)
        save_file_content(filename, file_content)

    logger.info(f'{filename}下载成功')
    print('保存成功')
