from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from utils.alidayu import AlidayuAPI


#创建发送短信的接口
alidayu=AlidayuAPI()
db=SQLAlchemy()
mail=Mail()