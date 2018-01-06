# -*- coding: utf-8 -*-
# __author__ = ‘du‘
# __created_at__ = '2018/1/6'
import logging
import time
from django.shortcuts import redirect, render


log = logging.getLogger("django")  # 为loggers中定义的名称


def logger(info_status=None):
    def inner_func(view_method):
        def innver_innver_func(*args, **kwargs):
            request = args[0]
            try:
                start_time = time.time()
                user = request.user
                if info_status is not None and user.info_status != info_status:
                    result = redirect("/")
                else:
                    result = view_method(*args, **kwargs)
                end_time = time.time()
                log.info(
                    'Method: {0}, Url: {1}, Body: {2}, COOKIES: {3}, Delay: {4}'.format
                    (request.method, request.path, request.body, request.COOKIES, end_time - start_time)
                )
            except Exception as e:
                log.exception(str(e))
                result = render(request, '500.html')
            return result
        return innver_innver_func
    return inner_func
