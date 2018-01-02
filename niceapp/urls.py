# -*- coding: utf-8 -*-
# __author__ = ‘du‘
# __created_at__ = '2017/12/31'
from django.conf.urls import url

from views import *

urlpatterns = [
    url(r'^login$', access_login, name='login'),
    url(r'^logout$', access_logout, name='logout'),
    url(r'^$', index, name='index'),
    url(r'^submit$', submit, name='submit'),
    url(r'^connect$', connect, name='connect'),
    url(r'^fall_in_love$', fall_in_love, name='fall_in_love'),
    url(r'^be_in_love$', be_in_love, name='be_in_love'),
]
