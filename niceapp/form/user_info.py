# -*- coding: utf-8 -*-
# __author__ = ‘du‘
# __created_at__ = '2017/12/31'
from django import forms

APPEARANCE_CHOICE = (
    (0, '不要求'),
    (1, '干净整洁'),
    (2, '阳光自信'),
    (3, '英俊帅气')
)


CHARACTER_CHOICE = (
    (0, '不明显'),
    (1, '自信'),
    (2, '好强'),
    (3, '暴躁'),
    (4, '温柔'),
    (5, '细心'),
    (6, '耐心')
)


HOBBY_CHOICE = (
    (0, '无'),
    (1, '动漫'),
    (2, '体育'),
    (3, '唱歌'),
    (4, '跳舞'),
    (5, '看书'),
    (6, '写作'),
    (7, '旅游'),
    (8, '摄影')
)


SPECIALITY_CHOICE = (
    (0, '无'),
    (1, '体育'),
    (2, '音乐'),
    (3, '写作'),
    (4, '历史'),
    (5, '政治'),
    (6, '演讲'),
    (7, '幽默'),
    (8, '着装'),
    (9, '学习')
)


HABIT_CHOICE = (
    (0, '无'),
    (1, '健身'),
    (2, '饮食'),
    (3, '自省'),
    (4, '阅读'),
    (5, '交友')
)


DISGUST_CHOICE = (
    (0, '无'),
    (1, '不守时'),
    (2, '说到做不到'),
    (3, '花心'),
    (4, '玩世不恭'),
    (5, '小心眼'),
    (6, '小气'),
    (7, '娘娘腔'),
    (8, '脏话连篇')
)


class UserForm(forms.Form):
    """用户基本信息表单"""
    city = forms.CharField(label='城市名', max_length=100)
    school = forms.CharField(label='学校名', max_length=100)
    stature = forms.IntegerField(label='身高(cm)')
    weight = forms.IntegerField(label='体重(kg)')
    appearance = forms.ChoiceField(label='相貌', choices=APPEARANCE_CHOICE)
    character = forms.ChoiceField(label='性格', choices=CHARACTER_CHOICE)
    hobby = forms.ChoiceField(label='兴趣', choices=HOBBY_CHOICE)
    speciality = forms.ChoiceField(label='特长', choices=SPECIALITY_CHOICE)
    habit = forms.ChoiceField(label='习惯', choices=HABIT_CHOICE)
    disgust = forms.ChoiceField(label='反感', choices=DISGUST_CHOICE)
    wealth = forms.IntegerField(label='每月生活费(元)')
    custom = forms.CharField(label='自定义', max_length=255)
    threshold_fee = forms.IntegerField(label='门槛费')


class RealForm(forms.Form):
    """实名制信息表单"""
    city = forms.CharField(label='城市名', max_length=100)
    school = forms.CharField(label='学校名', max_length=100)
