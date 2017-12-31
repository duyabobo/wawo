# -*- coding: utf-8 -*-
# __author__ = ‘du‘
# __created_at__ = '2017/12/31'
from django import forms

SEX_CHOICE = (
    (0, '女'),
    (1, '男')
)


class AuthForm(forms.Form):
    """登陆表单"""
    mobile = forms.CharField(label='手机号', max_length=100)
    code = forms.CharField(label='短信码', max_length=100)
    sex = forms.ChoiceField(label='我的性别', choices=SEX_CHOICE)
