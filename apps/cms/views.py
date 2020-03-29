import string
import random

from flask import Blueprint, views, render_template, request, session, redirect, url_for, g, jsonify
from .forms import LoginForm, ResetpwdForm, ResetEmailForm, AddBannerForm, UpdateBannnerForm, AddBoardForm, \
    UpdateBoardForm
from .models import CmsUser, CmsPermission
from .decorators import login_required, permission_required
import config
from exts import db, mail
from utils import restful, zlcache
from flask_mail import Message
from apps.models import BannerModel, BoardModel,PostModel,HighlightPostModel

# 注册时 url_prefix 要加/
bp = Blueprint("cms", __name__, url_prefix='/cms')  # 域名


@bp.route('/')
@login_required
def index():
    return render_template('cms/cms_index.html')


@bp.route('/logout/')
@login_required
def logout():
    del session[config.CMS_USER_ID]
    return redirect(url_for('cms.login'))


@bp.route('/email/')
def email():
    message = Message('邮件发送', recipients=['987639797@qq.com'], body='test')
    mail.send(message)
    return 'success'


@bp.route('/email_captcha/')
@login_required
def email_captcha():
    # memch
    user = g.cms_user
    print(user)
    email = request.args.get('email')

    if not email:
        return restful.params_error('请传递邮箱参数')
    source = list(string.ascii_letters)
    source.extend(map(lambda x: str(x), range(0, 10)))
    # source.extend(['0','1','2','3','4','5','6','7','8','9'])
    captcha = "".join(random.sample(source, 6))  # 获取验证码,返回的是列表
    # send email

    message = Message('Python BBs', recipients=[email], body='验证码为:%s' % captcha)
    try:
        mail.send(message)
    except:
        return restful.server_error()
    # 验证码 邮箱 存储到memcache
    zlcache.set(email, captcha)
    return restful.success()


@bp.route('/banners/')
@login_required
def banners():
    banners = BannerModel.query.all()
    return render_template('cms/cms_banners.html', banners=banners)


@bp.route('/abanner/', methods=['POST'])
def abanner():
    form = AddBannerForm(request.form)
    if form.validate():
        name = form.name.data
        image_url = form.image_url.data
        link_url = form.link_url.data
        priority = form.priority.data
        banner = BannerModel(name=name, image_url=image_url, link_url=link_url, priority=priority)
        db.session.add(banner)
        db.session.commit()
        return restful.success()
    else:
        return restful.params_error(message=form.get_error())


@bp.route('/ubanner/', methods=["POST"])
def ubanner():
    form = UpdateBannnerForm(request.form)
    if form.validate():
        banner_id = form.banner_id.data
        name = form.name.data
        image_url = form.image_url.data
        link_url = form.link_url.data
        priority = form.priority.data
        banner = BannerModel.query.get(banner_id)
        if banner:
            banner.name = name
            banner.image_url = image_url
            banner.link_url = link_url
            banner.priority = priority
            print(banner.image_url)
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(message='五轮播图')
    else:
        return restful.params_error(message=form.get_error())


@bp.route('/dbanner/', methods=['POST'])
@login_required
def dbanner():
    banner_id = request.form.get('banner_id')
    if not banner_id:
        return restful.params_error(message="请输入轮播图id")
    banner = BannerModel.query.get(banner_id)
    if not banner:
        return restful.params_error(message='没有这个id')

    db.session.delete(banner)
    db.session.commit()
    return restful.success()


@bp.route('/comments/')
@login_required
@permission_required(CmsPermission.COMMENTER)
def comments():
    return render_template('cms/cms_comments.html')


@bp.route('/posts/')
@login_required
@permission_required(CmsPermission.POSTER)
def posts():
    post_list = PostModel.query.all()
    return render_template('cms/cms_posts.html',posts=post_list)

@bp.route('/boards/')
@login_required
@permission_required(CmsPermission.BORARDER)
def boards():
    board_models = BoardModel.query.all()
    context = {
        'boards': board_models
    }
    return render_template('cms/cms_boards.html', **context)


@bp.route('/aboard/', methods=["POST"])
@login_required
@permission_required(CmsPermission.BORARDER)
def aboard():
    form = AddBoardForm(request.form)
    if form.validate():
        name = form.name.data
        board = BoardModel(name=name)
        db.session.add(board)
        db.session.commit()
        return restful.success()
    else:
        return restful.params_error(message=form.get_error())


# 修改板块
@bp.route('/uboard/', methods=["POST"])
@login_required
@permission_required(CmsPermission.BORARDER)
def uboard():
    form = UpdateBoardForm(request.form)
    if form.validate():
        name = form.name.data
        board_id = form.board_id.data
        board = BoardModel.query.get(board_id)
        if board:
            board.name = name
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(message='五次模块')
    else:
        return restful.params_error(form.get_error())


# 删除板块
@bp.route('/dboard/', methods=["POST"])
@login_required
@permission_required(CmsPermission.BORARDER)
def dboard():
    board_id = request.form.get()
    if not board_id:
        return restful.params_error(message='请传入id')
    board = BoardModel.query.get(board_id)
    if not board:
        return restful.params_error(message='没有这个模块')
    db.session.delete(board)
    db.session.commit()
    return restful.success()


#加精
@bp.route('/hpost/',methods=["POST"])
@login_required
@permission_required(CmsPermission.POSTER)
def hpost():
    post_id=request.form.get('post_id')
    if not post_id:
        return restful.params_error('出入id')
    post=PostModel.query.get(post_id)
    if not post:
        return restful.params_error('无此帖子')
    hightlight=HighlightPostModel()
    hightlight.post=post
    db.session.add(hightlight)
    db.session.commit()
    return restful.success()


#取消精品
@bp.route('/uhpost/',methods=["POST"])
@login_required
@permission_required(CmsPermission.POSTER)
def uhpost():
    post_id=request.form.get('post_id')
    if not post_id:
        return restful.params_error('出入id')
    post=PostModel.query.get(post_id)
    if not post:
        return restful.params_error('无此帖子')
    hightlight=HighlightPostModel.query.filter_by(post_id=post_id)

    db.session.delete(hightlight)
    db.session.commit()
    return restful.success()

@bp.route('/frusers/')
@login_required
@permission_required(CmsPermission.FRONTER)
def frusers():
    return render_template('cms/cms_fronuser.html')


@bp.route('/croles/')
@login_required
@permission_required(CmsPermission.ALL_PERMISSION)
def croles():
    return render_template('cms/cms_croles.html')


@bp.route('/cusers/')
@login_required
@permission_required(CmsPermission.CMSUSER)
def cusers():
    return render_template('cms/cms_cusers.html')


class LoginView(views.MethodView):
    def get(self, message=None):
        return render_template('cms/cms_login.html', message=message)

    def post(self):
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            remember = form.remember.data
            user = CmsUser.query.filter_by(email=email).first()
            if user and user.check_password(password):
                session[config.CMS_USER_ID] = user.id
                if remember:
                    # 设置持久化 (31天)
                    # config 中PERMANENT_SESSION_LIFETIME=Time
                    session.permanent = True
                    # 不管怎样 要加上返回的 那个函数的前缀
                return redirect(url_for('cms.index'))
            else:
                return self.get(message='邮箱或密码错误')
        else:
            print(form.errors)
            message = form.errors.popitem()[1][0]
            return self.get(message=message)


@bp.route('/profile/')
def profile():
    return render_template('cms/cms_profile.html')


class RestPwdView(views.MethodView):
    decorators = [login_required]

    def get(self):
        return render_template('cms/cms_resetpassword.html')

    def post(self):
        form = ResetpwdForm(request.form)
        if form.validate():
            oldpwd = form.oldpwd.data
            newpwd = form.newpwd.data
            user = g.cms_user
            if user.check_password(oldpwd):
                user.password = newpwd
                db.session.commit()
                return restful.success()

            else:
                return restful.params_error("旧密码错误！")
        else:
            # message = form.get_error()
            return restful.params_error(form.get_error())


class ResetEmailView(views.MethodView):
    decorators = [login_required]

    def get(self):
        return render_template('cms/cms_resetemail.html')

    def post(self):
        # 验证
        form = ResetEmailForm(request.form)
        email = form.email.data
        print('email', email)
        g.cms_user.email = email
        if form.validate():
            email = form.email.data
            print('email', email)
            g.cms_user.email = email
            db.session.commit()
            return restful.success()

        else:
            return restful.params_error(form.get_error())


bp.add_url_rule('/login/', view_func=LoginView.as_view('login'))
bp.add_url_rule('/resetpwd/', view_func=RestPwdView.as_view('resetpwd'))
bp.add_url_rule('/resetemail/', view_func=ResetEmailView.as_view('resetemail'))
