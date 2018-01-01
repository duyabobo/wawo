# -*- coding: utf-8 -*-
# __author__ = ‘du‘
# __created_at__ = '2018/1/1'

from niceapp.models import MessageCode, Users


def authenticate(mobile, code, sex):
    """
    验证手机号和验证码，如果验证通过就创建或更新一个新用户
    :param mobile:
    :param code:
    :param sex:
    :return:
    """
    MessageCode.insert_message_code(mobile, code, sex)  # 这个其实应该在发短信的时候做的
    user_id = MessageCode.check_code(mobile, code)
    return Users.get_one(user_id) if user_id else None


def get_invite_boy_condition(user_id):
    """
    查询一个邀请男生的信息
    :param user_id:
    :return:
    """
    user = Users.get_one(user_id)
    return {
        'school': user.school,
        'stature': user.stature,
        'weight': user.weight,
        'appearance': user.appearance,
        'character': user.character,
        'hobby': user.hobby,
        'speciality': user.speciality,
        'habit': user.habit,
        'wealth': user.wealth
    }  # todo


def get_suitable_girl_expection(user_id):
    """
    获取合适的女生信息
    :param user_id:
    :return:
    """
    user = Users.get_one(user_id)
    return {
        'school': user.school,
        'stature': user.stature,
        'weight': user.weight,
        'appearance': user.appearance,
        'character': user.character,
        'hobby': user.hobby,
        'speciality': user.speciality,
        'habit': user.habit,
        'wealth': user.wealth
    }  # todo
