from django import forms

from blog.models import Post


class PostCreateFoorm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'text', ]


