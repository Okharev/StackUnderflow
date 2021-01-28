from django.urls import path
from .views import (
    ThreadListView,
    ThreadDisplay,
    ThreadCreateView,
    ThreadDeleteView,
    PostDetailView,
    ThreadDetail,
    ThreadPost,
)

urlpatterns = [
    path("", ThreadListView.as_view(), name="thread-list"),
    path("thread/<int:pk>", ThreadDetail.as_view(), name="thread-detail"),
    path("thread/create", ThreadCreateView.as_view(), name="thread-create"),
    path("thread/delete/<int:pk>", ThreadDeleteView.as_view(), name="thread-delete"),
    # path("post/delete/<int:pk>", PostDeleteView.as_view(), name="post-delete"),
    # path("post/create", PostCreateView.as_view(), name="post-create"),
]
