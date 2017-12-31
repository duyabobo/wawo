# -*- coding: utf-8 -*-
# __author__ = ‘du‘
# __created_at__ = '2017/12/31'
from niceapp.models import MessageCode, Users


def authenticate(mobile, code):
    """
    用户登陆前认证
    :param mobile:
    :param code:
    :return:
    """
    user_id = MessageCode.get_user_id(mobile, code)
    return Users.get_one(user_id)
