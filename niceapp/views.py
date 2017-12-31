# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import login, logout
from django.shortcuts import render_to_response, redirect

from utils.auth import authenticate
from form.login import UserForm


def access_login(request):
    """
    登陆view
    :param request:
    :return:
    """
    if request.method == "POST":
        user_form = UserForm(request.POST)
        mobile = user_form.cleaned_data['mobile']
        code = user_form.cleaned_data['code']
        user = authenticate(mobile=mobile, code=code)
        if user:
            login(request, user)  # 验证成功之后登录
            return redirect('/index')
    else:
        user_form = UserForm()
        return render_to_response('login.html', {'user_form': user_form})


def access_logout(request):
    """
    登出view
    :param request:
    :return:
    """
    logout(request)
    return redirect("/login")
