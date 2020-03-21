## 关于bbs项目的问题
1. 修改邮箱时 使用的views函数中 验证码和邮箱重复的验证出现的运行顺序问题

2. validate_函数到底时一个怎样的 函数运行 class 类中的函数实例化后即会执行

###优化 怎样才能让修改邮箱时 点击发送邮件时 先判断是否邮箱账号与新邮箱是否一致,若不一致点击后 *出现灰色倒计时*

3.权限的确认,每个功能赋予一个8位二进制代码 需要此权限时用`|`(或) 连接 进行加法操作 表之间要有多对多的连接,

4.发送短信功能 `阿里大于`接口,api 接口文件 申请密钥  编辑发送文本 发送验证码

salt 15xxxx时间戳

5. 加密加盐  使用md5 加密传输字节 规定相同的salt 对比 混淆和加密 将js 码压缩后进行混淆 不容易获取源码

6.`validate` validate+`_`参数名 wtforms 会自动调用方法验证
```python
# BaseForm 继承Form
from wtforms import Form
class BaseForm(Form):
    def validate(self):
        return super(BaseForm,self).validate()
# Form 中validate
def validate(self):
    """
    Validates the form by calling `validate` on each field, passing any
    extra `Form.validate_<fieldname>` validators to the field validator.
    """
```

7. HTTP Referer是header的一部分，
当浏览器向web服务器发送请求的时候，一般会带上Referer，
告诉服务器我是从哪个页面链接过来的，服务器籍此可以获得一些信息用于处理。`request.referrer`引用上一个页面的地址
在页面中可以直接使用你传入入的参数进行获取如`{{return_to}}`