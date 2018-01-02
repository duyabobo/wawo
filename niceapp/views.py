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
            user = authenticate(mobile=mobile, code=code)
            login(request, user)
            return redirect('/')
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
def submit(request):
    """
    补充信息，获取推荐异性
    :param request:
    :return:
    """
    user = request.user
    if user.info_status != REGISTERED:
        return redirect("/")
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            Users.update_one_record(user.id, **user_form.cleaned_data)
            Users.update_one_record_one_field(user.id, info_status=SUBMIT)
            return redirect("/connect")
        else:
            return HttpResponse(json.dumps(user_form.errors))
    else:
        user_form = UserForm()
        return render(request, 'submit_content.html', {'user_form': user_form})


@login_required
def connect(request):
    """
    邀请或被邀请，然后接受邀请进入联系阶段
    :param request:
    :return:
    """
    user = request.user
    if user.info_status == SENTINVITE:
        return render(request, 'invite_success.html')
    if user.info_status != SUBMIT:
        return redirect("/")
    if request.method == 'POST':
        if user.sex == MALE:
            Users.update_one_record_one_field(user.id, info_status=SENTINVITE)  # todo 还需要修改女生的状态
            return render(request, 'invite_success.html')
        else:
            Users.update_one_record_one_field(user.id, info_status=CONNECTED)  # todo 还需要修改男生的状态
            return render(request, 'access_success.html')
    else:
        if user.sex == MALE:
            suitable_girl_expection = get_suitable_girl_expection(user.id)
            return render(
                request, 'expection_content.html', {'suitable_girl_expection': suitable_girl_expection}
            )
        else:
            invite_boy_condition = get_invite_boy_condition(user.id)
            return render(
                request, 'inviter_content.html', {'invite_boy_condition': invite_boy_condition}
            )


@login_required
def fall_in_love(request):
    """
    进入热恋状态，或者进入投诉流程
    :param request:
    :return:
    """
    user = request.user
    if user.info_status != CONNECTED:
        return redirect("/")
    if request.method == 'POST':
        return render(request, 'fall_in_love.html')  # todo 区分是投诉还是坠入爱河
    else:
        if user.sex == MALE:
            return render(request, 'invite_success.html')
        else:
            return render(request, 'access_success.html')


@login_required
def be_in_love(request):
    """
    热恋后状态
    :param request:
    :return:
    """
    user = request.user
    if user.info_status != FALLINLOVE:
        return redirect("/")
    if request.method == 'POST':
        return render(request, 'fall_in_love.html')  # todo 区分是投诉还是深入爱河
    else:
        return render(request, 'fall_in_love.html')


@login_required
def index(request):
    """
    主页，根据 info_status 构建主逻辑
    :param request:
    :return:  
    """  # todo 拆分后，每个 api 应该只支持一个 method
    user = request.user
    info_status = int(user.info_status)
    if info_status == REGISTERED:
        return redirect("/submit")
    elif info_status == SUBMIT:
        return redirect("/connect")
    elif info_status == SENTINVITE:
        return redirect("/connect")
    elif info_status == CONNECTED:
        return redirect("/fall_in_love")
    elif info_status == FALLINLOVE:
        return redirect("/be_in_love")
    else:
        return render(request, 'error.html')
