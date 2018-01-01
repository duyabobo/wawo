# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required

from django.contrib.auth import login, logout
import json
from form.login import AuthForm
from form.user_info import UserForm
from models import *
from utils.users import get_invite_boy_condition, get_suitable_girl_expection, authenticate


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
            sex = auth_form.cleaned_data['sex']
            user = authenticate(mobile=mobile, code=code, sex=sex)
            if not user:  # 测试用户
                user = Users.get_test_user()
            login(request, user)  # 验证成功之后登录
            Users.update_one_record(user.id, sex=sex)
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
    主页
    :param request:
    :return:
    """
    user = request.user
    info_status = int(user.info_status)
    if info_status in (REGISTERED, EXPIRED):  # 填写用户信息或者期望信息
        if request.method == 'POST':
            user_form = UserForm(request.POST)
            if user_form.is_valid():
                Users.update_one_record(user.id, **user_form.cleaned_data)
                Users.update_one_record_one_field(user.id, info_status=SUBMIT)
                return redirect("/index")
            else:
                return HttpResponse(json.dumps(user_form.errors))
        else:
            user_form = UserForm()
            return render(request, 'submit_content.html', {'user_form': user_form, 'sex': user.sex})
    elif info_status in (SUBMIT, REALNAME):  # 已填写用户信息或期望信息
        if request.method == 'POST':
            Users.update_one_record_one_field(user.id, info_status=LOCKED)
            if user.sex == MALE:
                return render(request, 'invite_success.html')
            else:
                return render(request, 'access_success.html')
        else:
            if user.sex == MALE:
                suitable_girl_expection = get_suitable_girl_expection(user.id)
                suitable_girl_form = UserForm(suitable_girl_expection)
                return render(
                    request, 'expection_content.html',
                    {'suitable_girl_form': suitable_girl_form, 'suitable_girl_expection': suitable_girl_expection}
                )
            else:
                invite_boy_condition = get_invite_boy_condition(user.id)
                invite_boy_form = UserForm(invite_boy_condition)
                return render(
                    request, 'inviter_content.html',
                    {'invite_boy_form': invite_boy_form, 'invite_boy_condition': invite_boy_condition}
                )
    elif info_status == LOCKED:
        if user.sex == MALE:
            return render(request, 'invite_success.html')
        else:
            return render(request, 'access_success.html')
    else:
        return render(request, 'error.html')
