from flask_script import Manager
from flask_migrate import MigrateCommand, Migrate
from app import app
from exts import db
from apps.cms import models as cms_models
from apps.front import models as front_models
from apps.models import BannerModel,BoardModel

FrontUser=front_models.FrontUser

CmsUser = cms_models.CmsUser

CmsRole = cms_models.CMSRole

CmsPermission = cms_models.CmsPermission

# app = app()

manager = Manager(app)
Migrate(app, db)
manager.add_command('db', MigrateCommand)


@manager.command
def create_role():
    # 访问者
    visitor = CmsRole(name='访问者', desc='只能访问无法修改')
    visitor.permission = CmsPermission.VISTITOR

    # 运营角色 修改个人信息 帖子 评论
    operator = CmsRole(name='运营', desc='管理帖子,ing论')
    operator.permission = CmsPermission.VISTITOR | CmsPermission.POSTER | CmsPermission.CMSUSER | CmsPermission.COMMENTER

    # 管理员
    admin = CmsRole(name='管理员', desc='系统权限')
    admin.permission = CmsPermission.VISTITOR | CmsPermission.POSTER | CmsPermission.CMSUSER | CmsPermission.COMMENTER | CmsPermission.FRONTER | CmsPermission.BORARDER

    # 开发者
    developer = CmsRole(name='开发者', desc='开发人员')
    developer.permission = CmsPermission.ALL_PERMISSION

    # db.session.add_all([visitor, operator, admin, developer])
    # db.session.commit()

@manager.option('-e','--email',dest='email')
@manager.option('-n','--name',dest='name')
def add_user_to_role(email,name):
    user=CmsUser.query.filter_by(email=email).first()
    if user:
        pass
        role=CmsRole.query.filter_by(name=name).first()
        if role:
            role.users.append(user)
            db.session.commit()
            print('success')
        else:
            print('无此角色%s'% role)
    else:
        print('%s没有用户'%email)

# 测试是否有某个权限
@manager.command
def test_permission():
    print('sc')
    user = CmsUser.query.first()
    print(user)
    if user.has_permission(CmsPermission.VISTITOR):
        print('访问权限')
    else:
        print('无访问者权限')


@manager.option('-u', '--username', dest='username')
@manager.option('-p', '--password', dest='password')
@manager.option('-e', '--email', dest='email')
def create_cms_user(username, password, email):
    user = CmsUser(username=username, password=password, email=email)
    db.session.add(user)
    db.session.commit()
    print('success')

@manager.option('-t','--telephone',dest='telephone')
@manager.option('-u','--username',dest='username')
@manager.option('-p','--password',dest='password')
def create_front_user(telephone,username,password):
    user=FrontUser(telephone=telephone,username=username,password=password)
    db.session.add(user)
    db.session.commit()



if __name__ == "__main__":
    manager.run()
