import os

from datetime import datetime, date, time, timezone
from django.db import models as m


class NewsFeed(m.Model):
    user = m.ForeignKey(
        'auth.User',
        verbose_name='Пользователь',
    )

    blogs = m.ManyToManyField(
        'Blog',
        verbose_name='Блоги',
    )

    def __str__(self):
        title = "{}'s newsfeed".format(self.user.username)
        return title

    class Meta:
        verbose_name = "Новостная лента"
        verbose_name_plural = "Новостные ленты"


class Blog(m.Model):
    name = m.CharField(
        'Название',
        max_length=50,
    )

    user = m.ForeignKey(
        'auth.User',
        verbose_name='Пользователь',
    )

    def __str__(self):
        title = "{}'s blog".format(self.user.username)
        return title

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

    text = m.TextField('Текст сообщения')

    created_date = m.DateTimeField(
        'Создан',
        auto_now_add=True,
    )

    newsfeeds = m.ManyToManyField(
        NewsFeed,
        verbose_name='Новости',
        blank=True,
        through='Reviewed'
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_date"]
        get_latest_by = "create_date"
        verbose_name = "Пост"
        verbose_name_plural = "Посты"


class Reviewed(m.Model):
    post = m.ForeignKey(Post)
    news_feed = m.ForeignKey(NewsFeed)

    isreviewed = m.BooleanField(
        'Просмотрен',
        default=False,
    )


class PostContent(m.Model):

    def get_file_name(self, filename):
        new_file_name = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
        extension = '.'.join(filename.split('.')[1:])
        filename_from_date = '{}.{}'.format(new_file_name, extension)

        return filename_from_date

    def get_file_path(self, filename):
        return os.path.join('files', self.get_file_name(filename))

    def get_image_path(self, filename):
        return os.path.join('images', self.get_file_name(filename))

    post = m.ForeignKey(Post)

    file = m.FileField(
        'Вложение',
        upload_to=get_file_path,
        blank=True,
        null=True,
    )

    image = m.ImageField(
        'Картинка',
        # upload_to='images',
        upload_to=get_image_path,
        blank=True,
        null=True,
    )
