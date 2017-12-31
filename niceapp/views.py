# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import login, logout
from django.shortcuts import render, redirect

from utils.auth import authenticate
from form.login import UserForm
from models import Users


def access_login(request):
    """
    登陆view
    :param request:
    :return:
    """
    if request.method == "POST":
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            mobile = user_form.cleaned_data['mobile']
            code = user_form.cleaned_data['code']
            user = authenticate(mobile=mobile, code=code)
            if not user:  # 测试用户
                user = Users.get_test_user()
            login(request, user)  # 验证成功之后登录
            return redirect('/index')
    else:
        user_form = UserForm()
        return render(request, 'login.html', {'user_form': user_form})


def access_logout(request):
    """
    登出view
    :param request:
    :return:
    """
    logout(request)
    return redirect("/login")
