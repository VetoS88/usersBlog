from django.conf.urls import url
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response, redirect

from blog.forms import PostCreateFoorm
from .models import Post, NewsFeed, Blog


def news_feed(request):
    user = auth.get_user(request)
    if not user.is_authenticated:
        return redirect('/users_blogs/')
    user = auth.get_user_model().objects.get(username='qwe')
    newsfeed = NewsFeed.objects.get(user=user)
    userblogs = newsfeed.blogs.all()
    outposts = []
    for blog in userblogs:
        posts = blog.post_set.all()
        for post in posts:
            outposts.append(post)

    return render_to_response('blog/NewsFeed.html',
                              {
                                  'blogs': userblogs,
                                  'posts': outposts,
                                  'user':  user,
                              })

@login_required
def personal_blog(request):
    user = auth.get_user_model().objects.get(username='qwe')
    blog = Blog.objects.get(user=user)
    posts = blog.post_set.all()
    return render_to_response('blog/PersonalBlog.html',
                              {
                                  'blog': blog,
                                  'posts': posts,
                              })


def users_blogs(request):
    blogs = Blog.objects.all()
    return render_to_response('blog/UsersBlogs.html',
                              {
                                  'blogs': blogs,

                              })

def get_post(request):
    pass


def add_post(request):
    user = auth.get_user_model().objects.get(username='qwe')
    blog = Blog.objects.get(user=user)
    if request.method == 'POST':
        post = request.POST
        createform = PostCreateFoorm(post)
        if createform.is_valid():
            new_post = createform.save(commit=False)
            print(new_post.__dict__)
            new_post.blog_id = blog.id
            new_post.save()
        return render(request,
                      'blog/AddPost.html',
                      {
                          'postform': createform,
                      })
    else:
        createform = PostCreateFoorm()

    if request.method == 'GET':
        return render(request,
                      'blog/AddPost.html',
                      {'postform': createform})
    return render(request,
                  'blog/AddPost.html',
                  {'postform': createform})

