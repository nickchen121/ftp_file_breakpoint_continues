import socketserver
import os
import struct
from lib import common
from conf import settings

logger = common.load_my_logging_cfg('server')


class MyHandler(socketserver.BaseRequestHandler):
    @staticmethod
    def get_filename_list():
        """获取db/server下的所有文件名"""
        filename_list = os.listdir(settings.SERVER_DB_PATH)

        return filename_list

    @staticmethod
    def get_file_content(filename, file_size):
        """通过文件名获取文件路径"""
        filename_path = os.path.join(settings.SERVER_DB_PATH, filename)
        with open(filename_path, 'rb') as fr:
            fr.seek(file_size, 0)
            file_content = fr.read(1024)

        return file_content

    @staticmethod
    def get_file_content_iter(filename, file_size):
        """通过文件名获取文件路径"""
        filename_path = os.path.join(settings.SERVER_DB_PATH, filename)
        with open(filename_path, 'rb') as fr:
            fr.seek(file_size, 0)
            while True:
                file_content = fr.read(10240)
                yield file_content

    @staticmethod
    def set_file_head(filename, file_size):
        """设计一个文件头"""
        filename_path = os.path.join(settings.SERVER_DB_PATH, filename)
        file_head = os.path.getsize(filename_path) - file_size
        file_head = struct.pack('i', file_head)

        return file_head

    def handle(self):
        print(f'{self.client_address}成功连接')
        logger.info(f'{self.client_address}成功连接')
        print(self.client_address)
        while True:
            try:
                # 发送文件列表
                data = self.request.recv(1024)
                if data.decode('utf8') == 'ls':
                    filename_list = self.get_filename_list()
                    self.request.send(str(filename_list).encode('utf8'))
                    logger.info(f'{self.client_address}查看文件列表')

                # 收到文件名
                filename, file_size = eval(self.request.recv(1024).decode('utf8'))
                logger.info(f'{self.client_address}下载文件{filename}')
                file_content = self.get_file_content(filename, file_size)

                # 发送文件
                file_head = self.set_file_head(filename, file_size)
                # 发送文件头
                self.request.send(file_head)

                # 发送文件内容
                for file in self.get_file_content_iter(filename, file_size):
                    self.request.send(file)
                logger.info(f'成功给{self.client_address}发送文件{filename}')

            except ConnectionResetError:
                break
        self.request.close()


if __name__ == '__main__':
    server = socketserver.ThreadingTCPServer(('192.168.11.210', 8000), MyHandler, bind_and_activate=True)
    print('start...')
    server.serve_forever()
