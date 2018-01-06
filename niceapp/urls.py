# -*- coding: utf-8 -*-
# __author__ = ‘du‘
# __created_at__ = '2017/12/31'
from django.conf.urls import url

from views import *

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^login$', access_login, name='login'),
    url(r'^logout$', access_logout, name='logout'),
    url(r'^content_page$', content_page, name='content_page'),
    url(r'^submit_content$', submit_content, name='submit_content'),
    url(r'^girl_after_submit$', girl_after_submit, name='girl_after_submit'),
    url(r'^suitable_girl_page$', suitable_girl_page, name='suitable_girl_page'),
    url(r'^choice_suitable_girl$', choice_suitable_girl, name='choice_suitable_girl'),
    url(r'^boy_after_invite$', boy_after_invite, name='boy_after_invite'),
    url(r'^invite_boy_page$', invite_boy_page, name='invite_boy_page'),
    url(r'^connect_page$', connect_page, name='connect_page'),
    url(r'^connect_to_fall_in_love$', connect_to_fall_in_love, name='connect_to_fall_in_love'),
    url(r'^connect_to_not_fit$', connect_to_not_fit, name='connect_to_not_fit'),
    url(r'^connect_to_complain$', connect_to_complain, name='connect_to_complain'),
    url(r'^love_page$', love_page, name='love_page'),
    url(r'^break_up_after_love$', break_up_after_love, name='break_up_after_love'),
]
