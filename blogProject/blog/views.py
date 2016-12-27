from django.contrib import auth
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from blog.forms import PostCreateFoorm
from .models import Post, NewsFeed, Blog, Reviewed


class UserNewsFeed(TemplateView):
    template_name = 'blog/NewsFeed.html'

    def get(self, request, *args, **kwargs):
        user = auth.get_user(request)
        if not user.is_authenticated:
            return redirect('/users_blogs/')
        newsfeed = NewsFeed.objects.filter(user=user)
        posts = Post.objects.filter(blog__newsfeed=newsfeed)
        reviewed = Post.objects.filter(reviewed__news_feed=newsfeed)
        userblogs = Blog.objects.filter(newsfeed__user=user)
        reviewed_posts = {}
        for post in posts:
            reviewed_posts[post] = True if post in reviewed else False
        return render(request,
                      self.template_name,
                      {
                          'blogs': userblogs,
                          'posts': reviewed_posts,
                          'user': user,
                      })


@method_decorator(login_required, name='dispatch')
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
        user = auth.get_user(request)
        if not user.is_authenticated:
            user = None
            blogs = Blog.objects.all()
        else:
            blogs = Blog.objects.exclude(newsfeed__user=user)
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

    def get(self, request, *args, **kwargs):
        user = auth.get_user(request)
        context = self.get_context_data(**kwargs)
        if not user.is_authenticated:
            user = None
        else:
            newsfeed = NewsFeed.objects.get(user=user)
            post = context['post']
            reviewed = Reviewed.objects.filter(news_feed=newsfeed, post=post)
            '''[0] костыль. потому что может быть
            несколько связей. '''
            if not reviewed:
                # print('Mark Reviewed!')
                is_review = Reviewed(
                    news_feed=newsfeed,
                    post=post,
                    isreviewed=True
                )
                is_review.save()
            # else:
            #     print('Reviewd already!')
        return self.render_to_response(context)


@method_decorator(login_required, name='dispatch')
class AddPost(TemplateView):
    template_name = 'blog/AddPost.html'
    form_class = PostCreateFoorm

    def post(self, request, *args, **kwargs):
        user = auth.get_user(request)
        # нужно будет сделать когда блог будет не один
        blog = Blog.objects.filter(user=user)[0]
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

#сделать наследнком RedirectView
@method_decorator(login_required, name='dispatch')
class Subscribe(View):
    def dispatch(self, request, *args, **kwargs):
        blog_id = kwargs['blog_id']
        blog = Blog.objects.get(id=blog_id)
        user = auth.get_user(request)
        user_news_feed = NewsFeed.objects.get(user=user)
        user_news_feed.blogs.add(blog)
        return redirect('/users_blogs/')


@method_decorator(login_required, name='dispatch')
class Unsubscribe(View):
    def dispatch(self, request, *args, **kwargs):
        blog_id = kwargs['blog_id']
        blog = Blog.objects.get(id=blog_id)
        user = auth.get_user(request)
        user_news_feed = NewsFeed.objects.get(user=user)
        user_news_feed.blogs.remove(blog)
        return redirect('/')
