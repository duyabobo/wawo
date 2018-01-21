# -*- coding: utf-8 -*-
# __author__ = ‘du‘
# __created_at__ = '2018/1/6'
import logging
import time
from django.shortcuts import redirect, render


log = logging.getLogger("django")  # 为loggers中定义的名称


def logger(info_status, sex):
    """
    对每个接口请求进行日志记录
    :param info_status: 限制请求用户对用户状态
    :param sex: 限制请求用户的性别
    :return:
    """
    def inner_func(view_method):
        def innver_innver_func(*args, **kwargs):
            request = args[0]
            try:
                start_time = time.time()
                user = request.user
                if info_status or sex:
                    if info_status is not None and user.info_status != info_status:
                        result = redirect("/")
                    elif sex is not None and user.sex != sex:
                        result = redirect("/")
                    else:
                        result = view_method(*args, **kwargs)
                else:
                    result = view_method(*args, **kwargs)
                end_time = time.time()
                log.info(
                    'Method: {0}, Url: {1}, GET: {2}, POST: {3}, COOKIES: {4}, Delay: {5}'.format
                    (request.method, request.path, request.GET, request.POST, request.COOKIES, end_time - start_time)
                )
            except Exception as e:
                log.exception(str(e))
                result = render(request, '500.html')
            return result
        return innver_innver_func
    return inner_func
