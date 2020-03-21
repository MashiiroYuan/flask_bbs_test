from apps.forms import BaseForm
from wtforms import StringField
from wtforms.validators import regexp, InputRequired
import hashlib


class SmsCaptchaForm(BaseForm):
    salt = 'q3423805gdflvbdfvhsdoa`#$%'
    telephone = StringField(validators=[regexp(r'1[345789]\d{9}')])
    timestamp = StringField(validators=[regexp(r'\d{13}')])
    sign = StringField(validators=[InputRequired()])

    def validate(self):
        result = super(SmsCaptchaForm, self).validate()
        if not result:
            return False
        telephone = self.telephone.data
        timestamp = self.timestamp.data
        sign = self.sign.data

        # md5(timestamp+telephone+salt)
        # md5  chuanige byte 字符串

        sign2 = hashlib.md5((timestamp + telephone + self.salt).encode('utf-8')).hexdigest()
        if sign == sign2:
            return True
        else:
            return False
