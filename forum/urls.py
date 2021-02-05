from django.urls import path

from . import views
from .views import (
	ThreadListView,
	ThreadCreateView,
	ThreadDeleteView,
	ThreadDetailView,
	PostUpdateView,
	ThreadUpdateView,
	CategoryDetailView,
)

urlpatterns = [
	path("", ThreadListView.as_view(), name="thread-list"),
	path("thread/<int:pk>", ThreadDetailView.as_view(), name="thread-detail"),
	path("thread/update/<int:pk>", ThreadUpdateView.as_view(), name="thread-update"),
	path("thread/create", ThreadCreateView.as_view(), name="thread-create"),
	path("thread/delete/<int:pk>", ThreadDeleteView.as_view(), name="thread-delete"),
	path("category/<int:pk>", CategoryDetailView.as_view(), name="category-detail"),
	path("post/update/<int:pk>", PostUpdateView.as_view(), name="post-update"),
	path("post/karmaUp/<int:pk>", views.karma_upvote, name="karmaUp"),
	path("post/karmaDown/<int:pk>", views.karma_downvote, name="karmaDown"),
]
