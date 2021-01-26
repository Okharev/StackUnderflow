from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView
from forum.models import Thread


class ThreadListView(ListView):
    model = Thread
    paginate_by = 15


class ThreadDetailView(DetailView):
    model = Thread


class ThreadCreateView(CreateView):
    model = Thread
    fields = ["author", "title", "content", "categories"]
    success_url = reverse_lazy("thread-list")
