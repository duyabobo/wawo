# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django.contrib.auth import authenticate, login, logout
from form.login import AuthForm
from form.user_info import UserForm
from models import Users


def access_login(request):
    """
    登陆view
    :param request:
    :return:
    """
    if request.method == "POST":
        auth_form = AuthForm(request.POST)
        if auth_form.is_valid():
            mobile = auth_form.cleaned_data['mobile']
            code = auth_form.cleaned_data['code']
            user = authenticate(mobile=mobile, code=code)
            if not user:  # 测试用户
                user = Users.get_test_user()
            login(request, user)  # 验证成功之后登录
            return redirect('/index')
    else:
        auth_form = AuthForm()
        return render(request, 'login.html', {'auth_form': auth_form})


def access_logout(request):
    """
    登出view
    :param request:
    :return:
    """
    logout(request)
    return redirect("/login")


@login_required
def index(request):
    """
    主页，就是一个表单，一个基本信息表单
    :param request:
    :return:
    """
    user_form = UserForm()
    return render(request, 'index.html', {'user_form': user_form})
