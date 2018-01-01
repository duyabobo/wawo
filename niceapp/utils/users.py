# -*- coding: utf-8 -*-
# __author__ = ‘du‘
# __created_at__ = '2018/1/1'

from niceapp.models import Users


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
