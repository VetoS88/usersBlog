from django.shortcuts import render, render_to_response
from .models import Post

def feeds(request):
    pass


def user_blog(request):
    pass


def blogs(request):
    pass


def main(request):
    posts = Post.objects.all()
    return render_to_response('blog/feeds.html',
                              {
                                  'feeds': posts,
                              })


