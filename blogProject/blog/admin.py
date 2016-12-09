from django.contrib import admin
from .models import Post, NewsFeed, Blog

admin.site.register(Blog)

admin.site.register(NewsFeed)


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

    filter_horizontal = ['newsfeeds',]
