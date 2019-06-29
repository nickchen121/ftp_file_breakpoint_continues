import os

IP = '192.168.11.210'
PORT = 8000
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_PATH, 'db')
CLIENT_DB_PATH = os.path.join(DB_PATH, 'client')
SERVER_DB_PATH = os.path.join(DB_PATH, 'server')
LOG_PATH = os.path.join(BASE_PATH, 'log')





