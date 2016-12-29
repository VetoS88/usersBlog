from django.core import mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from blog.models import Post, NewsFeed
from blogProject import settings
from blogProject.settings import EMAIL_HOST_USER


@receiver(post_save, sender=Post)
def add_post(created, instance, **kwargs):
    blog = instance.blog
    # newsfeeds = NewsFeed.objects.filter(blogs=blog)
    # messages_list = []
    # for newsfeed in newsfeeds:
    #     email = newsfeed.user.email
    #     if email:
    #         subject = "В блоге {} новый пост".format(blog.name)
    #         body = "Тема {}. Опубликовано {}. Пользователь {}".format(instance.title,
    #                                                                   instance.created_date,
    #                                                                   blog.user)
    #         message = (subject, body, EMAIL_HOST_USER, [email])
    #         messages_list.append(message)

    # success = mail.send_mass_mail(messages_list, fail_silently=False)
    # print(success)
