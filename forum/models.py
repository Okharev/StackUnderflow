from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.html import format_html


class Category(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    url = models.URLField()
    hexcolor = models.CharField(
        max_length=7,
        default="ffffff",
        help_text="The color hex code without the '#'",
        validators=[MinValueValidator("00000"), MaxValueValidator("ffffff")],
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

    @property
    def post_count_parent(self):
        return Post.objects.filter(thread=self).filter(parent=True).count()

    @property
    def get_posts(self):
        return Post.objects.filter(thread=self)

    def __str__(self):
        return f"Thread {self.title} by {self.author}"


class Post(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        parent_link=True,
        related_name="children",
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if (
            self.thread.post_count_parent != 0
            and self.thread_id is not self.parent.thread_id
        ):
            raise ValidationError("Error: a post response must belong to thread")

        super(Post, self).clean()

    @property
    def votes(self):
        """
        TODO There might be more optimized queries
        :return:
        """
        pos = Karma.objects.filter(post=self).filter(karma=True).count()
        neg = Karma.objects.filter(post=self).filter(karma=False).count()
        return pos - neg

    def __str__(self):
        return f"{self.content} Post by {self.author} for Thread {self.thread}"


class Karma(models.Model):
    class Meta:
        unique_together = (("post", "author"),)

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    karma = models.BooleanField()

    def __str__(self):
        return f"Karma is {self.karma} by {self.author} for Post {self.post}"


class Categorisation(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
