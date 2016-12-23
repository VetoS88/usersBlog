from django.db.models.signals import post_save
from django.dispatch import receiver
from blog.models import Post


@receiver(post_save, sender=Post)
def add_post(instance, **kwargs):
    print("Creates is" + str(kwargs['created']))
    print("Created post is " + instance.title)

