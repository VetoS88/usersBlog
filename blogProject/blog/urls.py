from django.conf.urls import url
from .views import *

urlpatterns = [

    url(r'^$', UserNewsFeed.as_view(), name="news_feed"),
    url(r'^page/(\d+)/$', UserNewsFeed.as_view(), name="news_feed_page"),
    url(r'^personal_blog/$', PersonalBlog.as_view(), name="personal_blog"),
    url(r'^users_blogs/$', UsersBlogs.as_view(), name="users_blogs"),
    url(r'^add_post/$', AddPost.as_view(), name="add_post"),
    url(r'^subscribe/(?P<blog_id>\d+)/', Subscribe.as_view(), name="subscribe"),
    url(r'^unsubscribe/(?P<blog_id>\d+)/', Unsubscribe.as_view(), name="subscribe"),
    url(r'^post/get/(?P<post_id>\d+)/', GetPost.as_view(), name="get_post"),



]
