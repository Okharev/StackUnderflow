from django.urls import path

from . import views
from .views import (
    ThreadListView,
    ThreadCreateView,
    ThreadDeleteView,
    ThreadDetailView,
    # PostDetailView,
    # ThreadDisplay,
    # ThreadDetail,
    # ThreadPost,
)

urlpatterns = [
    path("", ThreadListView.as_view(), name="thread-list"),
    path("thread/<int:pk>", ThreadDetailView.as_view(), name="thread-detail"),
    path("thread/create", ThreadCreateView.as_view(), name="thread-create"),
    path("thread/delete/<int:pk>", ThreadDeleteView.as_view(), name="thread-delete"),
    path("post/<int:pk>/karmaUp", views.karma_upvote, name="karmaUp"),
    path("post/<int:pk>/karmaDown", views.karma_downvote, name="karmaDown"),
]
