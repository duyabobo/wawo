# -*- coding: utf-8 -*-
# __author__ = ‘du‘
# __created_at__ = '2017/12/31'
from django.conf.urls import url

from views import *

urlpatterns = [
    url(r'^login$', access_login, name='login'),
    url(r'^logout$', access_logout, name='logout'),
    url(r'^index$', index, name='index'),
]
