from django.contrib import admin
from django.urls import path
from django.urls import re_path

from .views import post_create
from .views import post_delete
from .views import post_detail
from .views import post_list
from .views import post_update

app_name = 'posts'

urlpatterns = [
    re_path(r'^$',post_list,name='list'),
    re_path(r'^create/$',post_create),
    re_path(r'^(?P<id>\d+)/$',post_detail,name='post_detail'),

    re_path(r'^(?P<id>\d+)/edit/$',post_update,name='update'),
    re_path(r'^^(?P<id>\d+)/delete/$',post_delete),
    
]
