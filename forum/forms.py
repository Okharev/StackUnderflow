from django import forms
from django.contrib.auth.models import User

from forum.models import Post, Thread


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["author", "thread", "content"]
