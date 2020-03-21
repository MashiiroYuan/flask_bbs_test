from wtforms import Form, StringField, IntegerField
from wtforms.validators import Email, InputRequired, Length, EqualTo
from apps.forms import BaseForm
from utils import zlcache
from wtforms import ValidationError  # c表单错误
from flask import g  # 导入g对象


# 登陆验证
class LoginForm(BaseForm):
    email = StringField(validators=[Email(message='请输入正确的邮箱格式'), InputRequired(message='请输入邮箱')])
    # 注意这里设置的密码长度 过少或超出都会报错
    password = StringField(validators=[Length(3, 20, message='请输入正确格式密码')])
    remember = IntegerField()


# 密码验证
class ResetpwdForm(BaseForm):
    oldpwd = StringField(validators=[Length(5, 20, message='请输入正确格式旧密码')])
    newpwd = StringField(validators=[Length(5, 20, message='请输入正确格式新密码')])
    newpwd2 = StringField(validators=[EqualTo('newpwd', message='确认密码必须和新密码保持一致')])


# 邮箱的
class ResetEmailForm(BaseForm):
    email = StringField(validators=[Email(message='请输入正确格式邮箱')])
    captcha = StringField(validators=[Length(min=6, max=6, message='请输入正确长度验证码')])

    def validate_captcha(self, field):
        # field <input id="captcha" name="captcha" type="text" value="3pmznl">
        captcha = field.data
        print('captcha', self.captcha.data)
        print('field', field)
        print('captcha', captcha)
        email = self.email.data
        captcha_cache = zlcache.get(email)
        if not captcha_cache or captcha.lower() != captcha_cache.lower():
            raise ValidationError("验证码错误")

    def validate_email(self, field):
        print('email', field, field.data)
        email = field.data
        user = g.cms_user
        if user.email == email:
            raise ValidationError('不能修改为相同的邮箱')


# 轮播图验证
class AddBannerForm(BaseForm):
    name = StringField(validators=[InputRequired(message='请输入轮播图名称！')])
    image_url = StringField(validators=[InputRequired(message='请输入轮播图图片链接！')])
    link_url = StringField(validators=[InputRequired(message='请输入轮播图跳转链接！')])
    priority = IntegerField(validators=[InputRequired(message='请输入轮播图优先级！')])


# 更新轮播图
class UpdateBannnerForm(AddBannerForm):
    banner_id = IntegerField(validators=[InputRequired(message='输入轮播图id')])
