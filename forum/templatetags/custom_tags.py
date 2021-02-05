from django import template

from forum.models import Karma

register = template.Library()


@register.simple_tag
def has_been_voted(post, user):
	if Karma.objects.filter(post=post).filter(author=user).count == 1:
		return True
	return False
