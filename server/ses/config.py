# config.py

SECRET_KEY = 'dev'

USERNAME = 'root'
PASSWORD = '000000'
HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'test_db'
# database type and driver
DIALECT = 'mysql'
DRIVER = 'pymysql'
# 连接数据的URI
DB_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT, DRIVER, USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)

SQLALCHEMY_DATABASE_URI = DB_URI

SQLALCHEMY_TRACK_MODIFICATIONS = True

SWAGGER_TITLE = "API"
SWAGGER_DESC = "API接口"
# 地址，必须带上端口号
SWAGGER_HOST = "localhost:5000"