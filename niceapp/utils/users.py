# -*- coding: utf-8 -*-
# __author__ = ‘du‘
# __created_at__ = '2018/1/1'

from niceapp.models import MessageCode, Users


def authenticate(mobile, code):
    """
    验证手机号和验证码，如果验证通过就创建或更新一个新用户
    :param mobile:
    :param code:
    :return:
    """
    MessageCode.insert_message_code(mobile, code)  # 这个其实应该在发短信的时候做的
    user_id = MessageCode.check_code(mobile, code)
    return Users.get_one(user_id) if user_id else None


def get_invite_boy_condition(girl_id):
    """
    查询一个邀请男生的信息
    :param girl_id:
    :return:
    """
    user = Users.get_one_boy(girl_id)
    return {
        'id': user.id,
        'home_province': user.home_province,
        'home_city': user.home_city,
        'school_province': user.school_province,
        'school_city': user.school_city,
        'birth_year': user.birth_year,
        'sex': user.sex,
        'stature': user.stature,
        'weight': user.weight,
        'appearance': user.appearance,
        'character': user.character,
        'hobby': user.hobby,
        'speciality': user.speciality,
        'habit': user.habit,
        'wealth': user.wealth
    }


def get_suitable_girl_expection(boy_id):
    """
    获取合适的女生信息
    :param girl_id:
    :return:
    """
    user = Users.get_one_girl(boy_id)
    return {
        'id': user.id,
        'home_province': user.home_province,
        'home_city': user.home_city,
        'school_province': user.school_province,
        'school_city': user.school_city,
        'birth_year': user.birth_year,
        'sex': user.sex,
        'stature': user.stature,
        'weight': user.weight,
        'appearance': user.appearance,
        'character': user.character,
        'hobby': user.hobby,
        'speciality': user.speciality,
        'habit': user.habit,
        'wealth': user.wealth
    }
