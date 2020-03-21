from .views import bp
from flask import session, g
import config
from .models import CmsUser, CmsPermission


@bp.before_request
def before_request():
    if config.CMS_USER_ID in session:
        user_id = session.get(config.CMS_USER_ID)
        user = CmsUser.query.get(user_id)
        if user:
            g.cms_user = user


@bp.context_processor
def cms_context_processor():
    return {"CmsPermission": CmsPermission}
