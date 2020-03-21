from io import BytesIO

from flask import Blueprint, request, make_response
from utils import restful,zlcache
from exts import alidayu
from utils.captcha import Captcha
from .forms import SmsCaptchaForm

bp = Blueprint("common", __name__, url_prefix='/common')  # 域名

'''旧版本 发送短信'''


# @bp.route('/sms_captcha/')
# def sms_captcha():
#     # /?telephone=xxx
#     # /c/sms_captcha/xxx
#     # 加密短信端口 防止被攻击
#     telephone = request.args.get('telephone')
#     if not telephone:
#         return restful.params_error(message='请输入手机号码')
#     captcha=Captcha.gene_text(number=4)
#     if alidayu.send_sms(telephone,code=captcha):
#         return restful.success()
#     else:
#         # 测试是否成功发送短信
#         # return restful.params_error(message='短信发送失败')
#         return restful.success()

'''短信验证码验证'''
@bp.route('/sms_captcha/', methods=['POST'])
def sms_captcha():
    # /?telephone=xxx
    # /c/sms_captcha/xxx
    # 加密短信端口 防止被攻击
    form = SmsCaptchaForm(request.form)
    if form.validate():
        telephone = form.telephone.data
        captcha = Captcha.gene_text(number=4)
        print('message',captcha)
        if alidayu.send_sms(telephone, code=captcha):
            zlcache.set(telephone,captcha)
            return restful.success()
        else:
            # 正式显示error
            # return restful.params_error()
            zlcache.set(telephone,captcha)
            return restful.success()
    else:
        return restful.params_error(message='参数错误')

'''图形验证码'''
@bp.route('/captcha/')
def graph_captcha():
    text, image = Captcha.gene_graph_captcha()
    out = BytesIO()
    zlcache.set(text.lower(),text.lower())
    image.save(out, 'png')
    out.seek(0)
    resp = make_response(out.read())
    resp.content_type = 'image/png'
    return resp
