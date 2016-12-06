from django.conf.urls import url, include
from .views import *


urlpatterns = [

    url(r'^$', news_feed, name="news_feed"),
    url(r'^personal_blog/$', personal_blog, name="personal_blog"),
    url(r'^users_blogs/$', users_blogs, name="users_blogs"),
    url(r'^add_post/$', add_post, name="add_post"),


]
