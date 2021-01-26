from django.urls import path, reverse
from .views import ThreadListView, ThreadDetailView, ThreadCreateView

urlpatterns = [
    path("", ThreadListView.as_view(), name="thread-list"),
    path("thread/<int:pk>", ThreadDetailView.as_view(), name="thread-detail"),
    path("thread/create", ThreadCreateView.as_view(), name="thread-create"),
]
