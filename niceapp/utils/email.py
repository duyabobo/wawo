# -*- coding: utf-8 -*-
# __author__ = ‘du‘
# __created_at__ = '2018/1/21'
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse


# # settings 中需要增加如下配置
# # 这一项是固定的
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# # smtp服务的邮箱服务器 我用的是163
# EMAIL_HOST = 'smtp.163.com'
# # smtp服务固定的端口是25
# EMAIL_PORT = 25
# # 发送邮件的邮箱
# EMAIL_HOST_USER = 'xxxx@163.com'
# # 在邮箱中设置的客户端授权密码
# EMAIL_HOST_PASSWORD = 'xxxx'
# # 收件人看到的发件人 <此处要和发送邮件的邮箱相同>
# EMAIL_FROM = 'serverWarning<xxxx@163.com>'
def send(msg):
    send_mail(
        'error',
        'error',
        settings.EMAIL_FROM,
        ('809618694@qq.com', ),
        html_message=msg
    )
