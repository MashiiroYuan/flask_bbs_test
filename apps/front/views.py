from flask import Blueprint, views, render_template, request, make_response,session,url_for
from io import BytesIO
from utils.captcha import Captcha
from .forms import SignupForm,SigninForm,AddPostForm
from utils import restful, safeutils
from exts import db
from .models import FrontUser
from .decorators import login_required
from ..models import BannerModel,BoardModel,PostModel
import config
bp = Blueprint("front", __name__, )  # 域名


@bp.route('/')
def index():
    banners = BannerModel.query.order_by(BannerModel.priority.desc()).limit(4)
    boards = BoardModel.query.all()
    context = {
        'banners': banners,
        'boards':boards
    }

    return render_template('front/front_index.html',**context)

@bp.route('/apost/',methods=["GET","POST"])
@login_required
def apost():
    if request.method=="GET":
        boards=BoardModel.query.all()

        return render_template('front/front_apost.html',boards=boards)
    else:
        form=AddPostForm(request.form)
        if form.validate():
            title=form.title.data
            content=form.board_id.data
            board_id=form.board_id.data
            board=BoardModel.query.get(board_id)
            if not board:
                return restful.params_error(message='没有这个板块')
            post=PostModel(title=title,content=content)
            post.board=board
            db.session.add(post)
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(message=form.get_error())

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
        if return_to and return_to != request.url and return_to!=url_for('front.signup')and safeutils.is_safe_url(return_to):

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
