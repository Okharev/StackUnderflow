from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.html import format_html
from mptt.models import MPTTModel, TreeForeignKey


class Category(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    url = models.URLField()
    hexcolor = models.CharField(
        max_length=7, default="ffffff", help_text="The color hex code without the '#'"
    )

    class Meta:
        verbose_name_plural = "Categories"

    @property
    def colored_name(self):
        return format_html(
            f'<span style="background-color: #{self.hexcolor};">{self.name}</span>'
        )

    def __str__(self):
        return self.slug


class Thread(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, help_text="The thread creator"
    )
    title = models.TextField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField(
        Category, through="Categorisation", related_name="cat"
    )

    @property
    def post_count(self):
        return Post.objects.filter(thread=self).count()

    def get_absolute_url(self):
        return reverse("thread-detail", kwargs={"pk": self.pk})

    def __str__(self):
        return f"Thread {self.title} by {self.author}"


class Post(MPTTModel):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    parent = TreeForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (("parent", "thread"),)

    class MPTTMeta:
        order_insertion_by = ["created_at"]

    def __str__(self):
        return f"Post by {self.author} for Thread {self.thread}"


class Karma(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    karma = models.BooleanField()

    def __str__(self):
        return f"Karma is {self.karma} by {self.author} for Post {self.post}"


class Categorisation(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
