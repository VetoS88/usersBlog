from django.contrib import admin
from .models import Post, NewsFeed, Blog


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = [
        'blog',
        'created_date',
        'title',

    ]

    list_filter = [
        'blog',
    ]

    filter_horizontal = ['newsfeeds', ]


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
