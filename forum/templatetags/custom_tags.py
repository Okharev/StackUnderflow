import markdown as md
from django import template
from django.contrib.auth.models import User
from django.db.models import Count
from django.template.defaultfilters import stringfilter

from forum.models import Category, Thread, Karma

register = template.Library()


@register.inclusion_tag("forum/categories.html")
def show_categories(number):
	return {"categories": Category.objects.all()[:number]}


@register.inclusion_tag("forum/authors.html")
def show_authors(number):
	return {
		"authors": User.objects.only("username", "id")
			           .annotate(total_threads=Count("post"))
			           .order_by("-total_threads")[:number]
	}


@register.inclusion_tag("forum/recent_post.html")
def show_latest_post():
	return {"thread": Thread.objects.latest("created_at")}


@register.simple_tag
def has_voted(user, post, karma):
	"""
	TODO Surely a better way to optimize this
	:param user:
	:param post:
	:param karma:
	:return:
	"""
	test = Karma.objects.filter(author=user).filter(post=post).first()
	if test:
		if karma == test.karma:
			return "bg-gray-500"
		else:
			return "bg-black"
	else:
		return "bg-black"


@register.filter(name="add_class")
def add_class(value, arg):
	return value.as_widget(attrs={"class": arg})


@register.filter()
@stringfilter
def markdown(value):
	return md.markdown(value, extensions=["markdown.extensions.fenced_code"])
