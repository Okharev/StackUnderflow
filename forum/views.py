from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, DetailView, DeleteView, FormView
from forum.forms import PostForm
from forum.models import Thread, Post


# TODO A more semantically correct way to implement things would be to have a List and Create View with single mixins
# but i'm too bad :(
# from django.views.generic.detail import SingleObjectMixin
"""
class ThreadDisplay(DetailView):
    model = Thread

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = PostForm()
        return context


class ThreadPost(SingleObjectMixin, FormView):
    template_name = "forum/thread_detail.html"
    form_class = PostForm
    model = Thread

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("thread-detail", kwargs={"pk": self.object.pk})

    # Perhaps Here in the validation ?
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

# Problem seems to be here
class ThreadDetail(View):
    def get(self, request, *args, **kwargs):
        view = ThreadDisplay.as_view()
        return view(request, *args, **kwargs)

    # especially here
    def post(self, request, *args, **kwargs):
        view = ThreadPost.as_view()
        return view(request, *args, **kwargs)
"""


class ThreadListView(ListView):
    model = Thread
    paginate_by = 15


class ThreadDetailView(View):
    form_class = PostForm
    initial = {"key": "value"}
    template_name = "forum/thread_detail.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        form.fields["parent"].queryset = Post.objects.filter(
            thread=Thread.objects.get(id=self.kwargs.get("pk"))
        )

        return render(
            request,
            self.template_name,
            {"form": form, "thread": Thread.objects.get(id=self.kwargs.get("pk"))},
        )

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST or None)
        form.instance.author = request.user
        form.instance.thread = Thread.objects.get(id=self.kwargs.get("pk"))
        if form.is_valid():
            form.save()
            return redirect("thread-list")

        return render(request, self.template_name, {"form": form})


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
    success_url = "forum/thread_detail.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.author != self.request.user:
            return redirect(self.success_url)
        return super().post(request, *args, **kwargs)


class PostDetailView(DetailView):
    model = Post
