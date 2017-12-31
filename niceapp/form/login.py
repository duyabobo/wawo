# -*- coding: utf-8 -*-
# __author__ = ‘du‘
# __created_at__ = '2017/12/31'
from django import forms


class UserForm(forms.Form):
    mobile = forms.CharField(label='手机号', max_length=100)
    code = forms.CharField(label='短信码', max_length=100)
