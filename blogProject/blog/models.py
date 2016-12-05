from django.db import models as m


class Blog(m.Model):

    user = m.ForeignKey(
        'auth.User',
        verbose_name='Пользователь',
    )

    class Meta:
        verbose_name = "Блог"
        verbose_name_plural = "Блоги"


class Post(m.Model):

    blog = m.ForeignKey(
        Blog,
        verbose_name='Блог',
    )

    title = m.CharField(
        'Заголовок',
        max_length=200,
    )
    text = m.TextField(
        'Текст сообщения',
    )
    created_date = m.DateTimeField(
        'Создан',
        auto_now_add=True,
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_date", "user"]
        get_latest_by = "create_date"
        verbose_name = "Пост"
        verbose_name_plural = "Посты"


class NewsFeed(m.Model):

    user = m.ForeignKey(
        'auth.User',
        verbose_name='Пользователь',
    )
    posts = m.ManyToManyField(
        Blog,
        verbose_name='Новости',
    )

    class Meta:
        verbose_name = "Новостная лента"
        verbose_name_plural = "Новостные ленты"


class Reviewed(m.Model):

    post = m.ManyToManyField(
        Post,
    )

    blog = m.ForeignKey(
        Blog,
    )

    isreviewed = m.BooleanField(
        'Просмотрен',
        default=False,
    )

