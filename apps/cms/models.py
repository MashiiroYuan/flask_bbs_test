from exts import db
from datetime import datetime
# 导入加密,解密函数
from werkzeug.security import generate_password_hash, check_password_hash


class CmsPermission(object):
    # 255 二进制表示权限
    ALL_PERMISSION = 0b11111111
    # Vistor 访问
    VISTITOR = 0b00000001
    # 帖子管理
    POSTER =   0b00000010
    # 评论管理
    COMMENTER =0b00000100
    # 板块管理
    BORARDER = 0b00001000
    # 前台用户管理
    FRONTER =  0b00010000
    # 后台用户管理
    CMSUSER =  0b00100000
    # 管理后台管理权限
    ADMINER =  0b01000000


cms_role_user = db.Table(
    'cms_role_user',
    db.Column('cms_role_id', db.Integer, db.ForeignKey('cms_role.id'), primary_key=True),
    db.Column('cms_user_id', db.Integer, db.ForeignKey("cms_user.id"), primary_key=True),
)


class CMSRole(db.Model):
    __tablename__ = 'cms_role'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=True)
    desc = db.Column(db.String(250), nullable=True)
    create_time = db.Column(db.DateTime, default=datetime.now)
    permission = db.Column(db.Integer, default=CmsPermission.VISTITOR)
    users = db.relationship("CmsUser", secondary=cms_role_user, backref='roles')


class CmsUser(db.Model):
    __tablename__ = 'cms_user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    _password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    join_time = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    @property
    def password(self):
        return self._password

    # 加密密码
    @password.setter
    def password(self, raw_password):
        self._password = generate_password_hash(raw_password)

    # 检查密码
    def check_password(self, raw_password):
        result = check_password_hash(self.password, raw_password)
        return result

    # 获取权限
    # 这里role 中的权限为permission 注意区分
    @property
    def permissions(self):
        if not self.roles:
            return 0
        all_permissions = 0
        for role in self.roles:
            permissions = role.permission
            print('12permission',permissions)
            all_permissions |= permissions
            print('allper',all_permissions)
        return all_permissions

    # 判断权限
    def has_permission(self, permission):
        all_permissions = self.permissions
        print('self',all_permissions,'persi',permission)
        result = all_permissions & permission == permission
        print('re',result)
        return result
        # return self.permission & permission == permission

    # 判断是否为开发者
    @property
    def is_developer(self):
        return self.has_permission(CmsPermission.ALL_PERMISSION)

# user=CmsUser()
