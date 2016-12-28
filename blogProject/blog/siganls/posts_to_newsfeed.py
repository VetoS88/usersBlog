from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from blog.models import NewsFeed, Blog


@receiver(m2m_changed, sender=NewsFeed.blogs.through)
def posts_to_newsfeed(sender, instance, action, pk_set, **kwargs):
    # print('Hook subscribing!')
    if action == 'post_add':
        # print(type(pk_set))
        blog = Blog.objects.get(id=pk_set.pop())
        # print(blog)

'''
    print(sender)
    print(instance)
    print('action: ', kwargs['action'])
    print('reverse: ', kwargs['reverse'])
    print('pk_set: ', kwargs['pk_set'])
    print('using: ', kwargs['using'])
    Hook subscribing!


<class 'blog.models.NewsFeed_blogs'>
iop's newsfeed
action:  post_remove
reverse:  False
pk_set:  {4}
using:  default
'''
