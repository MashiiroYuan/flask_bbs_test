from flask import Flask
from apps.cms import bp as cms_bp
from apps.common import bp as common_bp
from apps.front import bp as front_bp
from apps.ueditor import bp as ueditor_bp
import config
from exts import db, mail,alidayu
from flask_wtf import CSRFProtect
from utils.captcha import Captcha

Captcha.gene_graph_captcha()

app = Flask(__name__)
# 将config 注册

app.config.from_object(config)

# 将蓝图注册进app
app.register_blueprint(cms_bp)
app.register_blueprint(front_bp)
app.register_blueprint(common_bp)
app.register_blueprint(ueditor_bp)

db.init_app(app)
mail.init_app(app)
CSRFProtect(app)
#初始化发送短信
alidayu.init_app(app)



if __name__ == '__main__':
    # app = create_app()
    app.run(debug=True)
