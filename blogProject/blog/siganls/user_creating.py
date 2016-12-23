from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from blog.models import Blog, NewsFeed


@receiver(post_save, sender=User)
def add_blog(instance, **kwargs):
    if kwargs['created']:
        print("Hook creating user! add blog")
        name = "{}'s blog".format(instance.username)
        Blog.objects.create(user=instance, name=name)


@receiver(post_save, sender=User)
def add_newsfeed(instance, **kwargs):
    if kwargs['created']:
        print("Hook creating user! add newsfeed")
        NewsFeed.objects.create(user=instance)



