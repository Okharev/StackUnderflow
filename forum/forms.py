from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from forum.models import Post, Thread


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["parent", "content"]
