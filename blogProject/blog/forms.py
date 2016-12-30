from django import forms

from blog.models import Post, PostContent, Blog
from django.contrib import auth


class PostCreateFoorm(forms.ModelForm):
    """
        Если передаёться файлы контента (image или file),
        то пост сохраняется в любом случае.
        Обьект контета поста создаеться и сохраняется в методе save().
    """
    # blog = forms.ModelChoiceField(
    #     label='Blog',
    #     queryset=Bl.objects.all(),
    #     initial='anonymous',
    #     to_field_name='login',
    #     # widget=widgets. разобраться с виджетом выбора пользователя
    # )

    file = forms.FileField(
        label='Вложение',
        required=False,
    )

    image = forms.ImageField(
        label='Обложка',
        required=False,
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(PostCreateFoorm, self).__init__(*args, **kwargs)

    def clean(self):
        MAX_FILE_SIZE = 1 * 1024 * 1024

        cleaned_data = super(PostCreateFoorm, self).clean()

        image = cleaned_data.get('image')
        file = cleaned_data.get('file')


        if image:
            if image.size > MAX_FILE_SIZE:
                self.add_error('image', forms.ValidationError('max 1MB'))
                raise forms.ValidationError('Обложка слишком большого размера')

        if file:
            if file.size > MAX_FILE_SIZE:
                self.add_error('file', forms.ValidationError('max 1MB'))
                raise forms.ValidationError('Вложение слишком большого размера')

        return cleaned_data

    def save(self, commit=True):
        post = super(PostCreateFoorm, self).save(commit=False)
        cleaned_data = self.cleaned_data

        image = cleaned_data.get('image')
        file = cleaned_data.get('file')

        user = auth.get_user(self.request)
        # нужно будет сделать когда блог будет не один
        blog = Blog.objects.filter(user=user)[0]
        post.blog_id = blog.id
        if image or file:
            # Если есть контент то пост сохраняется в любом случае.
            post.save()
            post_content = PostContent(post=post)
            if file: post_content.file = file
            if image: post_content.image = image
            post_content.save()
            return post

        if commit:
            post.save()

        return post

    class Meta:
        model = Post
        fields = ['title', 'text', 'image', 'file']
