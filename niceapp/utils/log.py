# -*- coding: utf-8 -*-
# __author__ = ‘du‘
# __created_at__ = '2018/1/6'
import logging
import time
from django.shortcuts import redirect, render


log = logging.getLogger("django")  # 为loggers中定义的名称


def get_request_ip(request):
    """
    获取请求方的ip
    :param request:
    :return:
    """
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        ip = request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']
    return ip


def logger(info_status, sex):
    """
    对每个接口请求进行日志记录
    :param info_status: 限制请求用户对用户状态
    :param sex: 限制请求用户的性别
    :return:
    """
    def inner_func(view_method):
        def innver_innver_func(request, *args, **kwargs):
            try:
                start_time = time.time()
                user = request.user
                request_ip = get_request_ip(request)
                if info_status or sex:
                    if info_status is not None and user.info_status != info_status:
                        result = redirect("/")
                    elif sex is not None and user.sex != sex:
                        result = redirect("/")
                    else:
                        result = view_method(request, *args, **kwargs)
                else:
                    result = view_method(request, *args, **kwargs)
                end_time = time.time()
                log.info(
                    '''
                    RequestIp: {0}, 
                    Method: {1}, 
                    Url: {2}, 
                    GET: {3}, 
                    POST: {4}, 
                    COOKIES: {5}, 
                    Result: {6}, 
                    Delay: {7}
                    '''.format
                    (
                        request_ip,
                        request.method,
                        request.path,
                        request.GET,
                        request.POST,
                        request.COOKIES,
                        result,
                        end_time - start_time
                    )
                )
            except Exception as e:
                log.exception(str(e))
                result = render(request, '500.html')
            return result
        return innver_innver_func
    return inner_func
