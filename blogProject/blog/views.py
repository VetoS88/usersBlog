from django.contrib import auth
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView
from django.views.generic import TemplateView

from blog.forms import PostCreateFoorm
from .models import Post, NewsFeed, Blog


class UserNewsFeed(TemplateView):
    template_name = 'blog/NewsFeed.html'

    def get(self, request, *args, **kwargs):
        user = auth.get_user(request)
        if not user.is_authenticated:
            return redirect('/users_blogs/')
        posts = Post.objects.filter(blog__newsfeed__user=user)
        # newsfeed = NewsFeed.objects.get(user=user)
        # posts = newsfeed.post_set.all()

        # print(posts)
        userblogs = Blog.objects.filter(newsfeed__user=user)
        print(userblogs)
        return render(request,
                      self.template_name,
                      {
                          'blogs': userblogs,
                          'posts': posts,
                          'user': user,
                      })


class PersonalBlog(ListView):
    template_name = 'blog/PersonalBlog.html'
    context_object_name = 'posts'

    def get_queryset(self):
        user = auth.get_user(self.request)
        posts = Post.objects.filter(blog__user=user).order_by('-created_date')
        return posts


class UsersBlogs(TemplateView):
    template_name = 'blog/UsersBlogs.html'

    def get(self, request, *args, **kwargs):
        blogs = Blog.objects.all()
        user = auth.get_user(request)
        if not user.is_authenticated:
            user = None
        return render(request,
                      self.template_name,
                      {
                          'blogs': blogs,
                          'user': user,
                      })


class GetPost(TemplateView):
    template_name = 'blog/Post.html'

    def get_context_data(self, **kwargs):
        context = super(GetPost, self).get_context_data(**kwargs)
        post_id = context['post_id']
        context['post'] = Post.objects.get(id=post_id)
        return context


class AddPost(TemplateView):
    template_name = 'blog/AddPost.html'
    form_class = PostCreateFoorm

    def post(self, request, *args, **kwargs):
        user = auth.get_user(request)
        blog = Blog.objects.get(user=user)
        post = request.POST
        createform = PostCreateFoorm(post)
        if createform.is_valid():
            new_post = createform.save(commit=False)
            new_post.blog_id = blog.id
            new_post.save()
        return render(request,
                      self.template_name,
                      {
                          'postform': createform,
                      })

    def get(self, request, *args, **kwargs):
        return render(request,
                      self.template_name,
                      {
                          'postform': self.form_class
                      })


class Subscribe(View):
    def dispatch(self, request, *args, **kwargs):
        blog_id = kwargs['blog_id']
        blog = Blog.objects.get(id=blog_id)
        user = auth.get_user(request)
        user_news_feed = NewsFeed.objects.get(user=user)
        user_news_feed.blogs.add(blog)
        return redirect('/users_blogs/')


class Unsubscribe(View):
    def dispatch(self, request, *args, **kwargs):
        blog_id = kwargs['blog_id']
        blog = Blog.objects.get(id=blog_id)
        user = auth.get_user(request)
        user_news_feed = NewsFeed.objects.get(user=user)

