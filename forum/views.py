from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, DeleteView

from forum.models import Thread, Post


class ThreadListView(ListView):
    model = Thread
    paginate_by = 15


class ThreadDetailView(DetailView):
    model = Thread


class ThreadCreateView(CreateView):
    model = Thread
    fields = ["title", "content", "categories"]

    def get_success_url(self):
        return reverse("thread-detail", args=(self.object.id,))

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ThreadDeleteView(DeleteView):
    model = Thread
    success_url = reverse_lazy("thread-list")

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.author != self.request.user:
            return redirect(self.success_url)
        return super().post(request, *args, **kwargs)


class PostDetailView(DetailView):
    model = Post


class PostCreateView(CreateView):
    model = Post


class PostDeleteView(DeleteView):
    model = Post
