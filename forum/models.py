from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Thread(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.TextField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField('Tag', through="Tagging")

    def __str__(self):
        return f"Thread by {self.author}"


class Post(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Post by {self.author} for Thread {self.thread}"


class Karma(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    karma = models.BooleanField()

    def __str__(self):
        return f"Karma is {self.karma} by {self.author} for Post {self.post}"


class Tag(models.Model):
    tag = models.CharField(max_length=50)

    def __str__(self):
        return f"Tag {self.tag}"


class Tagging(models.Model):
    threads = models.ForeignKey('Thread', on_delete=models.CASCADE)
    taggings = models.ForeignKey('Tag', on_delete=models.CASCADE)

    def __str__(self):
        return f"nb threads {self.threads}"
