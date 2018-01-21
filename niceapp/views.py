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
from utils.log import logger


@logger(None)
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


@logger(None)
def access_logout(request):
    """
    登出view
    :param request:
    :return:
    """
    logout(request)
    return redirect("/login")


@logger(REGISTERED)
@login_required
def content_page(request):
    """
    补充信息
    :param request:
    :return:
    """
    user_form = UserForm()
    return render(request, 'submit_content.html', {'user_form': user_form})


@logger(REGISTERED)
@login_required
def submit_content(request):
    """
    存储用户上传的信息（期望条件/自身条件）
    :param request:
    :return:
    """
    user = request.user
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


@logger(SUBMIT)
@login_required
def girl_after_submit(request):
    """
    女生填完期望信息的等待邀请状态
    :param request:
    :return:
    """
    return render(request, 'girl_after_submit.html')


@logger(SUBMIT)
@login_required
def suitable_girl_page(request):
    """
    查看合适的女孩
    :param request:
    :return:
    """
    user = request.user
    suitable_girl_expection = get_suitable_girl_expection(user.id)
    UserRelation.insert_or_update_user_relation(user.id, suitable_girl_expection['id'], BOY_READ)
    return render(
        request, 'expection_content.html', {'suitable_girl_expection': suitable_girl_expection}
    )


@logger(SUBMIT)
@login_required
def choice_suitable_girl(request):
    """
    选择合适的女生
    :param request:
    :return:
    """
    user = request.user
    if request.method == 'POST':
        Users.update_one_record_one_field(user.id, info_status=INVITE)
        user_relation = UserRelation.get_one_user_relation_with_boy_id(user.id)
        if user_relation:
            girl_id = user_relation.girl_id
            Users.update_one_record_one_field(girl_id, info_status=INVITE)
            UserRelation.insert_or_update_user_relation(user.id, girl_id, BOY_INVITE)
        # 如果不存在 user_relation 怎么做
        return render(request, 'invite_success.html')
    else:
        return render(request, '404.html')


@logger(INVITE)
@login_required
def boy_after_invite(request):
    """
    男生等待邀请被接收的状态
    :param request:
    :return:
    """
    return render(request, 'boy_after_invite.html')


@logger(INVITE)
@login_required
def invite_boy_page(request):
    """
    查看邀请自己的男生
    :param request:
    :return:
    """
    user = request.user
    invite_boy_condition = get_invite_boy_condition(user.id)
    UserRelation.insert_or_update_user_relation(invite_boy_condition['id'], user.id, GRIL_READ)
    return render(
        request, 'inviter_content.html', {'invite_boy_condition': invite_boy_condition}
    )


@logger(INVITE)
@login_required
def accept_invite_boy(request):
    """
    接受男生邀请, 不需要拒绝接口，默认一天之后自动拒绝，可以限制女生拒绝的盲目性
    :param request:
    :return:
    """
    user = request.user
    if request.method == 'POST':
        Users.update_one_record_one_field(user.id, info_status=CONNECTED)
        user_relation = UserRelation.get_one_user_relation_with_girl_id(user.id)
        if user_relation:
            boy_id = user_relation.boy_id
            Users.update_one_record_one_field(boy_id, info_status=CONNECTED)
            UserRelation.insert_or_update_user_relation(boy_id, user.id, GRIL_ACCEPT)
        # todo 發送女生qq给男生, 如果不存在 user_relation 怎么做
        return redirect("/connect_page")
    else:
        return render(request, '404.html')


@logger(CONNECTED)
@login_required
def connect_page(request):
    """
    邀请或被邀请，然后接受邀请进入联系阶段
    :param request:
    :return:
    """
    return render(request, 'connect_success.html')


@logger(CONNECTED)
@login_required
def connect_to_fall_in_love(request):
    """
    进入恋爱状态
    :param request:
    :return:
    """
    user = request.user
    if request.method == 'POST':
        Users.update_one_record_one_field(user.id, info_status=FALLINLOVE)
        if user.sex == MALE:
            user_relation = UserRelation.get_one_user_relation_with_boy_id(user.id)
            if user_relation:
                girl_id = user_relation.girl_id
                UserRelation.insert_or_update_user_relation(user.id, girl_id, LAVE_STATUS)
                Users.update_one_record_one_field(girl_id, info_status=FALLINLOVE)
        else:
            user_relation = UserRelation.get_one_user_relation_with_girl_id(user.id)
            if user_relation:
                boy_id = user_relation.boy_id
                UserRelation.insert_or_update_user_relation(boy_id, user.id, LAVE_STATUS)
                Users.update_one_record_one_field(boy_id, info_status=FALLINLOVE)
        return render(request, 'fall_in_love.html')
    else:
        return render(request, '404.html')


@logger(CONNECTED)
@login_required
def connect_to_not_fit(request):
    """
    接触后不合适
    :param request:
    :return:
    """
    user = request.user
    if request.method == 'POST':
        Users.update_one_record_one_field(user.id, info_status=SUBMIT)
        if user.sex == MALE:
            user_relation = UserRelation.get_one_user_relation_with_boy_id(user.id)
            if user_relation:
                girl_id = user_relation.girl_id
                UserRelation.insert_or_update_user_relation(user.id, girl_id, NOT_FIT)
                Users.update_one_record_one_field(girl_id, info_status=SUBMIT)
        else:
            user_relation = UserRelation.get_one_user_relation_with_girl_id(user.id)
            if user_relation:
                boy_id = user_relation.boy_id
                UserRelation.insert_or_update_user_relation(boy_id, user.id, NOT_FIT)
                Users.update_one_record_one_field(boy_id, info_status=SUBMIT)
        return redirect("/")
    else:
        return render(request, '404.html')


@logger(CONNECTED)
@login_required
def connect_to_complain(request):
    """
    接触后投诉
    :param request:
    :return:
    """
    user = request.user
    if request.method == 'POST':
        Users.update_one_record_one_field(user.id, info_status=COMPLAIN)
        if user.sex == MALE:
            user_relation = UserRelation.get_one_user_relation_with_boy_id(user.id)
            if user_relation:
                girl_id = user_relation.girl_id
                UserRelation.insert_or_update_user_relation(user.id, girl_id, IN_COMPLAN)
                Users.update_one_record_one_field(girl_id, info_status=COMPLAINED)
        else:
            user_relation = UserRelation.get_one_user_relation_with_girl_id(user.id)
            if user_relation:
                boy_id = user_relation.boy_id
                UserRelation.insert_or_update_user_relation(boy_id, user.id, IN_COMPLAN)
                Users.update_one_record_one_field(boy_id, info_status=COMPLAINED)
        return redirect("/")
    else:
        return render(request, '404.html')


@logger(FALLINLOVE)
@login_required
def love_page(request):
    """
    恋爱页面
    :param request:
    :return:
    """
    return render(request, 'fall_in_love.html')


@logger(FALLINLOVE)
@login_required
def break_up_after_love(request):
    """
    恋爱后分手，分手后没有抱怨入口，因为可以防止进入恋爱状态的盲目性，分手如果想要退还门槛费，男生需要实名制
    :param request:
    :return:
    """
    user = request.user
    if request.method == 'POST':
        Users.update_one_record_one_field(user.id, info_status=SUBMIT)
        if user.sex == MALE:
            user_relation = UserRelation.get_one_user_relation_with_boy_id(user.id)
            if user_relation:
                girl_id = user_relation.girl_id
                UserRelation.insert_or_update_user_relation(user.id, girl_id, BREAK_UP)
                Users.update_one_record_one_field(girl_id, info_status=SUBMIT)
        else:
            user_relation = UserRelation.get_one_user_relation_with_girl_id(user.id)
            if user_relation:
                boy_id = user_relation.boy_id
                UserRelation.insert_or_update_user_relation(boy_id, user.id, BREAK_UP)
                Users.update_one_record_one_field(boy_id, info_status=SUBMIT)
        return redirect("/")
    else:
        return render(request, '404.html')


@logger(BREAK_UP)
@login_required
def request_pay_back(request):
    """
    申请退还门槛费页面，如果选了，就设置男生的状态为 REQUEST_PAY_BACK
    :param request:
    :return:
    """
    user = request.user
    Users.update_one_record_one_field(user.id, info_status=REQUEST_PAY_BACK)
    return redirect("/")


@login_required
def index(request):
    """
    主页，根据 info_status 构建主逻辑
    :param request:
    :return:  
    """
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
        return render(request, 'real_name.html')
