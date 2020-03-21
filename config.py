import os

# s设置SECRETKEY
SECRET_KEY = os.urandom(24)

DEBUG = True
USERNAME = 'root'
PASSOWRD = '111111'
HOST = '127.0.0.1'
PORT = '3306'
NAME = 'first'

DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSOWRD, HOST, PORT, NAME)

SQLALCHEMY_DATABASE_URI = DB_URI
# 更改数据库就发送信号
SQLALCHEMY_TRACK_MODIFICATIONS = False

CMS_USER_ID = 'jisfa'

FRONT_USER_ID='jiums'

# flask_email参数
# qq mail Tls 587 ssl 465 不支持非加密
MAIL_SERVER = 'smtp.qq.com'
MAIL_PORT = '587'
MAIL_USE_TLS = True
# MAIL_USE_SSL : default False
# MAIL_DEBUG =default app.debug
MAIL_USERNAME = '987639797@qq.com'
MAIL_PASSWORD = 'sqklhjzdxoulbfij'  # 申请sqklhjzdxoulbfij
MAIL_DEFAULT_SENDER = '987639797@qq.com'

# 阿里大于 短信配置
ALIDAYU_APP_KEY = ''
ALIDAYU_APP_SECRET = ''
ALIDAYU_SIGN_NAME = ''
ALIDAYU_TEMPLATE_CODE = 'sms_68465012'
