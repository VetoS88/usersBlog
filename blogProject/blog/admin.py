from django.contrib import admin

from blog.forms import PostCreateFoorm
from .models import Post, NewsFeed, Blog


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):

    form = PostCreateFoorm

    list_display = [
        'blog',
        'created_date',
        'title',

    ]

    list_filter = [
        'blog',
    ]

    filter_horizontal = ['newsfeeds', ]

    def get_form(self, request, obj=None, **kwargs):
        ModelForm = super(PostAdmin, self).get_form(request, obj, **kwargs)

        class ModelFormMetaClass(ModelForm):
            def __new__(cls, *args, **kwargs):
                kwargs['request'] = request
                return ModelForm(*args, **kwargs)

        return ModelFormMetaClass


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'user',
    ]

    list_filter = [
        'user',
    ]


@admin.register(NewsFeed)
class NewsFeedAdmin(admin.ModelAdmin):
    list_display = [
        'user',
    ]

    list_filter = [
        'user',
    ]

    filter_horizontal = ['blogs', ]
