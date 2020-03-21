from flask import Blueprint, views, render_template, request, make_response,session,url_for
from io import BytesIO
from utils.captcha import Captcha
from .forms import SignupForm,SigninForm
from utils import restful, safeutils
from exts import db
from .models import FrontUser

from ..models import BannerModel
import config
bp = Blueprint("front", __name__, )  # 域名


@bp.route('/')
def index():
    banners = BannerModel.query.order_by(BannerModel.priority.desc()).limit(4)
    context = {
        'banners': banners
    }
    return render_template('front/front_index.html',**context)


class SignupView(views.MethodView):
    def get(self):
        # 注册完成后返回上一层页面
        return_to = request.referrer
        # safeutils防止返回值被劫持
        if return_to and return_to != request.url and safeutils.is_safe_url(return_to):

            return render_template('front/front_signup.html', return_to=return_to)
        else:
            return render_template('front/front_signup.html')

    def post(self):
        form = SignupForm(request.form)
        if form.validate():
            telephone = form.telephone.data
            username = form.username.data
            password = form.password1.data
            user = FrontUser(telephone=telephone, username=username, password=password)
            db.session.add(user)
            db.session.commit()
            return restful.success()
        else:
            print(form.get_error())
            return restful.params_error(message=form.get_error())


class SignInView(views.MethodView):
    def get(self):
        return_to = request.referrer
        # safeutils防止返回值被劫持
        if return_to and return_to != request.url and return_to!=url_for('front.singup')and safeutils.is_safe_url(return_to):

            return render_template('front/front_signin.html', return_to=return_to)
        else:
            return render_template('front/front_signin.html')
        # return render_template('front/front_signin.html')

    def post(self):
        form=SigninForm(request.form)
        if form.validate():
            telephone=form.telephone.data
            password=form.password.data
            remember=form.remember.data

            user=FrontUser.query.filter_by(telephone=telephone).first()
            if user and user.check_password(password):
                session[config.FRONT_USER_ID]=user.id
                if remember:
                    session.permanent=True
                return restful.success()
            else:
                return restful.params_error(message='手机号或密码错误')
        else:
            return restful.params_error(message=form.get_error())


bp.add_url_rule('/signup/', view_func=SignupView.as_view('signup'))
bp.add_url_rule('/signin/', view_func=SignInView.as_view('signin'))
