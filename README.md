# 文件上传-断点续传

文件上传时可能会异常终止,因此只下载了一部分,所以我们可以重新连接之后接着下载.

# 目录结构

|- client.py
|- server.py
|- conf
    |- settings.py
|- lib
    |- common.py
|- log
    |- log.log
|- db
    |- server_db
    |- client_db
|- README.md
|- requirement.txt

# client.py

发送指令给服务端,下载文件.

# server.py

实现并发的服务端,提供文件.

## 文件的多种状态

1. 全新的文件,未下载的文件
2. 下载一部分的文件
3. 下载完成的文件

# conf/settings.py

IP = ''
PORT = ''
BASE_PATH = ''
DB_PATH = ''
CLIENT_DB_PATH = ''
SERVER_DB_PATH = ''
LOG_PATH = ''

日志的模板

# lib/common.py

通用模板,如:日志.

# log/log.log

记录日志,**按天新增文件**

# db

存储客户端/服务端数据


1. ls