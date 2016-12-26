from django.apps import AppConfig


class BlogConfig(AppConfig):
    name = 'blog'
    verbose_name = "Блоги"

    def ready(self):
        from blog.siganls.user_creating import add_blog, add_newsfeed
        from blog.siganls.posts_to_newsfeed import posts_to_newsfeed
        from blog.siganls.add_post import add_post



