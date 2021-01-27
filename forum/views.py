from django.urls import reverse
from django.views.generic import CreateView, ListView, DetailView

from forum.models import Thread


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
