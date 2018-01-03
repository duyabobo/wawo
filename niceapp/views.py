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
def content_page(request):
    """
    补充信息
    :param request:
    :return:
    """
    user_form = UserForm()
    return render(request, 'submit_content.html', {'user_form': user_form})


@login_required
def submit_content(request):
    """
    存储用户上传的信息（期望条件/自身条件）
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
            if user.sex == MALE:
                return redirect("/suitable_girl_page")
            else:
                return redirect("/invite_boy_page")
        else:
            return HttpResponse(json.dumps(user_form.errors))
    else:
        return render(request, '404.html')


@login_required
def girl_after_submit(request):
    """
    女生填完期望信息的等待邀请状态
    :param request:
    :return:
    """
    return render(request, 'girl_after_submit.html')


@login_required
def suitable_girl_page(request):
    """
    查看合适的女孩
    :param request:
    :return:
    """
    user = request.user
    if user.info_status != SUBMIT:
        return redirect("/")
    suitable_girl_expection = get_suitable_girl_expection(user.id)  # todo 如果没有合适的女生？？
    return render(
        request, 'expection_content.html', {'suitable_girl_expection': suitable_girl_expection}
    )


@login_required
def choice_suitable_girl(request):
    """
    选择合适的女生
    :param request:
    :return:
    """
    user = request.user
    if user.info_status != SUBMIT:
        return redirect("/")
    if request.method == 'POST':
        Users.update_one_record_one_field(user.id, info_status=INVITE)  # todo 还需要同步修改女生的状态为 INVITE
        return render(request, 'invite_success.html')
    else:
        return render(request, '404.html')


@login_required
def boy_after_invite(request):
    """
    男生等待邀请被接收的状态
    :param request:
    :return:
    """
    return render(request, 'boy_after_invite.html')


@login_required
def invite_boy_page(request):
    """
    查看邀请自己的男生
    :param request:
    :return:
    """
    user = request.user
    if user.info_status != INVITE:
        return redirect("/")
    invite_boy_condition = get_invite_boy_condition(user.id)  # todo 如果没有邀请的男生
    return render(
        request, 'inviter_content.html', {'invite_boy_condition': invite_boy_condition}
    )


@login_required
def accept_invite_boy(request):  # todo 还需要一个 拒绝邀请的 接口
    """
    接受男生邀请
    :param request:
    :return:
    """
    user = request.user
    if user.info_status != INVITE:
        return redirect("/")
    if request.method == 'POST':
        Users.update_one_record_one_field(user.id, info_status=CONNECTED)  # todo 还需要同步修改男生的状态为 CONNECTED
        return redirect("/connect_page")
    else:
        return render(request, '404.html')


@login_required
def connect_page(request):
    """
    邀请或被邀请，然后接受邀请进入联系阶段
    :param request:
    :return:
    """
    user = request.user
    if user.info_status != CONNECTED:
        return redirect("/")
    return render(request, 'connect_success.html')


@login_required
def connect_to_fall_in_love(request):  # todo 还需要进入不合适接口/进入投诉状态的接口
    """
    进入恋爱状态
    :param request:
    :return:
    """
    user = request.user
    if user.info_status != CONNECTED:
        return redirect("/")
    if request.method == 'POST':
        Users.update_one_record_one_field(user.id, info_status=FALLINLOVE)  # todo 男生女生需要同步变化状态
        return render(request, 'fall_in_love.html')
    else:
        return render(request, '404.html')


@login_required
def love_page(request):
    """
    恋爱页面
    :param request:
    :return:
    """
    user = request.user
    if user.info_status != FALLINLOVE:
        return redirect("/")
    return render(request, 'fall_in_love.html')


@login_required
def break_up_after_love(request):
    """
    恋爱后分手
    :param request:
    :return:
    """
    user = request.user
    if user.info_status != FALLINLOVE:
        return redirect("/")
    if request.method == 'POST':
        Users.update_one_record_one_field(user.id, info_status=SUBMIT)  # todo 男生女生需要同步变化状态
        return redirect("/")
    else:
        return render(request, '404.html')


@login_required
def index(request):
    """
    主页，根据 info_status 构建主逻辑
    :param request:
    :return:  
    """  # todo 拆分后，每个 api 应该只支持一个 method
    user = request.user
    info_status = int(user.info_status)
    sex = user.sex
    if info_status == REGISTERED:
        return redirect("/content_page")
    elif info_status == SUBMIT:
        if sex == MALE:
            return redirect("/suitable_girl_page")
        else:
            return redirect("/girl_after_submit")
    elif info_status == INVITE:
        if sex == MALE:
            return redirect("/boy_after_invite")
        else:
            return redirect("/invite_boy_page")
    elif info_status == CONNECTED:
        return redirect("/connect_page")
    elif info_status == FALLINLOVE:
        return redirect("/love_page")
    else:
        return render(request, 'realname.html')
